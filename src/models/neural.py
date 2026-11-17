"""S8 PyTorch ablation: tabular MLP + masked GRU vs the S4 table (pj-061..pj-070)."""

from __future__ import annotations

import copy
import os
import pickle
import random
import tempfile

import numpy as np
import pandas as pd
import torch
from torch import nn

from src.features import OBJECT_TYPES
from src.models.linear import make_preprocessor
from src.models import trees
from src.models.trees import CvResult, kelvins_pack, p_hr_from_r_hat
from src.protocol import N_SPLITS, TTC_MIN

SEQ_NUMERIC = ("risk", "miss_distance", "relative_speed", "t_weighted_rms", "time_to_tca")  # per pj-063 (engineering detail in LEDGER)
SEQ_CHANNELS = SEQ_NUMERIC + tuple(f"obj_{t.replace(' ', '_')}" for t in OBJECT_TYPES)  # per pj-063, pj-067: last-usable one-hot on each step
T_MAX = 20  # per pj-067
MLP_HIDDEN = (128, 64)  # per pj-067
GRU_HIDDEN = 64
GRU_LAYERS = 1
LR = 1e-3  # per pj-066
BETAS = (0.9, 0.999)
EPS = 1e-8
WEIGHT_DECAY = 0.0
BATCH_SIZE = 64
MAX_EPOCHS = 100  # per pj-074
PATIENCE = 10
INNER_VAL_FRAC = 0.20
_N_NUM = len(SEQ_NUMERIC)


def build_sequences(event_ids, cdm: pd.DataFrame, *, ttc_min=TTC_MIN, T=T_MAX):
    # per pj-063, pj-067
    event_ids = np.asarray(event_ids)
    use = cdm[cdm["time_to_tca"] >= ttc_min]
    use = use.sort_values(["event_id", "time_to_tca"], kind="stable")  # ascending: rank 0 = closest to TCA
    rank = use.groupby("event_id").cumcount().to_numpy()
    use = use[rank < T]
    rank = rank[rank < T]
    length = use.groupby("event_id").size()
    row = pd.Index(event_ids).get_indexer(use["event_id"])
    in_req = row >= 0
    missing = ~pd.Index(event_ids).isin(length.index)
    if missing.any():
        raise ValueError(f"events without usable CDMs: {event_ids[missing][:5].tolist()}")
    use, rank, row = use[in_req], rank[in_req], row[in_req]
    pos = length.loc[use["event_id"]].to_numpy() - 1 - rank  # left-aligned, descending time_to_tca
    seq = np.zeros((len(event_ids), T, len(SEQ_CHANNELS)))
    mask = np.zeros((len(event_ids), T), dtype=bool)
    seq[row, pos, :_N_NUM] = use[list(SEQ_NUMERIC)].to_numpy(dtype=np.float64)
    mask[row, pos] = True
    closest = use[rank == 0]
    type_idx = closest["c_object_type"].map({t: i for i, t in enumerate(OBJECT_TYPES)}).fillna(-1).to_numpy(dtype=int)
    ok = type_idx >= 0
    crow = row[rank == 0][ok]
    onehot = np.zeros((len(event_ids), len(OBJECT_TYPES)))
    onehot[crow, type_idx[ok]] = 1.0
    seq[:, :, _N_NUM:] = onehot[:, None, :] * mask[:, :, None]
    return seq, mask


class SequencePreprocessor:
    # per pj-065: median-impute then standardize numeric channels over valid steps only
    def fit(self, seq, mask):
        v = seq[mask][:, :_N_NUM]
        self.median_ = np.nanmedian(v, axis=0)
        filled = np.where(np.isnan(v), self.median_, v)
        self.mean_ = filled.mean(axis=0)
        std = filled.std(axis=0)
        self.std_ = np.where(std == 0, 1.0, std)
        return self

    def transform(self, seq, mask):
        z = np.array(seq, dtype=np.float64)
        num = z[:, :, :_N_NUM]
        num = np.where(np.isnan(num), self.median_, num)
        z[:, :, :_N_NUM] = (num - self.mean_) / self.std_
        z[~mask] = 0.0
        return z


