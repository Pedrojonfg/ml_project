"""S4 event-level bootstrap with BCa intervals (pj-006, pj-007, mf-016, mf-017)."""
# ponytail: metrics are computed from per-event sums times resample counts (matmul),
# not by calling src.metrics on every materialized resample; equality is tested.

from __future__ import annotations

from statistics import NormalDist

import numpy as np

from src.metrics import HR_THRESHOLD_LOG10, crp_constant_risk

BOOT_B = 10000  # per pj-006
BOOT_SEED = 2026  # per mf-016
BOOT_LEVEL = 0.95  # per pj-006
L_CAP_FACTOR = 10  # per mf-017
F2_ZERO_MAX_SHARE = 0.025  # per mf-017
CLIP_AT = -6.001  # per pj-007

KEYS = ("F2", "MSE_HR_clipped", "MSE_HR_unclipped", "L_clipped", "L_unclipped")
L_KEYS = ("L_clipped", "L_unclipped")
_CHUNK = 256  # resamples per matmul block; engineering only (memory)
_N = NormalDist()


def bootstrap_indices(n_events, B=BOOT_B, seed=BOOT_SEED):
    """(B, n_events) resample indices, one seeded generator (mf-016)."""
    return np.random.default_rng(seed).integers(0, n_events, size=(B, n_events))


def _features(y, r_hat, p_hr):
    """Per-event contributions (N, 5R+1): per repetition tp, fp, fn, sq_clipped, sq_unclipped; then HR flag."""
    y = np.asarray(y, dtype=np.float64)
    r_hat = np.atleast_2d(np.asarray(r_hat, dtype=np.float64))
    pos = np.atleast_2d(np.asarray(p_hr)).astype(bool)
    hr = y >= HR_THRESHOLD_LOG10
    cols = []
    for r in range(r_hat.shape[0]):
        p = pos[r]
        sq_u = np.where(hr, (y - r_hat[r]) ** 2, 0.0)
        sq_c = np.where(hr, (np.maximum(y, CLIP_AT) - np.maximum(r_hat[r], CLIP_AT)) ** 2, 0.0)
        cols += [hr & p, ~hr & p, hr & ~p, sq_c, sq_u]
    cols.append(hr)
    return np.column_stack(cols).astype(np.float64)


def _metrics(S):
    """Metrics from count-weighted sums S (..., 5R+1) -> dict of arrays (..., R)."""
    n_hr = S[..., -1:]
    T = S[..., :-1].reshape(S.shape[:-1] + (-1, 5))
    tp, fp, fn, sq_c, sq_u = (T[..., j] for j in range(5))
    den = 5.0 * tp + 4.0 * fn + fp  # F-beta, beta = 2
    with np.errstate(divide="ignore", invalid="ignore"):
        f2 = np.where(den == 0, 1.0, 5.0 * tp / den)  # all-negative perfect -> 1, as f2_score
        mse_c = np.where(n_hr > 0, sq_c / n_hr, 0.0)
        mse_u = np.where(n_hr > 0, sq_u / n_hr, 0.0)
        l_c = np.where(f2 == 0, np.inf, mse_c / f2)
        l_u = np.where(f2 == 0, np.inf, mse_u / f2)
    return dict(zip(KEYS, (f2, mse_c, mse_u, l_c, l_u)))


def metric_pack_reps(y, r_hat, p_hr, idx=None):
    """Five metrics per repetition, shape (R,) each; idx is ONE resample (N,)."""
    M = _features(y, r_hat, p_hr)
    counts = np.ones(len(M)) if idx is None else np.bincount(idx, minlength=len(M))
    return _metrics(counts @ M)


def bca_interval(theta_hat, boot, jack, level=BOOT_LEVEL):
    """BCa interval; boot may hold +inf (never below). None if z0 is infinite (mf-018);
    (theta_hat, theta_hat) if every boot value equals theta_hat."""
    boot = np.asarray(boot, dtype=np.float64)
    jack = np.asarray(jack, dtype=np.float64)
    if np.all(boot == theta_hat):
        return theta_hat, theta_hat
    prop = float(np.mean(boot < theta_hat))
    if prop in (0.0, 1.0):  # mf-018: z0 infinite, not computable; no clipping, no fallback
        return None
    z0 = _N.inv_cdf(prop)
    d = jack.mean() - jack
    s2 = float(np.sum(d**2))
    a = float(np.sum(d**3)) / (6.0 * s2**1.5) if s2 > 0 else 0.0
    out = []
    for z in (_N.inv_cdf((1 - level) / 2), _N.inv_cdf((1 + level) / 2)):
        u = z0 + z
        out.append(float(np.quantile(boot, _N.cdf(z0 + u / (1 - a * u)), method="linear")))  # per mf-020
    return out[0], out[1]


