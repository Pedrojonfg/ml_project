"""S8 PyTorch ablation (pj-061..pj-070) + iteration 2 (pj-072..pj-076): sequences,
preprocessing, nets, weighted training loop, nested-CV selection of w."""

import copy
import inspect
import random

import numpy as np
import pandas as pd
import pytest
import torch
from sklearn.model_selection import StratifiedKFold

import src.models.neural as nn_mod
import src.models.trees as trees_mod
from src.features import FEATURE_COLUMNS, OBJECT_TYPES
from src.metrics import f2_score
from src.models.linear import make_preprocessor
from src.models.neural import (
    MLP,
    MaskedGRU,
    SequencePreprocessor,
    build_sequences,
    inner_split,
    run_neural_cv,
    seed_everything,
    train_net,
)
from src.protocol import make_folds

C = 10  # 5 numeric + 5 one-hot channels (contract)
OBJ = [f"obj_{t.replace(' ', '_')}" for t in OBJECT_TYPES]
NUM = ["risk", "miss_distance", "relative_speed", "t_weighted_rms", "time_to_tca"]


# ---------------------------------------------------------------- registry (pj-066, pj-067)

def test_registry_constants_match_adrs():
    # protects the ratified values from a silent edit (pj-066 package A, pj-067 option 1);
    # pj-074 supersedes the epoch cap: 100 for both arms, patience 10 unchanged
    assert nn_mod.SEQ_NUMERIC == tuple(NUM)
    assert nn_mod.SEQ_CHANNELS == tuple(NUM + OBJ)
    assert nn_mod.T_MAX == 20
    assert nn_mod.MLP_HIDDEN == (128, 64)
    assert nn_mod.GRU_HIDDEN == 64 and nn_mod.GRU_LAYERS == 1
    assert nn_mod.LR == 1e-3 and nn_mod.BETAS == (0.9, 0.999)
    assert nn_mod.EPS == 1e-8 and nn_mod.WEIGHT_DECAY == 0.0
    assert nn_mod.BATCH_SIZE == 64 and nn_mod.MAX_EPOCHS == 100 and nn_mod.PATIENCE == 10
    assert nn_mod.INNER_VAL_FRAC == 0.20


# ---------------------------------------------------------------- build_sequences (pj-063, pj-067)

def _cdm(rows):
    """rows: (event_id, time_to_tca, risk, miss_distance, relative_speed, t_weighted_rms, type)."""
    df = pd.DataFrame(rows, columns=["event_id", "time_to_tca", "risk", "miss_distance",
                                     "relative_speed", "t_weighted_rms", "c_object_type"])
    return df.astype({"event_id": "int64", "time_to_tca": "float64", "risk": "float64",
                      "miss_distance": "float64", "relative_speed": "float64",
                      "t_weighted_rms": "float64"})


def _toy_cdm():
    rows = [
        # event 7: usable ttc 6, 4, 2.5; ttc 1.0 is unusable and has another type + extreme risk
        (7, 4.0, -12.0, 400.0, 11000.0, 0.4, "DEBRIS"),
        (7, 1.0, -3.0, 10.0, 11000.0, 0.1, "PAYLOAD"),
        (7, 6.0, -14.0, 900.0, 11000.0, 0.6, "PAYLOAD"),
        (7, 2.5, -10.0, np.nan, 11000.0, 0.3, "DEBRIS"),
        # event 3: single usable CDM, type outside OBJECT_TYPES
        (3, 3.0, -20.0, 5000.0, 9000.0, 1.0, "WEIRD"),
        (3, 0.5, -5.0, 50.0, 9000.0, 0.1, "DEBRIS"),
    ]
    return _cdm(rows)


def test_build_sequences_shape_dtype_and_input_order():
    seq, mask = build_sequences(np.array([3, 7]), _toy_cdm())
    assert seq.shape == (2, 20, C) and seq.dtype == np.float64
    assert mask.shape == (2, 20) and mask.dtype == np.bool_
    assert mask.sum(axis=1).tolist() == [1, 3]  # row 0 is event 3, row 1 is event 7
    seq2, mask2 = build_sequences(np.array([7, 3]), _toy_cdm())
    np.testing.assert_array_equal(seq2[0], seq[1])
    np.testing.assert_array_equal(mask2[1], mask[0])


def test_build_sequences_chronological_left_aligned_and_ttc_filter():
    seq, mask = build_sequences(np.array([7]), _toy_cdm())
    assert mask[0].tolist() == [True] * 3 + [False] * 17
    ttc = seq[0, :3, NUM.index("time_to_tca")]
    assert ttc.tolist() == [6.0, 4.0, 2.5]  # descending ttc; last valid = closest usable to TCA
    assert seq[0, :3, 0].tolist() == [-14.0, -12.0, -10.0]
    assert seq[0, :3, 1].tolist()[:2] == [900.0, 400.0]
    assert np.isnan(seq[0, 2, 1])  # NaN kept on valid steps
    assert not np.any(seq[0, :, 0] == -3.0)  # ttc 1.0 < TTC_MIN never enters


def test_build_sequences_custom_ttc_min():
    seq, mask = build_sequences(np.array([7]), _toy_cdm(), ttc_min=4.0)
    assert mask[0].sum() == 2
    assert seq[0, :2, NUM.index("time_to_tca")].tolist() == [6.0, 4.0]


def test_build_sequences_one_hot_from_closest_usable_cdm_on_valid_steps_only():
    seq, mask = build_sequences(np.array([7, 3]), _toy_cdm())
    oh = seq[0, :, 5:]
    expected = np.zeros(5)
    expected[OBJECT_TYPES.index("DEBRIS")] = 1.0  # ttc 2.5 is DEBRIS; ttc 1.0 PAYLOAD is unusable
    np.testing.assert_array_equal(oh[:3], np.tile(expected, (3, 1)))
    np.testing.assert_array_equal(oh[3:], 0.0)
    np.testing.assert_array_equal(seq[1, :, 5:], 0.0)  # type not in OBJECT_TYPES -> all zero


def test_build_sequences_padding_is_zero():
    seq, mask = build_sequences(np.array([3, 7]), _toy_cdm())
    assert np.all(seq[~mask] == 0.0)
    assert not np.isnan(seq[~mask]).any()


