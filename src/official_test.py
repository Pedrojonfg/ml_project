"""One-shot official Zenodo test evaluation (pj-081..pj-084)."""
# ponytail: reuse family selectors; full-train as sole outer part

from __future__ import annotations

import numpy as np
import pandas as pd

from src.metrics import crp_predictions, f2_score, kelvins_l, mse_hr
from src.models import linear as lin
from src.models import trees
from src.models.trees import select_by_inner_cv  # noqa: F401 — tests may patch this name
from src.protocol import TTC_MIN

# per pj-081
OFFICIAL_SLUGS: tuple[str, ...] = (
    "CRP",
    "LRP",
    "ols",
    "ridge",
    "lasso",
    "knn",
    "kernel_ridge",
    "rf",
    "gbdt",
    "mlp",
    "gru",
    "s6_stage1_lr_none",
    "s6_stage1_lr_l2",
    "s6_stage1_lr_l1",
    "s6_lr_none__ols",
    "s6_lr_none__ridge",
    "s6_lr_none__lasso",
    "s6_lr_l2__ols",
    "s6_lr_l2__ridge",
    "s6_lr_l2__lasso",
    "s6_lr_l1__ols",
    "s6_lr_l1__ridge",
    "s6_lr_l1__lasso",
)

_LINEAR = frozenset({"ols", "ridge", "lasso", "knn", "kernel_ridge"})
_TREES = frozenset({"rf", "gbdt"})
_NEURAL = frozenset({"mlp", "gru"})
_STAGE1 = {
    "s6_stage1_lr_none": "lr_none",
    "s6_stage1_lr_l2": "lr_l2",
    "s6_stage1_lr_l1": "lr_l1",
}


def filter_official_test_events(cdm: pd.DataFrame) -> pd.DataFrame:
    # per pj-084: keep events with ≥1 CDM time_to_tca ≥ 2
    ids = (
        cdm.loc[cdm["time_to_tca"] >= TTC_MIN, "event_id"]
        .drop_duplicates()
        .sort_values()
        .to_numpy(dtype=np.int64)
    )
    return pd.DataFrame({"event_id": ids})


def official_test_cdms(cdm: pd.DataFrame) -> pd.DataFrame:
    # per pj-084: inputs only CDMs with ttc ≥ 2 of kept events
    kept = filter_official_test_events(cdm)["event_id"]
    out = cdm.loc[cdm["event_id"].isin(kept) & (cdm["time_to_tca"] >= TTC_MIN)].copy()
    return out.reset_index(drop=True)


