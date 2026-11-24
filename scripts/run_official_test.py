"""One-shot official test for pj-081..pj-084 models (frozen after OOF bake-off)."""
# ponytail: CLI + atomic JSON cache per slug under results/official/

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.features import FEATURE_COLUMNS, build_features  # noqa: E402
from src.metrics import lrp_from_cdms  # noqa: E402
from src.official_test import (  # noqa: E402
    OFFICIAL_SLUGS,
    filter_official_test_events,
    fit_predict_slug,
    official_test_cdms,
    run_official_baselines,
)
from src.protocol import TTC_MIN, build_event_table  # noqa: E402

DATA = ROOT / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data"
OUT = ROOT / "results" / "official"


def _test_event_table(cdm: pd.DataFrame) -> pd.DataFrame:
    # meta for build_features; filter is pj-084 (not full pj-003)
    kept = filter_official_test_events(cdm)
    d = cdm.loc[cdm["event_id"].isin(kept["event_id"])].copy()
    g = d.groupby("event_id")
    t = pd.DataFrame({
        "event_id": g.size().index.astype("int64"),
        "n_cdm": g.size().astype("int64").to_numpy(),
        "first_ttc": g["time_to_tca"].max().to_numpy(dtype=np.float64),
        "last_ttc": g["time_to_tca"].min().to_numpy(dtype=np.float64),
    })
    return t.sort_values("event_id").reset_index(drop=True)


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, default=float) + "\n")
    tmp.replace(path)


def main() -> None:
    want = [s for s in (sys.argv[1:] or list(OFFICIAL_SLUGS)) if s in OFFICIAL_SLUGS or s in ("CRP", "LRP")]
    train_cdm = pd.read_csv(DATA / "train_data.csv")
    test_cdm = pd.read_csv(DATA / "test_data.csv")
    priv = pd.read_csv(DATA / "test_data_private.csv", usecols=["event_id", "true_risk"])

    train_table = build_event_table(train_cdm)
    train_feats = build_features(train_table, train_cdm)
    tr = train_feats.merge(train_table[["event_id", "risk_final", "lrp"]], on="event_id")
    X_tr = tr[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y_tr = tr["risk_final"].to_numpy(dtype=np.float64)
    lrp_tr = tr["lrp"].to_numpy(dtype=np.float64)
    eid_tr = tr["event_id"].to_numpy(dtype=np.int64)

    test_table = _test_event_table(test_cdm)
    test_in = official_test_cdms(test_cdm)
    test_feats = build_features(test_table, test_cdm)
    te = test_feats.merge(priv, on="event_id").sort_values("event_id")
    X_te = te[list(FEATURE_COLUMNS)].to_numpy(dtype=np.float64)
    y_te = te["true_risk"].to_numpy(dtype=np.float64)
    eid_te = te["event_id"].to_numpy(dtype=np.int64)
    lrp_map = lrp_from_cdms({
        "event_id": test_in["event_id"].to_numpy(),
        "time_to_tca": test_in["time_to_tca"].to_numpy(dtype=np.float64),
        "risk": test_in["risk"].to_numpy(dtype=np.float64),
    })
    lrp_te = np.array([lrp_map[int(e)] for e in eid_te], dtype=np.float64)

    gru_tr = gru_te = None
    if "gru" in want:
        from src.models.neural import build_sequences

        gru_tr = build_sequences(eid_tr, train_cdm, ttc_min=TTC_MIN)
        gru_te = build_sequences(eid_te, test_cdm, ttc_min=TTC_MIN)

    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"protocol": "pj-081..pj-084", "n_train": int(len(y_tr)), "n_test": int(len(y_te)), "models": {}}

    if "CRP" in want or "LRP" in want:
        base = run_official_baselines(y_te, lrp_te)
        for name in ("CRP", "LRP"):
            if name not in want:
                continue
            path = OUT / f"{name.lower()}.json"
            if path.exists():
                summary["models"][name] = json.loads(path.read_text())["metrics"]
                continue
            payload = {"model": name, "metrics": base[name], "n_test": int(len(y_te))}
            _atomic_write(path, payload)
            summary["models"][name] = base[name]
            print(name, json.dumps(base[name]))

    for slug in want:
        if slug in ("CRP", "LRP"):
            continue
        path = OUT / f"{slug}.json"
        if path.exists():
            summary["models"][slug] = json.loads(path.read_text())["metrics"]
            print(slug, "cache hit")
            continue
        t0 = time.time()
        kw = {}
        if slug == "mlp":
            kw["inputs_train"] = (X_tr,)
            kw["inputs_test"] = (X_te,)
        elif slug == "gru":
            kw["inputs_train"] = gru_tr
            kw["inputs_test"] = gru_te
        pred = fit_predict_slug(slug, X_tr, y_tr, X_te, lrp_train=lrp_tr, **kw)
        from src.models.linear import _rep_metrics

        metrics = _rep_metrics(y_te, pred["r_hat"], pred["p_hr"])
        payload = {
            "model": slug,
            "metrics": metrics,
            "seconds": round(time.time() - t0, 1),
            "n_test": int(len(y_te)),
        }
        _atomic_write(path, payload)
        pd.DataFrame({
            "event_id": eid_te,
            "r_hat": pred["r_hat"],
            "p_hr": pred["p_hr"],
        }).to_parquet(OUT / f"{slug}.parquet", index=False)
        summary["models"][slug] = metrics
        print(slug, payload["seconds"], "s", json.dumps(metrics))

    _atomic_write(OUT / "summary.json", summary)


if __name__ == "__main__":
    main()