def test_build_sequences_truncates_to_closest_to_tca():
    ttcs = np.arange(2.0, 27.0)  # 25 usable CDMs, ttc 2..26
    rows = [(1, t, -t, 100.0 * t, 1.0, 0.1, "TBA") for t in ttcs[::-1].tolist()[::2]]
    rows += [(1, t, -t, 100.0 * t, 1.0, 0.1, "TBA") for t in ttcs[::-1].tolist()[1::2]]
    seq, mask = build_sequences(np.array([1]), _cdm(rows))
    assert mask.all()
    np.testing.assert_array_equal(seq[0, :, 4], np.arange(21.0, 1.0, -1.0))
    seq3, mask3 = build_sequences(np.array([1]), _cdm(rows), T=3)
    assert seq3.shape == (1, 3, C) and mask3.all()
    assert seq3[0, :, 4].tolist() == [4.0, 3.0, 2.0]


def test_build_sequences_raises_without_usable_cdm():
    cdm = _toy_cdm()
    with pytest.raises(ValueError):
        build_sequences(np.array([7, 99]), cdm)  # 99 absent
    only_late = _cdm([(5, 1.0, -5.0, 1.0, 1.0, 1.0, "DEBRIS")])
    with pytest.raises(ValueError):
        build_sequences(np.array([5]), only_late)


# ---------------------------------------------------------------- SequencePreprocessor (pj-065)

def _seq_small():
    seq = np.zeros((2, 4, C))
    mask = np.array([[True, True, True, False], [True, False, False, False]])
    seq[0, :3, 0] = [1.0, 3.0, np.nan]
    seq[1, 0, 0] = 5.0
    seq[0, :3, 1] = [2.0, 2.0, 2.0]
    seq[1, 0, 1] = 2.0  # constant channel -> std 0 -> treated as 1
    seq[0, :3, 4] = [3.0, 2.0, 1.0]
    seq[1, 0, 4] = 2.0
    seq[0, :3, 5] = 1.0  # DEBRIS one-hot
    seq[1, 0, 7] = 1.0  # PAYLOAD one-hot
    return seq, mask


def test_seq_preproc_median_impute_then_standardize_valid_steps():
    seq, mask = _seq_small()
    z = SequencePreprocessor().fit(seq, mask).transform(seq, mask)
    assert z.shape == seq.shape and z.dtype == np.float64
    # channel 0 valid = [1, 3, NaN, 5] -> median 3 -> [1, 3, 3, 5], mean 3, std sqrt(2) (ddof=0)
    s = np.sqrt(2.0)
    np.testing.assert_allclose(z[0, :3, 0], [-2 / s, 0.0, 0.0])
    np.testing.assert_allclose(z[1, 0, 0], 2 / s)
    np.testing.assert_allclose(z[mask][:, 1], 0.0)  # constant channel: (x - mean) / 1
    np.testing.assert_allclose(z[mask][:, 4], np.array([1.0, 0.0, -1.0, 0.0]) / np.sqrt(0.5))
    np.testing.assert_array_equal(z[..., 5:], seq[..., 5:])  # one-hots untouched
    assert np.all(z[~mask] == 0.0) and not np.isnan(z).any()


def test_seq_preproc_ignores_padded_slots_when_fitting():
    seq, mask = _seq_small()
    dirty = seq.copy()
    dirty[~mask] = 1e6
    dirty[0, 3, 0] = np.nan
    a = SequencePreprocessor().fit(seq, mask)
    b = SequencePreprocessor().fit(dirty, mask)
    np.testing.assert_allclose(a.transform(seq, mask), b.transform(seq, mask))
    # garbage in padded slots at transform time is also zeroed
    np.testing.assert_allclose(a.transform(dirty, mask), a.transform(seq, mask))


def test_seq_preproc_transform_uses_fit_stats_only():
    seq, mask = _seq_small()
    pre = SequencePreprocessor().fit(seq, mask)
    other = np.zeros((1, 4, C))
    m2 = np.array([[True, True, False, False]])
    other[0, :2, 0] = [100.0, np.nan]
    other[0, :2, 4] = [50.0, 7.0]
    z = pre.transform(other, m2)
    s = np.sqrt(2.0)
    np.testing.assert_allclose(z[0, :2, 0], [(100.0 - 3.0) / s, 0.0])  # NaN -> fit median 3
    np.testing.assert_allclose(z[0, :2, 4], (np.array([50.0, 7.0]) - 2.0) / np.sqrt(0.5))
    # fitting on the other set would give different statistics
    z_self = SequencePreprocessor().fit(other, m2).transform(other, m2)
    assert not np.allclose(z_self[0, :2, 0], z[0, :2, 0])


# ---------------------------------------------------------------- networks (pj-064, pj-067)

def test_mlp_layer_shapes_no_dropout_and_output_shape():
    torch.manual_seed(0)
    m = MLP(35)
    lins = [mod for mod in m.modules() if isinstance(mod, torch.nn.Linear)]
    assert [tuple(l.weight.shape) for l in lins] == [(128, 35), (64, 128), (1, 64)]
    assert all(l.bias is not None for l in lins)
    assert sum(isinstance(mod, torch.nn.ReLU) for mod in m.modules()) == 2
    assert not any(isinstance(mod, torch.nn.Dropout) for mod in m.modules())
    out = m(torch.randn(7, 35))
    assert out.shape == (7,)


def test_masked_gru_structure():
    g = MaskedGRU(C)
    assert isinstance(g.gru, torch.nn.GRU)
    assert g.gru.input_size == C and g.gru.hidden_size == 64 and g.gru.num_layers == 1
    assert g.gru.batch_first and g.gru.dropout == 0
    assert isinstance(g.head, torch.nn.Linear)
    assert (g.head.in_features, g.head.out_features) == (64, 1)


def _gru_reference(g, x, lengths):
    out = []
    with torch.no_grad():
        for i, L in enumerate(lengths):
            h, _ = g.gru(x[i:i + 1, :L])
            out.append(g.head(h[0, -1]).reshape(()))
    return torch.stack(out)


def test_masked_gru_uses_last_valid_state_with_mixed_lengths():
    torch.manual_seed(1)
    g = MaskedGRU(C).eval()
    lengths = [1, 5, 20, 3]
    x = torch.randn(4, 20, C)
    mask = torch.zeros(4, 20, dtype=torch.bool)
    for i, L in enumerate(lengths):
        mask[i, :L] = True
        x[i, L:] = 0.0
    with torch.no_grad():
        y = g(x, mask)
    assert y.shape == (4,)
    torch.testing.assert_close(y, _gru_reference(g, x, lengths), rtol=1e-5, atol=1e-6)