def _cap(pack, cap):
    """Replace infinite L by the per-model cap (mf-017), before averaging repetitions."""
    out = dict(pack)
    for k in L_KEYS:
        out[k] = np.where(np.isinf(pack[k]), cap[k], pack[k])
    return out


def bootstrap_report(y, lrp, r_hat, p_hr, B=BOOT_B, seed=BOOT_SEED):
    y = np.asarray(y, dtype=np.float64)
    r_hat = np.atleast_2d(np.asarray(r_hat, dtype=np.float64))
    N, R = len(y), r_hat.shape[0]
    lrp = np.asarray(lrp, dtype=np.float64)
    crp = np.full(N, crp_constant_risk())
    preds = {  # same R-repetition layout for all, so paired differences are exact
        "model": (r_hat, p_hr),
        "LRP": (np.tile(lrp, (R, 1)), np.tile(lrp >= HR_THRESHOLD_LOG10, (R, 1))),
        "CRP": (np.tile(crp, (R, 1)), np.tile(crp >= HR_THRESHOLD_LOG10, (R, 1))),
    }
    Ms = {n: _features(y, *a) for n, a in preds.items()}
    M = np.hstack(list(Ms.values()))
    w = M.shape[1] // 3

    # Resamples: one fresh generator drawn in row-chunks == bootstrap_indices(N, B, seed) (mf-016).
    rng = np.random.default_rng(seed)
    S = np.empty((B, M.shape[1]))
    for s in range(0, B, _CHUNK):
        idx = rng.integers(0, N, size=(min(_CHUNK, B - s), N))
        m = len(idx)
        flat = (idx + np.arange(m)[:, None] * N).ravel()
        S[s : s + m] = np.bincount(flat, minlength=m * N).reshape(m, N).astype(np.float64) @ M

    boot, orig, jack, caps, no_l = {}, {}, {}, {}, {}
    for j, n in enumerate(preds):
        sl = slice(j * w, (j + 1) * w)
        boot[n] = _metrics(S[:, sl])
        orig[n] = _metrics(M[:, sl].sum(axis=0))
        jack[n] = _metrics(M[:, sl].sum(axis=0) - M[:, sl])  # leave-one-event-out, closed form
        fin = {k: boot[n][k][np.isfinite(boot[n][k])] for k in L_KEYS}
        no_l[n] = {k: fin[k].size == 0 for k in L_KEYS}  # mf-019: no finite L, cap undefined
        caps[n] = {k: L_CAP_FACTOR * fin[k].max() for k in L_KEYS if fin[k].size}  # per mf-017
        if not any(no_l[n].values()):
            boot[n], orig[n], jack[n] = (_cap(p, caps[n]) for p in (boot[n], orig[n], jack[n]))

    zero = (boot["model"]["F2"] == 0).any(axis=1)
    n_zero = int(zero.sum())
    share = n_zero / B
    reliable = bool(share <= F2_ZERO_MAX_SHARE)

    def stat(n, k):
        return boot[n][k].mean(axis=1), float(orig[n][k].mean()), jack[n][k].mean(axis=1)

    def entry(b, t, j, no_ci=False):
        ci = None if no_ci else bca_interval(t, b, j)  # mf-018 / mf-019
        return {"estimate": t, "ci": None if ci is None else list(ci), "bca_not_computable": ci is None}

    rep = {}
    for k in KEYS:
        bm, tm, jm = stat("model", k)
        nl = k in L_KEYS and no_l["model"][k]
        e = entry(bm, tm, jm, nl)
        for base in ("LRP", "CRP"):
            bb, tb, jb = stat(base, k)
            nlp = k in L_KEYS and (nl or no_l[base][k])
            e[f"paired_vs_{base}"] = entry(bm - bb, tm - tb, jm - jb, nlp)
            if k in L_KEYS:
                e[f"paired_vs_{base}"]["reliable"] = reliable and not nlp
        if k in L_KEYS:
            e["reliable"] = reliable and not nl
        rep[k] = e
    rep.update(n_f2_zero_resamples=n_zero, f2_zero_share=share, L_reliable=reliable and not any(no_l["model"].values()))
    return rep