class MLP(nn.Module):
    # per pj-064
    def __init__(self, d_in: int):
        super().__init__()
        h1, h2 = MLP_HIDDEN
        self.net = nn.Sequential(nn.Linear(d_in, h1), nn.ReLU(), nn.Linear(h1, h2), nn.ReLU(), nn.Linear(h2, 1))

    def forward(self, x):
        return self.net(x).squeeze(-1)


class MaskedGRU(nn.Module):
    # per pj-064, pj-067: valid steps are left-aligned, so padding never precedes a valid step
    def __init__(self, c_in: int):
        super().__init__()
        self.gru = nn.GRU(c_in, GRU_HIDDEN, num_layers=GRU_LAYERS, batch_first=True, dropout=0)
        self.head = nn.Linear(GRU_HIDDEN, 1)

    def forward(self, x, mask):
        out, _ = self.gru(x)
        last = out[torch.arange(len(x)), mask.sum(dim=1) - 1]
        return self.head(last).squeeze(-1)


def seed_everything(seed: int) -> None:
    # per pj-069
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def inner_split(n: int, seed: int, fold: int):
    # per pj-066
    perm = np.random.default_rng([seed, fold]).permutation(n)
    n_es = round(INNER_VAL_FRAC * n)
    return perm[n_es:], perm[:n_es]


def _tensors(inputs):
    return [torch.as_tensor(a).float() if np.issubdtype(np.asarray(a).dtype, np.floating)
            else torch.as_tensor(a) for a in inputs]


def _predict(model, tensors):
    model.eval()
    with torch.no_grad():
        return model(*tensors).double().numpy()


def train_net(model, inputs_fit, y_fit, inputs_es, y_es, *, seed, w_fit, w_es):
    # per pj-066, pj-074, pj-076: Adam, weighted-mean loss sum(w*e^2)/sum(w), same weighted
    # monitor on the inner es set, best weights restored
    xf, xe = _tensors(inputs_fit), _tensors(inputs_es)
    yf = torch.as_tensor(np.asarray(y_fit, dtype=np.float64)).float()
    wf = torch.as_tensor(np.asarray(w_fit, dtype=np.float64)).float()
    y_es = np.asarray(y_es, dtype=np.float64)
    w_es = np.asarray(w_es, dtype=np.float64)
    opt = torch.optim.Adam(model.parameters(), lr=LR, betas=BETAS, eps=EPS, weight_decay=WEIGHT_DECAY)
    gen = torch.Generator().manual_seed(seed)
    n = len(yf)
    best, best_epoch, best_state, epochs_run = np.inf, 0, None, 0
    for epoch in range(1, MAX_EPOCHS + 1):
        model.train()
        perm = torch.randperm(n, generator=gen)
        for i in range(0, n, BATCH_SIZE):
            b = perm[i:i + BATCH_SIZE]
            opt.zero_grad()
            loss = (wf[b] * (model(*[x[b] for x in xf]) - yf[b]) ** 2).sum() / wf[b].sum()
            loss.backward()
            opt.step()
        epochs_run = epoch
        es_loss = float(np.sum(w_es * (_predict(model, xe) - y_es) ** 2) / np.sum(w_es))
        if es_loss < best:
            best, best_epoch, best_state = es_loss, epoch, copy.deepcopy(model.state_dict())
        elif epoch - best_epoch >= PATIENCE:
            break
    model.load_state_dict(best_state)
    model.eval()
    return model, {"best_epoch": best_epoch, "epochs_run": epochs_run, "best_es_loss": best}