def test_masked_gru_ignores_padded_values_but_not_last_valid_step():
    torch.manual_seed(2)
    g = MaskedGRU(C).eval()
    x = torch.randn(2, 20, C)
    mask = torch.zeros(2, 20, dtype=torch.bool)
    mask[0, :4] = True
    mask[1, :9] = True
    with torch.no_grad():
        base = g(x, mask)
        x2 = x.clone()
        x2[0, 4:] = 1e3
        x2[1, 9:] = -1e3
        torch.testing.assert_close(g(x2, mask), base)
        x3 = x.clone()
        x3[0, 3] += 5.0  # last valid step of row 0
        moved = g(x3, mask)
    assert abs(float(moved[0] - base[0])) > 1e-4
    torch.testing.assert_close(moved[1], base[1])


# ---------------------------------------------------------------- seeds, inner split (pj-066, pj-069)

def test_seed_everything_seeds_all_rngs():
    seed_everything(43)
    a = (random.random(), np.random.rand(), torch.rand(1).item())
    seed_everything(43)
    b = (random.random(), np.random.rand(), torch.rand(1).item())
    assert a == b
    seed_everything(44)
    c = (random.random(), np.random.rand(), torch.rand(1).item())
    assert all(x != y for x, y in zip(a, c))


@pytest.mark.parametrize("n", [10, 37, 81])
def test_inner_split_partition_and_size(n):
    fit, es = inner_split(n, 42, 0)
    assert len(es) == round(0.2 * n)
    assert len(np.intersect1d(fit, es)) == 0
    assert np.array_equal(np.sort(np.concatenate([fit, es])), np.arange(n))


def test_inner_split_deterministic_and_varies_with_fold_and_seed():
    a = inner_split(80, 42, 1)
    b = inner_split(80, 42, 1)
    np.testing.assert_array_equal(a[1], b[1])
    np.testing.assert_array_equal(a[0], b[0])
    other_fold = inner_split(80, 42, 2)[1]
    other_seed = inner_split(80, 43, 1)[1]
    assert set(other_fold.tolist()) != set(a[1].tolist())
    assert set(other_seed.tolist()) != set(a[1].tolist())
    # shuffled, not a contiguous block of indices
    assert set(a[1].tolist()) != set(range(64, 80)) and set(a[1].tolist()) != set(range(16))


# ---------------------------------------------------------------- train_net (pj-066, pj-074, pj-076)

def _es_mse(model, inputs, y, w=None):
    """(Weighted) mean squared error of `model` on `inputs`: sum w*e^2 / sum w (pj-074, pj-076)."""
    with torch.no_grad():
        t = [torch.as_tensor(a) for a in inputs]
        t = [a.float() if a.dtype.is_floating_point else a for a in t]
        pred = model(*t).double().numpy()
    w = np.ones(len(y)) if w is None else np.asarray(w, dtype=np.float64)
    return float(np.sum(w * (pred - y) ** 2) / np.sum(w))


def _ones(y_fit, y_es):
    return {"w_fit": np.ones(len(y_fit)), "w_es": np.ones(len(y_es))}


def _train_plain_mse_reference(model, inputs_fit, y_fit, inputs_es, y_es, *, seed):
    """Iteration-1 train_net (pj-066) verbatim: unweighted MSE loss and monitor."""
    def tens(inputs):
        return [torch.as_tensor(a).float() if np.issubdtype(np.asarray(a).dtype, np.floating)
                else torch.as_tensor(a) for a in inputs]

    def pred(m, t):
        m.eval()
        with torch.no_grad():
            return m(*t).double().numpy()

    xf, xe = tens(inputs_fit), tens(inputs_es)
    yf = torch.as_tensor(np.asarray(y_fit, dtype=np.float64)).float()
    y_es = np.asarray(y_es, dtype=np.float64)
    opt = torch.optim.Adam(model.parameters(), lr=nn_mod.LR, betas=nn_mod.BETAS, eps=nn_mod.EPS,
                           weight_decay=nn_mod.WEIGHT_DECAY)
    gen = torch.Generator().manual_seed(seed)
    n = len(yf)
    best, best_epoch, best_state, epochs_run = np.inf, 0, None, 0
    for epoch in range(1, nn_mod.MAX_EPOCHS + 1):
        model.train()
        perm = torch.randperm(n, generator=gen)
        for i in range(0, n, nn_mod.BATCH_SIZE):
            b = perm[i:i + nn_mod.BATCH_SIZE]
            opt.zero_grad()
            loss = torch.nn.functional.mse_loss(model(*[x[b] for x in xf]), yf[b])
            loss.backward()
            opt.step()
        epochs_run = epoch
        es_loss = float(np.mean((pred(model, xe) - y_es) ** 2))
        if es_loss < best:
            best, best_epoch, best_state = es_loss, epoch, copy.deepcopy(model.state_dict())
        elif epoch - best_epoch >= nn_mod.PATIENCE:
            break
    model.load_state_dict(best_state)
    model.eval()
    return model, {"best_epoch": best_epoch, "epochs_run": epochs_run, "best_es_loss": best}


def test_train_net_learns_simple_target_with_real_constants():
    # real MAX_EPOCHS / PATIENCE / BATCH_SIZE on a tiny linear problem (cap 100 per pj-074)
    rng = np.random.default_rng(0)
    X = rng.normal(size=(160, 3))
    y = 2.0 * X[:, 0] - X[:, 1] + 1.0
    seed_everything(42)
    model, info = train_net(MLP(3), (X[:128],), y[:128], (X[128:],), y[128:], seed=42,
                            **_ones(y[:128], y[128:]))
    assert {"best_epoch", "epochs_run", "best_es_loss"} <= set(info)
    assert 1 <= info["best_epoch"] <= info["epochs_run"] <= 100
    assert info["epochs_run"] <= info["best_epoch"] + 10
    assert not model.training
    mse = _es_mse(model, (X[128:],), y[128:])
    assert mse < 0.05 * np.var(y[128:])
    assert mse == pytest.approx(info["best_es_loss"], rel=1e-4, abs=1e-6)


def test_train_net_early_stops_and_restores_best_weights(monkeypatch):
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 300)
    monkeypatch.setattr(nn_mod, "PATIENCE", 3)
    rng = np.random.default_rng(1)
    X = rng.normal(size=(100, 20))
    y_fit = rng.normal(size=80)  # pure noise: memorising it worsens the es loss
    y_es = rng.normal(size=20)
    seed_everything(42)
    model, info = train_net(MLP(20), (X[:80],), y_fit, (X[80:],), y_es, seed=42, **_ones(y_fit, y_es))
    assert info["epochs_run"] < 300
    assert info["epochs_run"] == info["best_epoch"] + 3  # stopped by patience, not by the cap
    # weights after the last epoch were worse; the returned model must be the best one
    assert _es_mse(model, (X[80:],), y_es) == pytest.approx(info["best_es_loss"], rel=1e-4)


