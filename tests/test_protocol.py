"""Tests for the S1 event protocol (pj-001..pj-007): event table and folds."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.model_selection import StratifiedKFold

from src.metrics import lrp_from_cdms
from src.protocol import N_SPLITS, SEEDS, build_event_table, make_folds

DATA = (
    Path(__file__).resolve().parents[1]
    / "data/esa/Collision Avoidance Challenge - Dataset/kelvins_competition_data/train_data.csv"
)
COLUMNS = ["event_id", "risk_final", "y_hr", "lrp", "first_ttc", "last_ttc", "n_cdm"]


def cdms(events):
    """events: {event_id: [(time_to_tca, risk), ...]} -> CDM frame."""
    rows = [(e, t, r) for e, lst in events.items() for t, r in lst]
    df = pd.DataFrame(rows, columns=["event_id", "time_to_tca", "risk"])
    return df.astype({"event_id": "int64", "time_to_tca": "float64", "risk": "float64"})


def row(table, event_id):
    return table[table.event_id == event_id].iloc[0]


def synthetic_table(n=200, n_hr=20):
    y = np.zeros(n, dtype=bool)
    y[:n_hr] = True
    return pd.DataFrame({"event_id": np.arange(n, dtype="int64") * 3 + 7, "y_hr": y})


def reference_folds(table, seed):
    skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    fold = np.empty(len(table), dtype="int64")
    for k, (_, test) in enumerate(skf.split(table, table.y_hr)):
        fold[test] = k
    return fold


# ---------- event table, synthetic ----------


def test_keep_and_drop_rules():
    df = cdms({
        1: [(5, -5.0), (3, -5.5), (0.4, -4.0)],  # kept
        2: [(1.5, -5.0), (0.3, -5.0)],  # no CDM >= 2 d
        3: [(6, -5.0), (4, -5.0), (2.5, -5.0)],  # last CDM >= 2 d
        4: [(6, -5.0), (1.5, -5.0)],  # kept, last in [1, 2)
        5: [(0.5, -5.0)],  # one CDM
    })
    assert build_event_table(df).event_id.tolist() == [1, 4]


def test_risk_final_unclipped_and_label():
    df = cdms({
        1: [(5, -5.0), (0.4, -4.2)],
        2: [(5, -5.0), (0.4, -9.3)],
        3: [(5, -5.0), (0.4, -6.0)],
        4: [(5, -5.0), (0.4, -6.001)],
    })
    t = build_event_table(df)
    assert row(t, 1).risk_final == -4.2
    assert row(t, 2).risk_final == -9.3
    assert t.y_hr.tolist() == [True, False, True, False]


def test_lrp_and_ttc_values():
    df = cdms({1: [(7.5, -8.0), (4.0, -7.0), (2.2, -6.5), (1.1, -5.0), (0.2, -4.0)]})
    r = row(build_event_table(df), 1)
    assert r.lrp == -6.5  # min ttc among >= 2, not the label CDM
    assert r.risk_final == -4.0
    assert (r.first_ttc, r.last_ttc, r.n_cdm) == (7.5, 0.2, 5)


def test_lrp_boundary_ttc_exactly_two():
    df = cdms({1: [(5, -7.0), (2.0, -6.2), (0.5, -5.0)]})
    assert row(build_event_table(df), 1).lrp == -6.2


def test_columns_dtypes_sorted_and_index():
    df = cdms({9: [(5, -5.0), (0.4, -4.0)], 2: [(5, -7.0), (1.0, -6.0)]})
    t = build_event_table(df)
    assert t.columns.tolist() == COLUMNS
    assert t.dtypes.astype(str).tolist() == [
        "int64", "float64", "bool", "float64", "float64", "float64", "int64"
    ]
    assert t.event_id.tolist() == [2, 9]
    assert isinstance(t.index, pd.RangeIndex)


def test_shuffle_invariance_and_extra_columns():
    df = cdms({
        1: [(5, -5.0), (3, -5.5), (0.4, -4.0)],
        2: [(6, -7.0), (2.5, -6.5), (1.5, -6.0)],
        3: [(4, -8.0), (0.9, -9.0)],
    })
    df["junk"] = "x"
    shuffled = df.sample(frac=1, random_state=0).reset_index(drop=True)
    pd.testing.assert_frame_equal(build_event_table(df), build_event_table(shuffled))


def test_lrp_matches_metrics_on_kept_events():
    rng = np.random.default_rng(0)
    events = {}
    for e in range(1, 41):
        ttc = np.sort(rng.uniform(0.1, 7, size=rng.integers(2, 8)))[::-1]
        events[e] = list(zip(ttc, rng.uniform(-10, -3, size=len(ttc))))
    df = cdms(events)
    t = build_event_table(df)
    assert 0 < len(t) < 40
    ref = lrp_from_cdms({c: df[c].to_numpy() for c in ["event_id", "time_to_tca", "risk"]})
    for _, r in t.iterrows():
        assert r.lrp == ref[int(r.event_id)]


# ---------- folds, synthetic ----------


def test_folds_shape_columns_and_uniqueness():
    t = synthetic_table()
    f = make_folds(t)
    assert f.columns.tolist() == ["event_id", "rep", "seed", "fold"]
    assert (f.dtypes.astype(str) == "int64").all()
    assert len(f) == len(t) * len(SEEDS)
    assert not f.duplicated(["event_id", "rep"]).any()
    assert f.fold.between(0, N_SPLITS - 1).all()
    assert f.rep.tolist() == sorted(f.rep.tolist())
    for _, g in f.groupby("rep"):
        assert g.event_id.tolist() == sorted(t.event_id)
        assert g.event_id.is_unique  # an event sits in one fold per repetition


def test_folds_seed_column():
    f = make_folds(synthetic_table())
    assert (f.seed == f.rep.map(dict(enumerate(SEEDS)))).all()


def test_folds_deterministic_and_seed_dependent():
    t = synthetic_table()
    a, b = make_folds(t), make_folds(t)
    pd.testing.assert_frame_equal(a, b)
    folds = [g.fold.to_numpy() for _, g in a.groupby("rep")]
    assert any(not np.array_equal(folds[0], x) for x in folds[1:])
    assert not np.array_equal(
        make_folds(t, seeds=(1,)).fold.to_numpy(), make_folds(t, seeds=(2,)).fold.to_numpy()
    )


def test_folds_match_stratified_kfold_reference():
    t = synthetic_table()
    f = make_folds(t)
    for i, seed in enumerate(SEEDS):
        g = f[f.rep == i]
        assert np.array_equal(g.fold.to_numpy(), reference_folds(t, seed))


def test_folds_stratification_balanced():
    t = synthetic_table(200, 20)
    f = make_folds(t).merge(t, on="event_id")
    for _, g in f.groupby("rep"):
        counts = g.groupby("fold").y_hr.sum()
        assert len(counts) == N_SPLITS
        assert counts.max() - counts.min() <= 1


# ---------- real data ----------

needs_data = pytest.mark.skipif(not DATA.exists(), reason="train_data.csv missing")


@pytest.fixture(scope="module")
def raw():
    return pd.read_csv(DATA, usecols=["event_id", "time_to_tca", "risk"])


@pytest.fixture(scope="module")
def table(raw):
    return build_event_table(raw)


@pytest.fixture(scope="module")
def folds(table):
    return make_folds(table)


@needs_data
def test_real_event_counts(table):
    assert len(table) == 8892
    assert int(table.y_hr.sum()) == 93


@needs_data
def test_real_filter_invariants(raw, table):
    assert (table.last_ttc < 2).all()
    has_early = raw[raw.time_to_tca >= 2].event_id.unique()
    assert table.event_id.isin(has_early).all()
    assert int((table.last_ttc < 1).sum()) == 8293
    assert int(((table.last_ttc >= 1) & (table.last_ttc < 2)).sum()) == 599


@needs_data
def test_real_folds(table, folds):
    assert len(folds) == 8892 * len(SEEDS)
    hr = folds.merge(table[["event_id", "y_hr"]], on="event_id")
    for _, g in hr.groupby("rep"):
        assert g.event_id.is_unique and len(g) == 8892
        counts = g.groupby("fold").y_hr.sum()
        assert len(counts) == N_SPLITS
        assert set(counts) <= {18, 19}
        assert counts.sum() == 93