def run_neural_cv(arm, inputs, y, lrp, event_ids, folds, cache_dir=None) -> CvResult:
    # per pj-062, pj-065, pj-066, pj-068, pj-072, pj-073
    if arm not in ("mlp", "gru"):
        raise ValueError(f"unknown arm {arm!r}")
    y = np.asarray(y, dtype=np.float64)
    lrp = np.asarray(lrp, dtype=np.float64)
    inputs = tuple(np.asarray(a) for a in inputs)
    index = pd.Index(event_ids)
    reps = sorted(folds["rep"].unique())
    oof = np.full((len(reps), len(y)), np.nan)
    frames, floors = [], []

    def fit_predict(fit_idx, pred_idx, w, s_r, k):
        # one network on the 80% fit part of fit_idx; floor c(w), weights and preprocessing from it
        fi, ei = inner_split(len(fit_idx), s_r, k)
        fit, es = fit_idx[fi], fit_idx[ei]
        fc = trees.floor_c(y[fit], lrp[fit], w)
        y_fit, y_es = np.maximum(y[fit], fc["c"]), np.maximum(y[es], fc["c"])
        if arm == "mlp":
            pre = make_preprocessor().fit(inputs[0][fit])
            z_fit, z_es, z_pred = ((pre.transform(inputs[0][i]),) for i in (fit, es, pred_idx))
            model = lambda: MLP(z_fit[0].shape[1])
        else:
            seq, mask = inputs
            pre = SequencePreprocessor().fit(seq[fit], mask[fit])
            z_fit, z_es, z_pred = ((pre.transform(seq[i], mask[i]), mask[i]) for i in (fit, es, pred_idx))
            model = lambda: MaskedGRU(len(SEQ_CHANNELS))
        seed_everything(s_r)
        model, info = train_net(model(), z_fit, y_fit, z_es, y_es, seed=s_r,
                                w_fit=trees.hr_weights(y[fit], w), w_es=trees.hr_weights(y[es], w))
        return _predict(model, _tensors(z_pred)), fc, info

    for ri, r in enumerate(reps):
        path = os.path.join(cache_dir, f"rep{int(r)}.pkl") if cache_dir is not None else None
        if path and os.path.exists(path):  # per pj-073: resume per finished rep
            with open(path, "rb") as fh:
                d = pickle.load(fh)
        else:
            s_r = 42 + int(r)
            d = {"pred": np.full(len(y), np.nan), "frames": [], "floors": []}
            sub = folds[folds["rep"] == r]
            pos = index.get_indexer(sub["event_id"])
            fold_of = sub["fold"].to_numpy()
            for k in range(N_SPLITS):
                val, tr = pos[fold_of == k], pos[fold_of != k]
                (w, v), scores = trees.select_by_inner_cv(
                    lambda fi, pi, w: {0: fit_predict(fi, pi, w, s_r, k)[0]},
                    tuple(trees.W_GRID), tr, y, seed=s_r)
                r_hat, fc, info = fit_predict(tr, val, w, s_r, k)
                d["pred"][val] = r_hat
                d["frames"].append(pd.DataFrame({
                    "event_id": np.asarray(event_ids)[val], "rep": int(r), "fold": k,
                    "r_hat": r_hat, "p_hr": p_hr_from_r_hat(r_hat)}))
                d["floors"].append({"rep": int(r), "fold": k, **fc, **info,
                                    "inner_L": {f"{a}|{b}": float(L) for (a, b), L in scores.items()}})
            if path:
                fd, tmp = tempfile.mkstemp(dir=cache_dir)
                with os.fdopen(fd, "wb") as fh:
                    pickle.dump(d, fh)
                os.replace(tmp, path)
        oof[ri] = d["pred"]
        frames += d["frames"]
        floors += d["floors"]
    if np.isnan(oof).any():
        raise RuntimeError("NaN in out-of-fold predictions")
    per_rep = [kelvins_pack(y, oof[i]) for i in range(len(reps))]
    return CvResult(
        oof_pred=oof,
        metrics={key: float(np.mean([m[key] for m in per_rep])) for key in per_rep[0]},
        metrics_per_rep=per_rep,
        metrics_pooled=kelvins_pack(np.tile(y, len(reps)), oof.ravel()),
        fold_frames=frames,
        importances=np.zeros(0),
        floors=floors,
    )