def test_train_net_respects_max_epochs(monkeypatch):
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 2)
    monkeypatch.setattr(nn_mod, "PATIENCE", 100)
    rng = np.random.default_rng(2)
    X = rng.normal(size=(50, 4))
    y = X[:, 0]
    _, info = train_net(MLP(4), (X[:40],), y[:40], (X[40:],), y[40:], seed=1, **_ones(y[:40], y[40:]))
    assert info["epochs_run"] == 2


def _spy_adam(monkeypatch, on_step=None):
    made = []
    real_adam = torch.optim.Adam

    class SpyAdam(real_adam):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            made.append(self)

        def step(self, *a, **k):
            if on_step is not None:
                on_step(self)
            return super().step(*a, **k)

    monkeypatch.setattr(torch.optim, "Adam", SpyAdam)
    monkeypatch.setattr(nn_mod, "Adam", SpyAdam, raising=False)
    return made


def test_train_net_adam_hyperparameters(monkeypatch):
    made = _spy_adam(monkeypatch)
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 1)
    rng = np.random.default_rng(3)
    X = rng.normal(size=(30, 4))
    model = MLP(4)
    train_net(model, (X[:24],), X[:24, 0], (X[24:],), X[24:, 0], seed=0, **_ones(X[:24], X[24:]))
    assert len(made) == 1
    d = made[0].defaults
    assert d["lr"] == 1e-3 and tuple(d["betas"]) == (0.9, 0.999)
    assert d["eps"] == 1e-8 and d["weight_decay"] == 0.0
    opt_params = {id(p) for g in made[0].param_groups for p in g["params"]}
    assert opt_params == {id(p) for p in model.parameters()}


def test_train_net_handles_sequence_inputs():
    rng = np.random.default_rng(4)
    seq, mask = _random_seq(40, rng)
    seq = np.nan_to_num(seq)  # train_net receives already-preprocessed (NaN-free) inputs
    y = seq[:, 0, 0]
    _, info = train_net(MaskedGRU(C), (seq[:32], mask[:32]), y[:32], (seq[32:], mask[32:]), y[32:],
                        seed=0, **_ones(y[:32], y[32:]))
    assert np.isfinite(info["best_es_loss"])


def test_train_net_unit_weights_equal_iteration1_plain_mse(monkeypatch):
    # pj-076: with all weights 1 the loss is the plain MSE of iteration 1, so the whole
    # trajectory (early stopping included) matches the iteration-1 loop; pj-074: fits that
    # stopped before the old cap reproduce the same stop with w = 1.
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 8)
    monkeypatch.setattr(nn_mod, "PATIENCE", 3)
    rng = np.random.default_rng(7)
    X = rng.normal(size=(170, 6))
    y = X[:, 0] - 0.5 * X[:, 1] ** 2 + 0.3 * rng.normal(size=170)
    a = (X[:140],), y[:140], (X[140:],), y[140:]
    seed_everything(42)
    ref, ref_info = _train_plain_mse_reference(MLP(6), *a, seed=42)
    seed_everything(42)
    m1, i1 = train_net(MLP(6), *a, seed=42, **_ones(y[:140], y[140:]))
    seed_everything(42)
    m2, i2 = train_net(MLP(6), *a, seed=42, **_ones(y[:140], y[140:]))
    probe = torch.as_tensor(X).float()
    with torch.no_grad():
        p_ref, p1, p2 = (m(probe).double().numpy() for m in (ref, m1, m2))
    # same call twice: bit-identical
    np.testing.assert_array_equal(p1, p2)
    assert i1 == i2
    # versus the iteration-1 loop: identical epochs, same model up to float32 round-off
    assert (i1["best_epoch"], i1["epochs_run"]) == (ref_info["best_epoch"], ref_info["epochs_run"])
    assert i1["best_es_loss"] == pytest.approx(ref_info["best_es_loss"], rel=1e-5)
    np.testing.assert_allclose(p1, p_ref, rtol=1e-5, atol=1e-6)


def test_train_net_batch_loss_is_weighted_mean_not_sum_over_batch(monkeypatch):
    # pj-076 option A: L = sum w*l / sum w. A single mini-batch (n_fit < BATCH_SIZE) lets the
    # first optimizer step's gradients be compared to the gradient of the expected loss
    # computed on a copy of the initial model. Option B (sum w*l / B) would give gradients
    # scaled by mean(w) = 3 here.
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 1)
    rng = np.random.default_rng(11)
    X = rng.normal(size=(50, 4))
    y = X[:, 0] + rng.normal(size=50)
    w_fit = np.where(np.arange(40) % 2 == 0, 1.0, 5.0)
    assert w_fit.mean() == 3.0
    grads = []

    def on_step(opt):
        if not grads:
            grads.append([p.grad.detach().clone() for g in opt.param_groups for p in g["params"]])

    _spy_adam(monkeypatch, on_step)
    torch.manual_seed(0)
    model = MLP(4)
    init = copy.deepcopy(model)
    train_net(model, (X[:40],), y[:40], (X[40:],), y[40:], seed=0, w_fit=w_fit, w_es=np.ones(10))
    assert len(grads) == 1
    xt, yt, wt = (torch.as_tensor(a).float() for a in (X[:40], y[:40], w_fit))
    init.train()
    init.zero_grad()
    pred = init(xt)
    ((wt * (pred - yt) ** 2).sum() / wt.sum()).backward()
    expected = [p.grad for p in init.parameters()]
    assert len(expected) == len(grads[0])
    for g, e in zip(grads[0], expected):
        torch.testing.assert_close(g, e, rtol=1e-4, atol=1e-6)


