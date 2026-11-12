"""O2 t_raw: mf-035 recipe on sigmoid(z) of inner-OOF stage-1 scores (pj-049 option A)."""
# ponytail: reuse saved C from results/s6_stage1_*.json; only recompute oof_z (no select_c)

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import Parallel, delayed

from src.models.linear import choose_alarm_line
from src.models.two_stage import CLASSIFIERS, oof_z


def _sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=np.float64)
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    ez = np.exp(z[~pos])
    out[~pos] = ez / (1.0 + ez)
    return out


def _one_fold(name: str, C: float | None, X_train: np.ndarray, y_train: np.ndarray) -> float:
    y_hr = y_train >= -6.0
    z_oof, _ = oof_z(name, C, X_train, y_hr)
    return float(choose_alarm_line(_sigmoid(z_oof), y_train))


def compute_t_raw_by_clf(
    X: np.ndarray,
    y: np.ndarray,
    event_ids: np.ndarray,
    folds: pd.DataFrame,
    stage1_dir: Path,
    n_jobs: int = 1,
) -> dict[tuple[str, int, int], float]:
    """Return {(clf, rep, fold): t_raw} using inner-OOF raw probs on each outer train fold."""
    out: dict[tuple[str, int, int], float] = {}
    for clf in CLASSIFIERS:
        path = stage1_dir / f"s6_stage1_{clf}.json"
        records = json.loads(path.read_text())["fold_records"]
        tasks = []
        keys = []
        for rec in records:
            rep, fold = int(rec["rep"]), int(rec["fold"])
            C = rec["C"]
            sub = folds[folds.rep == rep]
            fold_of = pd.Series(sub.fold.to_numpy(), index=sub.event_id.to_numpy()).reindex(event_ids).to_numpy()
            val = fold_of == fold
            keys.append((clf, rep, fold))
            tasks.append((C, X[~val], y[~val]))
        if n_jobs == 1:
            vals = [_one_fold(clf, C, Xt, yt) for C, Xt, yt in tasks]
        else:
            vals = Parallel(n_jobs=n_jobs)(delayed(_one_fold)(clf, C, Xt, yt) for C, Xt, yt in tasks)
        for k, v in zip(keys, vals):
            out[k] = float(v)
    return out


def t_raw_to_jsonable(t_raw: dict[tuple[str, int, int], float]) -> list[dict]:
    return [{"clf": c, "rep": r, "fold": f, "t_raw": t} for (c, r, f), t in sorted(t_raw.items())]


def t_raw_from_jsonable(rows: list[dict]) -> dict[tuple[str, int, int], float]:
    return {(r["clf"], int(r["rep"]), int(r["fold"])): float(r["t_raw"]) for r in rows}