def _pack(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    f2 = float(f2_score(y_true, y_pred))
    m_clip = float(mse_hr(y_true, y_pred, clip_at=-6.001))
    m_raw = float(mse_hr(y_true, y_pred, clip_at=None))
    return {
        "F2": f2,
        "MSE_HR_clipped": m_clip,
        "MSE_HR_unclipped": m_raw,
        "L_clipped": float(kelvins_l(m_clip, f2)),
        "L_unclipped": float(kelvins_l(m_raw, f2)),
    }


def run_official_baselines(y_true: np.ndarray, lrp: np.ndarray) -> dict[str, dict[str, float]]:
    y_true = np.asarray(y_true, dtype=np.float64)
    lrp = np.asarray(lrp, dtype=np.float64)
    return {
        "CRP": _pack(y_true, crp_predictions(len(y_true))),
        "LRP": _pack(y_true, lrp),
    }


def _fit_tree(kind: str, X, y, X_test, lrp_train):
    # per pj-083: nested re-selection on full train, seed 42
    X = np.asarray(X, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    lrp_train = np.asarray(lrp_train, dtype=np.float64)
    tr = np.arange(len(y))
    ns = tuple(trees.N_ESTIMATORS_GRID)
    ws = tuple(trees.W_GRID)
    rs = 42

    def fp(fit_idx, pred_idx, w):
        pipe, _ = trees._fit_variants(kind, X, y, lrp_train, fit_idx, w, ns, rs)
        return trees._predict_variants(kind, pipe, X[pred_idx], ns)

    (bw, bn), _scores = trees.select_by_inner_cv(fp, ws, tr, y, 42)
    fc = trees.floor_c(y, lrp_train, bw)
    pipe = (trees.make_rf if kind == "rf" else trees.make_gbdt)(int(bn), rs)
    pipe.fit(X, np.maximum(y, fc["c"]), **trees._sw(y, bw))
    r_hat = pipe.predict(X_test)
    return {"r_hat": np.asarray(r_hat, dtype=np.float64), "p_hr": trees.p_hr_from_r_hat(r_hat)}


def _fit_neural(arm: str, X, y, X_test, lrp_train, *, inputs_train, inputs_test):
    # per pj-083 / pj-073: select w on full train with seed 42, then one train_net
    from src.models.linear import make_preprocessor
    from src.models.neural import (
        MLP,
        MaskedGRU,
        SEQ_CHANNELS,
        SequencePreprocessor,
        _predict,
        _tensors,
        inner_split,
        seed_everything,
        train_net,
    )

    y = np.asarray(y, dtype=np.float64)
    lrp_train = np.asarray(lrp_train, dtype=np.float64)
    inputs_train = tuple(np.asarray(a) for a in inputs_train)
    inputs_test = tuple(np.asarray(a) for a in inputs_test)
    tr = np.arange(len(y))
    s_r = 42

    def pred_on_train_slice(fit_idx, pred_idx, w, k=0):
        fi, ei = inner_split(len(fit_idx), s_r, k)
        fit, es = fit_idx[fi], fit_idx[ei]
        fc = trees.floor_c(y[fit], lrp_train[fit], w)
        y_fit = np.maximum(y[fit], fc["c"])
        y_es = np.maximum(y[es], fc["c"])
        if arm == "mlp":
            pre = make_preprocessor().fit(inputs_train[0][fit])
            z_fit = (pre.transform(inputs_train[0][fit]),)
            z_es = (pre.transform(inputs_train[0][es]),)
            z_pred = (pre.transform(inputs_train[0][pred_idx]),)
            model_fn = lambda: MLP(z_fit[0].shape[1])
        else:
            seq, mask = inputs_train
            pre = SequencePreprocessor().fit(seq[fit], mask[fit])
            z_fit = (pre.transform(seq[fit], mask[fit]), mask[fit])
            z_es = (pre.transform(seq[es], mask[es]), mask[es])
            z_pred = (pre.transform(seq[pred_idx], mask[pred_idx]), mask[pred_idx])
            model_fn = lambda: MaskedGRU(len(SEQ_CHANNELS))
        seed_everything(s_r)
        model, _info = train_net(
            model_fn(), z_fit, y_fit, z_es, y_es, seed=s_r,
            w_fit=trees.hr_weights(y[fit], w), w_es=trees.hr_weights(y[es], w),
        )
        return _predict(model, _tensors(z_pred))

    (bw, _v), _scores = trees.select_by_inner_cv(
        lambda fi, pi, w: {0: pred_on_train_slice(fi, pi, w)},
        tuple(trees.W_GRID), tr, y, seed=42,
    )
    # final fit: early-stopping split inside full train; predict official test
    fi, ei = inner_split(len(tr), s_r, 0)
    fit, es = tr[fi], tr[ei]
    fc = trees.floor_c(y[fit], lrp_train[fit], bw)
    y_fit = np.maximum(y[fit], fc["c"])
    y_es = np.maximum(y[es], fc["c"])
    if arm == "mlp":
        pre = make_preprocessor().fit(inputs_train[0][fit])
        z_fit = (pre.transform(inputs_train[0][fit]),)
        z_es = (pre.transform(inputs_train[0][es]),)
        z_test = (pre.transform(inputs_test[0]),)
        model_fn = lambda: MLP(z_fit[0].shape[1])
    else:
        seq, mask = inputs_train
        pre = SequencePreprocessor().fit(seq[fit], mask[fit])
        z_fit = (pre.transform(seq[fit], mask[fit]), mask[fit])
        z_es = (pre.transform(seq[es], mask[es]), mask[es])
        z_test = (pre.transform(inputs_test[0], inputs_test[1]), inputs_test[1])
        model_fn = lambda: MaskedGRU(len(SEQ_CHANNELS))
    seed_everything(s_r)
    model, _info = train_net(
        model_fn(), z_fit, y_fit, z_es, y_es, seed=s_r,
        w_fit=trees.hr_weights(y[fit], bw), w_es=trees.hr_weights(y[es], bw),
    )
    r_hat = _predict(model, _tensors(z_test))
    return {"r_hat": np.asarray(r_hat, dtype=np.float64), "p_hr": trees.p_hr_from_r_hat(r_hat)}


def _fit_stage1(clf: str, X, y, X_test):
    from src.models import two_stage as s6

    out = s6.fit_predict_fold(clf, X, y, X_test)
    return {
        "r_hat": np.asarray(out["p_val"], dtype=np.float64),  # calibrated p as score
        "p_hr": np.asarray(out["alarm_val"], dtype=np.float64),
        "p_val": np.asarray(out["p_val"], dtype=np.float64),
        "alarm": np.asarray(out["alarm_val"], dtype=np.float64),
    }


def fit_predict_slug(
    slug: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    *,
    lrp_train: np.ndarray,
    inputs_train=None,
    inputs_test=None,
) -> dict:
    """One full-train fit + predict test (pj-082); re-selection per pj-083."""
    if slug in _LINEAR:
        out = lin.fit_predict_fold(slug, X_train, y_train, X_test)
        return {
            "r_hat": np.asarray(out["r_hat_val"], dtype=np.float64),
            "p_hr": np.asarray(out["p_hr_val"], dtype=np.float64),
        }
    if slug in _TREES:
        return _fit_tree(slug, X_train, y_train, X_test, lrp_train)
    if slug in _NEURAL:
        if inputs_train is None or inputs_test is None:
            raise ValueError(f"{slug} requires inputs_train and inputs_test")
        return _fit_neural(
            slug, X_train, y_train, X_test, lrp_train,
            inputs_train=inputs_train, inputs_test=inputs_test,
        )
    if slug in _STAGE1:
        return _fit_stage1(_STAGE1[slug], X_train, y_train, X_test)
    if slug.startswith("s6_") and "__" in slug:
        # s6_<clf>__<reg> — per pj-081 pairs
        body = slug[len("s6_"):]
        clf, reg = body.split("__", 1)
        s1 = _fit_stage1(clf, X_train, y_train, X_test)
        reg_out = lin.fit_predict_fold(reg, X_train, y_train, X_test)
        return {
            "r_hat": np.asarray(reg_out["r_hat_val"], dtype=np.float64),
            "p_hr": np.asarray(s1["alarm"], dtype=np.float64),
        }
    raise ValueError(f"unknown official-test slug {slug!r}")