def test_train_net_early_stopping_monitor_is_weighted_mse(monkeypatch):
    # pj-074: the monitor is sum w_es*e^2 / sum w_es. Training is identical in both runs (same
    # seed, same w_fit, no early stop), so the runs see the same sequence of epoch models and
    # differ only in which one the monitor keeps.
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 30)
    monkeypatch.setattr(nn_mod, "PATIENCE", 1000)
    rng = np.random.default_rng(1)
    X = rng.normal(size=(100, 20))
    y_fit = rng.normal(size=80)
    y_es = rng.normal(size=20)
    w_es = np.ones(20)
    w_es[:3] = 20.0
    runs = {}
    for name, we in (("plain", np.ones(20)), ("weighted", w_es)):
        seed_everything(42)
        runs[name] = train_net(MLP(20), (X[:80],), y_fit, (X[80:],), y_es, seed=42,
                               w_fit=np.ones(80), w_es=we)
    (mp, ip), (mw, iw) = runs["plain"], runs["weighted"]
    assert ip["epochs_run"] == iw["epochs_run"] == 30
    assert ip["best_epoch"] != iw["best_epoch"]  # the two monitors disagree on this data
    xe = (X[80:],)
    # reported best_es_loss is the monitor value of the restored model
    assert iw["best_es_loss"] == pytest.approx(_es_mse(mw, xe, y_es, w_es), rel=1e-4)
    assert ip["best_es_loss"] == pytest.approx(_es_mse(mp, xe, y_es), rel=1e-4)
    # each run keeps the epoch that is best under its own monitor
    assert _es_mse(mw, xe, y_es, w_es) < _es_mse(mp, xe, y_es, w_es)
    assert _es_mse(mp, xe, y_es) < _es_mse(mw, xe, y_es)


def test_train_net_hr_weights_pull_the_fit_toward_weighted_points(monkeypatch):
    # Every input appears twice, once with target 0 and once with target 4. The weighted-mean
    # optimum is 4*w/(w+1): 2 unweighted, 3.6 with w = 9 on the target-4 copies.
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 50)
    monkeypatch.setattr(nn_mod, "PATIENCE", 10)
    rng = np.random.default_rng(5)
    X = rng.normal(size=(60, 2))
    Xd = np.vstack([X, X])
    yd = np.r_[np.zeros(60), np.full(60, 4.0)]
    wd = np.r_[np.ones(60), np.full(60, 9.0)]
    means = {}
    for name, w in (("plain", np.ones(120)), ("weighted", wd)):
        seed_everything(0)
        m, _ = train_net(MLP(2), (Xd,), yd, (Xd,), yd, seed=0, w_fit=w, w_es=w)
        with torch.no_grad():
            means[name] = float(m(torch.as_tensor(X).float()).mean())
    assert 1.5 < means["plain"] < 2.5
    assert means["weighted"] > 3.0


# ---------------------------------------------------------------- run_neural_cv (pj-062, pj-065, pj-068, pj-072, pj-073)

def _random_seq(n, rng):
    lengths = rng.integers(1, 21, n)
    seq = np.zeros((n, 20, C))
    mask = np.zeros((n, 20), dtype=bool)
    for i, L in enumerate(lengths):
        mask[i, :L] = True
        seq[i, :L, :4] = rng.normal(size=(L, 4))
        seq[i, :L, 4] = np.arange(L, 0, -1) + 1.0
        seq[i, :L, 5 + rng.integers(0, 5)] = 1.0
        if L > 1 and rng.random() < 0.2:
            seq[i, L - 1, 1] = np.nan
    return seq, mask


def _cv_data(n=100, seed=0):
    """y realistic for pj-026: mostly far below -6, a near-threshold band, ~15% HR."""
    rng = np.random.default_rng(seed)
    u = rng.random(n)
    y = rng.uniform(-30.0, -10.0, n)
    hr = u < 0.15
    near = (u >= 0.15) & (u < 0.45)
    y[hr] = rng.uniform(-6.0, -4.0, hr.sum())
    y[near] = rng.uniform(-6.5, -6.01, near.sum())
    lrp = np.full(n, -30.0)
    lrp[hr] = y[hr]  # LRP detects every HR event -> f_star > 0 in any subset holding an HR event
    fa = ~hr & (rng.random(n) < 0.05)
    lrp[fa] = -5.0
    X = np.hstack([rng.normal(size=(n, 30)), np.eye(5)[rng.integers(0, 5, n)]])
    X[:, 0] += 0.1 * y
    X[rng.random(n) < 0.1, 3] = np.nan
    seq, mask = _random_seq(n, rng)
    eid = np.arange(n, dtype=np.int64)
    table = pd.DataFrame({"event_id": eid, "y_hr": y >= -6.0})
    return X, (seq, mask), y, lrp, eid, table


def _dup_rep_folds(table):
    """Two reps with the same fold assignment (rep 1 differs only by its seed)."""
    f1 = make_folds(table, seeds=(42,), n_splits=5)
    return pd.concat([f1, f1.assign(rep=1, seed=43)], ignore_index=True)


@pytest.fixture
def fast(monkeypatch):
    monkeypatch.setattr(nn_mod, "MAX_EPOCHS", 3)
    monkeypatch.setattr(nn_mod, "PATIENCE", 2)


@pytest.fixture
def grid2(monkeypatch):
    # neural reads trees.W_GRID at call time; raising=False so a missing grid shows up as a
    # failing test body, not a fixture error
    monkeypatch.setattr(trees_mod, "W_GRID", (1, 2), raising=False)
    return (1, 2)


@pytest.fixture
def grid1(monkeypatch):
    monkeypatch.setattr(trees_mod, "W_GRID", (1,), raising=False)
    return (1,)


def _inputs(arm, X, sm):
    return (X,) if arm == "mlp" else sm


def _parts(folds, r, k):
    fold = folds[folds.rep == r].fold.to_numpy()
    return np.flatnonzero(fold == k), np.flatnonzero(fold != k)


def _floor_solvable(y, lrp, w):
    """Independent check that the pj-072 equation q(c) = p*_w has a root in [-29.99, -6.0005]."""
    hr = y >= -6.0
    if hr.sum() < 2:
        return False
    p_star = f2_score(y, lrp) / 5.0
    pw = w * p_star / (w * p_star + 1.0 - p_star)
    mu = y[hr].mean()

    def q(c):
        m = np.maximum(y[~hr], c).mean()
        return (-6.0 - m) / (mu - m)

    return (q(-29.99) - pw) * (q(-6.0005) - pw) < 0


@pytest.mark.parametrize("n,dseed,layout", [(100, 0, "two"), (80, 1, "two"), (80, 2, "dup")])
def test_synthetic_cv_data_gives_floor_root_for_any_inner_fit_part(n, dseed, layout):
    # guards the fixtures: the floor must be solvable for w in {1, 2} on every 80% fitting part
    # used below — outer refits and (3-fold stratified) inner fits alike
    X, sm, y, lrp, eid, table = _cv_data(n, seed=dseed)
    folds = make_folds(table, seeds=(42, 43), n_splits=5) if layout == "two" else _dup_rep_folds(table)
    for r in (0, 1):
        s = 42 + r
        for k in range(5):
            _, tr = _parts(folds, r, k)
            parts = [tr]
            skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=s)
            parts += [tr[i] for i, _ in skf.split(np.zeros(len(tr)), y[tr] >= -6.0)]
            for part in parts:
                fit, _ = inner_split(len(part), s, k)
                for w in (1, 2):
                    assert _floor_solvable(y[part[fit]], lrp[part[fit]], w)


@pytest.mark.parametrize("arm", ["mlp", "gru"])
def test_run_neural_cv_structure(arm, fast, grid2):
    X, sm, y, lrp, eid, table = _cv_data()
    folds = make_folds(table, seeds=(42, 43), n_splits=5)
    res = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    n = len(y)
    assert res.oof_pred.shape == (2, n) and not np.isnan(res.oof_pred).any()
    assert res.importances.shape == (0,)
    assert len(res.metrics_per_rep) == 2
    assert res.metrics["F2"] == pytest.approx(np.mean([m["F2"] for m in res.metrics_per_rep]))
    assert {"F2", "MSE_HR_clipped", "L_unclipped"} <= set(res.metrics_pooled)
    pf = pd.concat(res.fold_frames, ignore_index=True)
    assert list(pf.columns) == ["event_id", "rep", "fold", "r_hat", "p_hr"]
    np.testing.assert_array_equal(pf.p_hr.to_numpy(), (pf.r_hat.to_numpy() >= -6.0).astype(float))
    for r in (0, 1):
        pr = pf[pf.rep == r]
        assert sorted(pr.event_id.tolist()) == eid.tolist()  # each event exactly once per rep
        ref = folds[folds.rep == r].set_index("event_id").fold
        assert (pr.set_index("event_id").fold == ref.loc[pr.event_id].to_numpy()).all()
        np.testing.assert_allclose(res.oof_pred[r][pr.event_id.to_numpy()], pr.r_hat.to_numpy())
    assert [(f["rep"], f["fold"]) for f in res.floors] == [(r, k) for r in (0, 1) for k in range(5)]
    for f in res.floors:
        assert {"c", "mu_hr", "sd_hr", "f_star", "p_star", "w", "inner_L",
                "best_epoch", "epochs_run", "best_es_loss"} <= set(f)
        assert 1 <= f["best_epoch"] <= f["epochs_run"] <= 3
        assert f["w"] in grid2
        assert set(f["inner_L"]) == {f"{w}|0" for w in grid2}


def test_run_neural_cv_rejects_unknown_arm():
    X, sm, y, lrp, eid, table = _cv_data(60)
    folds = make_folds(table, seeds=(42,), n_splits=5)
    with pytest.raises(ValueError):
        run_neural_cv("lstm", (X,), y, lrp, eid, folds)


def _instrument(monkeypatch):
    """Spy on trees.select_by_inner_cv (and the fit_predict it receives) and on train_net.

    Returns a list of per-outer-fold groups: {"select": rec, "refits": [train calls made
    outside fit_predict after that selection]}. Each select rec holds its fit_predict calls
    ("fps"), each with the train_net calls made inside it.
    """
    events = []
    state = {"fp": None}
    real_train = nn_mod.train_net
    sig = inspect.signature(real_train)
    real_select = trees_mod.select_by_inner_cv

    def train_spy(*a, **k):
        call = dict(sig.bind(*a, **k).arguments)
        model, info = real_train(*a, **k)
        call.update(model=model, info=dict(info))
        if state["fp"] is not None:
            state["fp"]["trains"].append(call)
        else:
            events.append(("refit", call))
        return model, info

    def select_spy(fit_predict, *a, **k):
        rec = {"args": a, "kwargs": k, "fps": []}
        events.append(("select", rec))

        def fp(fit_idx, pred_idx, w):
            frec = {"fit_idx": np.asarray(fit_idx).copy(), "pred_idx": np.asarray(pred_idx).copy(),
                    "w": w, "trains": []}
            rec["fps"].append(frec)
            state["fp"] = frec
            try:
                out = fit_predict(fit_idx, pred_idx, w)
            finally:
                state["fp"] = None
            frec["out"] = out
            return out

        return real_select(fp, *a, **k)

    monkeypatch.setattr(nn_mod, "train_net", train_spy)
    monkeypatch.setattr(trees_mod, "select_by_inner_cv", select_spy)

    def groups():
        out = []
        for kind, rec in events:
            if kind == "select":
                out.append({"select": rec, "refits": []})
            else:
                assert out, "train_net called before any w selection"
                out[-1]["refits"].append(rec)
        return out

    return groups


def _check_fit_es(arm, call, X, sm, y, fit_rows, es_rows, c, w):
    """Inputs standardized with stats of `fit_rows` only, es transformed with them; targets
    are max(y, c) and weights hr_weights(y, w) on both parts, paired row by row."""
    y_fit, y_es = np.asarray(call["y_fit"], dtype=float), np.asarray(call["y_es"], dtype=float)
    w_fit, w_es = np.asarray(call["w_fit"], dtype=float), np.asarray(call["w_es"], dtype=float)
    assert len(w_fit) == len(y_fit) == len(fit_rows) and len(w_es) == len(y_es) == len(es_rows)
    if arm == "mlp":
        zf, ze = np.asarray(call["inputs_fit"][0]), np.asarray(call["inputs_es"][0])
        assert not np.isnan(zf).any() and not np.isnan(ze).any()
        np.testing.assert_allclose(zf[:, :30].mean(axis=0), 0.0, atol=1e-9)
        np.testing.assert_allclose(zf[:, :30].std(axis=0), 1.0, atol=1e-9)
        np.testing.assert_array_equal(np.sort(zf[:, 30:], axis=0), np.sort(X[fit_rows, 30:], axis=0))
        raw_f, raw_e = X[fit_rows, 0], X[es_rows, 0]
        col_f, col_e = zf[:, 0], ze[:, 0]
        mu, sd = raw_f.mean(), raw_f.std()
    else:
        (sf, mf), (se, me) = call["inputs_fit"], call["inputs_es"]
        sf, mf, se, me = map(np.asarray, (sf, mf, se, me))
        assert not np.isnan(sf).any() and not np.isnan(se).any()
        v = sf[mf][:, :5]
        np.testing.assert_allclose(v.mean(axis=0), 0.0, atol=1e-9)
        np.testing.assert_allclose(v.std(axis=0), 1.0, atol=1e-9)
        seq, mask = sm
        vf = seq[fit_rows][mask[fit_rows]][:, 0]
        raw_f, raw_e = seq[fit_rows, 0, 0], seq[es_rows, 0, 0]
        col_f, col_e = sf[:, 0, 0], se[:, 0, 0]
        mu, sd = vf.mean(), vf.std()
    # undo the fit-part scaling: (raw value, floored target, weight) triples must match exactly
    for col, raw, rows, yt, wt in ((col_f, raw_f, fit_rows, y_fit, w_fit), (col_e, raw_e, es_rows, y_es, w_es)):
        rec = col * sd + mu
        assert len(rec) == len(rows)
        g, e = np.argsort(rec), np.argsort(raw)  # raw values are distinct continuous draws
        np.testing.assert_allclose(rec[g], raw[e], rtol=0, atol=1e-8)
        np.testing.assert_allclose(yt[g], np.maximum(y[rows], c)[e], rtol=0, atol=1e-12)
        np.testing.assert_array_equal(wt[g], np.where(y[rows] >= -6.0, float(w), 1.0)[e])


def _predict_val(arm, model, X, sm, fit_rows, val):
    if arm == "mlp":
        z = (make_preprocessor().fit(X[fit_rows]).transform(X[val]),)
    else:
        seq, mask = sm
        z = (SequencePreprocessor().fit(seq[fit_rows], mask[fit_rows]).transform(seq[val], mask[val]),
             mask[val])
    t = [torch.as_tensor(a).float() if np.issubdtype(a.dtype, np.floating) else torch.as_tensor(a)
         for a in z]
    model.eval()
    with torch.no_grad():
        return model(*t).double().numpy()


@pytest.mark.parametrize("arm", ["mlp", "gru"])
def test_run_neural_cv_nested_selection_of_w(arm, fast, grid2, monkeypatch):
    # pj-073: per outer fold, 3 inner folds x len(W_GRID) fits on the outer training part only,
    # then one refit on the whole training part with the chosen w; pj-072: floor c(w) and HR
    # weights computed on each 80% fitting part; pj-065: preprocessing fit there only.
    X, sm, y, lrp, eid, table = _cv_data()
    folds = make_folds(table, seeds=(42,), n_splits=5)
    groups = _instrument(monkeypatch)
    res = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    gs = groups()
    assert len(gs) == 5
    assert sum(len(g["refits"]) + sum(len(f["trains"]) for f in g["select"]["fps"]) for g in gs) \
        == 5 * (len(grid2) * 3 + 1)
    for k, g in enumerate(gs):
        val, tr = _parts(folds, 0, k)
        sel = g["select"]
        grid_arg, tr_arg, y_arg = sel["args"][:3]
        seed_arg = sel["kwargs"]["seed"] if "seed" in sel["kwargs"] else sel["args"][3]
        assert tuple(grid_arg) == grid2 and seed_arg == 42
        np.testing.assert_array_equal(np.sort(np.asarray(tr_arg)), tr)
        np.testing.assert_array_equal(np.asarray(y_arg, dtype=float), y)  # raw y; flooring is per fit
        fps = sel["fps"]
        assert sorted(f["w"] for f in fps) == sorted(list(grid2) * 3)
        for w in grid2:
            held = np.concatenate([f["pred_idx"] for f in fps if f["w"] == w])
            np.testing.assert_array_equal(np.sort(held), tr)  # 3 disjoint held-out parts cover tr
        for f in fps:
            fit_idx, pred_idx, w = f["fit_idx"], f["pred_idx"], f["w"]
            assert not np.intersect1d(fit_idx, val).size and not np.intersect1d(pred_idx, val).size
            assert not np.intersect1d(fit_idx, pred_idx).size
            np.testing.assert_array_equal(np.sort(np.concatenate([fit_idx, pred_idx])), tr)
            assert len(f["trains"]) == 1  # one network per inner fit
            call = f["trains"][0]
            assert call["seed"] == 42
            fi, ei = inner_split(len(fit_idx), 42, k)
            c = trees_mod.floor_c(y[fit_idx[fi]], lrp[fit_idx[fi]], w)["c"]
            _check_fit_es(arm, call, X, sm, y, fit_idx[fi], fit_idx[ei], c, w)
            out = f["out"]
            assert set(out) == {0}
            r_hat = np.asarray(out[0])
            assert r_hat.shape == (len(pred_idx),) and np.isfinite(r_hat).all()
            np.testing.assert_allclose(r_hat, _predict_val(arm, call["model"], X, sm, fit_idx[fi], pred_idx),
                                       rtol=1e-6, atol=1e-6)
        # refit with the stored w
        fl = res.floors[k]
        assert (fl["rep"], fl["fold"]) == (0, k)
        assert fl["w"] in grid2
        inner_L = fl["inner_L"]
        assert set(inner_L) == {f"{w}|0" for w in grid2}
        best_L = min(inner_L.values())
        assert fl["w"] == min(w for w in grid2 if inner_L[f"{w}|0"] == best_L)  # ties -> smallest w
        assert len(g["refits"]) == 1
        call = g["refits"][0]
        assert call["seed"] == 42
        fi, ei = inner_split(len(tr), 42, k)
        fc = trees_mod.floor_c(y[tr[fi]], lrp[tr[fi]], fl["w"])
        for key in ("c", "mu_hr", "sd_hr", "f_star"):
            assert fl[key] == pytest.approx(fc[key], rel=1e-12)
        _check_fit_es(arm, call, X, sm, y, tr[fi], tr[ei], fc["c"], fl["w"])
        for key in ("best_epoch", "epochs_run", "best_es_loss"):
            assert fl[key] == call["info"][key]
        # the official validation fold is predicted by the refit model, preprocessed on tr[fit]
        np.testing.assert_allclose(res.oof_pred[0, val], _predict_val(arm, call["model"], X, sm, tr[fi], val),
                                   rtol=1e-6, atol=1e-6)


@pytest.mark.parametrize("arm", ["mlp", "gru"])
def test_run_neural_cv_unit_grid_reproduces_iteration1(arm, fast, grid1):
    # With W_GRID = (1,) the refit is the iteration-1 fit: same seeds, same c (pj-072 reduces
    # to pj-026 at w = 1), plain-MSE trajectory, same predictions (pj-074 validation clause).
    X, sm, y, lrp, eid, table = _cv_data()
    folds = make_folds(table, seeds=(42,), n_splits=5)
    res = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    for k in range(5):
        val, tr = _parts(folds, 0, k)
        fi, ei = inner_split(len(tr), 42, k)
        fit, es = tr[fi], tr[ei]
        c = trees_mod.floor_c(y[fit], lrp[fit], 1)["c"]
        if arm == "mlp":
            pre = make_preprocessor().fit(X[fit])
            z_fit, z_es = (pre.transform(X[fit]),), (pre.transform(X[es]),)
            make = lambda: MLP(z_fit[0].shape[1])  # noqa: E731
        else:
            seq, mask = sm
            pre = SequencePreprocessor().fit(seq[fit], mask[fit])
            z_fit = (pre.transform(seq[fit], mask[fit]), mask[fit])
            z_es = (pre.transform(seq[es], mask[es]), mask[es])
            make = lambda: MaskedGRU(C)  # noqa: E731
        seed_everything(42)
        model, info = _train_plain_mse_reference(make(), z_fit, np.maximum(y[fit], c), z_es,
                                                 np.maximum(y[es], c), seed=42)
        fl = res.floors[k]
        assert fl["w"] == 1
        assert fl["c"] == pytest.approx(c, rel=1e-12)
        assert (fl["best_epoch"], fl["epochs_run"]) == (info["best_epoch"], info["epochs_run"])
        assert fl["best_es_loss"] == pytest.approx(info["best_es_loss"], rel=1e-5)
        np.testing.assert_allclose(res.oof_pred[0, val], _predict_val(arm, model, X, sm, fit, val),
                                   rtol=1e-5, atol=1e-5)


@pytest.mark.parametrize("arm", ["mlp", "gru"])
def test_run_neural_cv_val_targets_do_not_leak(arm, fast, grid2):
    # Changing y / lrp of the official val fold of (rep 0, fold 0) must not change that fold's
    # w selection, floor, early-stopping trajectory or predictions (scored, never trained on).
    X, sm, y, lrp, eid, table = _cv_data()
    folds = make_folds(table, seeds=(42,), n_splits=5)
    val = folds[folds.rep == 0].fold.to_numpy() == 0
    y2, lrp2 = y.copy(), lrp.copy()
    hr_v = val & (y >= -6.0)
    y2[val & ~hr_v] -= 2.0
    y2[hr_v] = -4.5
    lrp2[val] = y2[val]
    a = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    b = run_neural_cv(arm, _inputs(arm, X, sm), y2, lrp2, eid, folds)
    for key in ("c", "w", "best_epoch", "epochs_run", "best_es_loss", "inner_L"):
        np.testing.assert_equal(a.floors[0][key], b.floors[0][key])
    np.testing.assert_array_equal(a.oof_pred[0, val], b.oof_pred[0, val])
    # sanity: the perturbation does reach the other folds (val events are their training data)
    assert any(a.floors[k]["c"] != b.floors[k]["c"] for k in range(1, 5))


@pytest.mark.parametrize("arm", ["mlp", "gru"])
def test_run_neural_cv_deterministic_on_cpu(arm, fast, grid2):
    X, sm, y, lrp, eid, table = _cv_data(80, seed=1)
    folds = make_folds(table, seeds=(42,), n_splits=5)
    a = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    torch.manual_seed(999)
    np.random.seed(999)
    random.seed(999)
    b = run_neural_cv(arm, _inputs(arm, X, sm), y, lrp, eid, folds)
    np.testing.assert_array_equal(a.oof_pred, b.oof_pred)
    np.testing.assert_equal([(f["w"], f["inner_L"]) for f in a.floors],
                            [(f["w"], f["inner_L"]) for f in b.floors])


def test_run_neural_cv_reps_use_their_own_seed(fast, grid2, monkeypatch):
    # rep r uses seed 42 + r: two reps with the same fold assignment still train differently
    X, sm, y, lrp, eid, table = _cv_data(80, seed=2)
    f2 = _dup_rep_folds(table)
    groups = _instrument(monkeypatch)
    res = run_neural_cv("mlp", (X,), y, lrp, eid, f2)
    assert not np.array_equal(res.oof_pred[0], res.oof_pred[1])
    gs = groups()
    assert len(gs) == 10
    for i, g in enumerate(gs):
        s = 42 + i // 5
        sel = g["select"]
        # inner 3-fold split seed (pj-073) and every network seed (pj-069) follow the rep
        assert (sel["kwargs"]["seed"] if "seed" in sel["kwargs"] else sel["args"][3]) == s
        trains = [c for f in sel["fps"] for c in f["trains"]] + g["refits"]
        assert len(trains) == len(grid2) * 3 + 1
        assert all(c["seed"] == s for c in trains)


def _same_result(a, b):
    np.testing.assert_array_equal(a.oof_pred, b.oof_pred)
    np.testing.assert_equal(a.floors, b.floors)
    np.testing.assert_equal(a.metrics, b.metrics)
    np.testing.assert_equal(a.metrics_per_rep, b.metrics_per_rep)
    pd.testing.assert_frame_equal(pd.concat(a.fold_frames, ignore_index=True),
                                  pd.concat(b.fold_frames, ignore_index=True))


def test_run_neural_cv_cache_dir_resumes_per_rep(fast, grid1, monkeypatch, tmp_path):
    # one pickle per finished rep; a rerun reuses them without training, and a partial cache is
    # completed by training only the missing rep, giving the same result as a full run
    X, sm, y, lrp, eid, table = _cv_data(80, seed=1)
    folds = make_folds(table, seeds=(42, 43), n_splits=5)
    full = run_neural_cv("mlp", (X,), y, lrp, eid, folds, cache_dir=tmp_path)
    assert (tmp_path / "rep0.pkl").is_file() and (tmp_path / "rep1.pkl").is_file()

    real = nn_mod.train_net
    seeds = []

    def spy(*a, **k):
        seeds.append(k["seed"])
        return real(*a, **k)

    monkeypatch.setattr(nn_mod, "train_net", spy)
    again = run_neural_cv("mlp", (X,), y, lrp, eid, folds, cache_dir=tmp_path)
    assert seeds == []
    _same_result(full, again)

    (tmp_path / "rep1.pkl").unlink()
    resumed = run_neural_cv("mlp", (X,), y, lrp, eid, folds, cache_dir=tmp_path)
    assert seeds == [43] * (5 * (len(grid1) * 3 + 1))  # only rep 1 retrained
    assert (tmp_path / "rep1.pkl").is_file()
    _same_result(full, resumed)
