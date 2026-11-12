"""Tests for S7 failure-atlas slot selection (pj-028..052, renumbered pj-051).

# contract helpers: from src.atlas.selection import HR_ALARM, alarm_tree, alarm_s4, select_atlas_slots
#   HR_ALARM == -6.0 ; alarm_tree(r_hat) -> r_hat >= -6 (inclusive) ; alarm_s4(r_hat, t) -> r_hat >= t (inclusive)
#   select_atlas_slots(event_table, labels, preds, range_risk=None, t_raw_by_clf=None, s4_t=None) -> dict with
#     'assignments' {slot: {'event_id': int|None, 'k': int, 'meta': dict} | None}, 'empty' [slot, ...], 'order' [...]
#   'k' = number of qualifying reps of the selected event (C1..C8, O1, O3) / of the O2 qualifying reps.
#   Tie-break errors: e(pred) = |risk_final - pred|, s = e_wrong - e_right (all fixtures below rank the same under
#   the signed difference too, so only the ordering is contractual).
#   S4 alarm is read from the stored p_hr column (1.0/0.0); s4_t is not passed in these tests.
#   preds slugs: rf, gbdt, ols, ridge, lasso, knn, and the 9 s6_<clf>__<reg> (clf in lr_none/lr_l2/lr_l1,
#   reg in ols/ridge/lasso) with columns event_id, rep, fold, z, p_cal, p_hr, r_hat.
#   t_raw_by_clf keys: (clf, rep, fold) -> t_raw (raw alarm of an s6 combo is sigmoid(z) >= t_raw).
#   LRP alarm = event_table.lrp >= -6 (rep independent).
"""

import numpy as np
import pandas as pd

from src.atlas.selection import HR_ALARM, alarm_s4, alarm_tree, select_atlas_slots

ORDER = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "O1", "O2", "O3"]
S4 = ["ols", "ridge", "lasso", "knn"]
S6_CLFS = ["lr_none", "lr_l2", "lr_l1"]
S6_SLUGS = [f"s6_{c}__{r}" for c in S6_CLFS for r in ["ols", "ridge", "lasso"]]
ALL = [-5.0] * 5   # alarm in every rep
NONE = [-7.0] * 5  # no alarm in any rep


def pat(bits):
    """'11100' -> r_hat per rep: alarm (-5) where 1, no alarm (-7) where 0."""
    return [-5.0 if b == "1" else -7.0 for b in bits]


def ev(eid, risk, lrp=None, jump="stable-high", delta=None, rf=None, gbdt=None, s4=None, rr=0.0, s6=None):
    """One synthetic event. Every model defaults to *agreeing with LRP* (no disagreement, so no C-slot
    qualifies by accident); tests override only the models they care about. y_hr = risk >= -6."""
    lrp = risk if lrp is None else lrp
    base = ALL if lrp >= -6.0 else NONE
    s4 = s4 or {}
    models = {"rf": rf or base, "gbdt": gbdt or base, **{m: s4.get(m, base) for m in S4}}
    return {"id": eid, "risk": risk, "lrp": lrp, "jump": jump, "rr": rr, "s6": s6, "base": base,
            "delta": risk - lrp if delta is None else delta, "models": models}


def flips(counts, hr):
    """s6 (z, cal-alarm) arrays [rep, combo]: in rep r the first counts[r] combos flip fail->success
    (raw wrong at t_raw=0.5, calibrated right); the other combos are right in both."""
    z = np.full((5, 9), 2.0 if hr else -2.0)
    cal = np.full((5, 9), hr)
    for rep, n in enumerate(counts):
        z[rep, :n] = -2.0 if hr else 2.0
    return z, cal


def world(events, t_raw_by_fold=None):
    t_raw_by_fold = t_raw_by_fold or {}
    et = pd.DataFrame({
        "event_id": np.array([e["id"] for e in events], dtype="int64"),
        "risk_final": [float(e["risk"]) for e in events],
        "y_hr": [e["risk"] >= -6.0 for e in events],
        "lrp": [float(e["lrp"]) for e in events],
    })
    labels = pd.DataFrame({
        "event_id": et.event_id,
        "delta": [float(e["delta"]) for e in events],
        "jump_class": [e["jump"] for e in events],
    })
    rows = {m: [] for m in ["rf", "gbdt", *S4]}
    s6rows = {s: [] for s in S6_SLUGS}
    for e in events:
        fold = e["id"] % 3
        for m, vals in e["models"].items():
            for rep in range(5):
                rows[m].append((e["id"], rep, fold, vals[rep], float(vals[rep] >= -6.0)))
        alarm = e["lrp"] >= -6.0
        z, cal = e["s6"] if e["s6"] is not None else (np.full((5, 9), 2.0 if alarm else -2.0), np.full((5, 9), alarm))
        for j, slug in enumerate(S6_SLUGS):
            for rep in range(5):
                c = bool(cal[rep, j])
                s6rows[slug].append((e["id"], rep, fold, float(z[rep, j]), 0.9 if c else 0.1, float(c), -5.0 if c else -7.0))
    preds = {m: pd.DataFrame(r, columns=["event_id", "rep", "fold", "r_hat", "p_hr"]) for m, r in rows.items()}
    preds.update({s: pd.DataFrame(r, columns=["event_id", "rep", "fold", "z", "p_cal", "p_hr", "r_hat"])
                  for s, r in s6rows.items()})
    range_risk = pd.Series({e["id"]: float(e["rr"]) for e in events})
    t_raw = {(c, rep, f): t_raw_by_fold.get(f, 0.5) for c in S6_CLFS for rep in range(5) for f in range(3)}
    return select_atlas_slots(et, labels, preds, range_risk=range_risk, t_raw_by_clf=t_raw, s4_t=None)


def eid(res, slot):
    a = res["assignments"][slot]
    return None if a is None else a["event_id"]


def assert_empty(res, slot):
    assert eid(res, slot) is None
    assert slot in res["empty"]


# ---------------------------------------------------------------- alarm helpers

def test_alarm_helpers_inclusive_thresholds():
    assert HR_ALARM == -6.0
    assert bool(alarm_tree(-6.0)) and not bool(alarm_tree(-6.0001))
    assert bool(alarm_s4(-3.0, -3.0)) and not bool(alarm_s4(-3.0001, -3.0))
    assert bool(alarm_s4(-7.0, -8.0))  # uses the fold t, not -6


# ---------------------------------------------------------------- C1 / C2

def test_c1_picks_highest_risk_among_qualifiers_only():
    res = world([
        ev(1, -5.0, lrp=-8.0, rf=ALL),  # qualifies, lower risk
        ev(2, -3.0, lrp=-8.0, rf=ALL),  # qualifies, highest risk among qualifiers -> expected
        ev(3, -1.0, lrp=-8.0),          # higher risk but no tree TP -> not a C1 candidate
    ])
    assert eid(res, "C1") == 2
    assert res["assignments"]["C1"]["k"] == 5
    assert res["order"] == ORDER


def test_c1_gate_three_of_five_reps_and_union_of_trees():
    res = world([
        ev(1, -2.0, lrp=-8.0, rf=pat("11000")),  # only 2/5 reps -> must not qualify despite highest risk
        ev(2, -5.0, lrp=-8.0, rf=pat("11100")),  # exactly 3/5 -> qualifies
    ])
    assert eid(res, "C1") == 2
    assert res["assignments"]["C1"]["k"] == 3
    # >=1 of {rf, gbdt}: rf TP in reps 0,1 and gbdt TP in rep 2 -> 3 reps qualify through the union
    res = world([
        ev(1, -5.0, lrp=-8.0, rf=pat("11000"), gbdt=pat("00100")),
        ev(2, -2.0, lrp=-8.0, rf=pat("11000")),
    ])
    assert eid(res, "C1") == 1
    assert res["assignments"]["C1"]["k"] == 3


def test_c1_tie_break_largest_lrp_vs_panel_tree_gap():
    # same risk_final; s = |risk-LRP| - |risk-r_hat(rf)| : id5 -> 3, id3 -> 2, id1 -> 1.5 (smallest id must not win)
    res = world([
        ev(1, -4.0, lrp=-6.5, rf=ALL),
        ev(3, -4.0, lrp=-7.0, rf=ALL),
        ev(5, -4.0, lrp=-8.0, rf=ALL),
    ])
    assert eid(res, "C1") == 5


def test_c2_tie_break_swapped_roles():
    # LRP right (-4.5, risk -4), rf is the wrong panel tree: s = |risk-r_hat(rf)| - |risk-LRP|
    # id5: 5-0.5=4.5 ; id3: 3-0.5=2.5 ; id1: 2.5-0.5=2.0
    res = world([
        ev(1, -4.0, lrp=-4.5, rf=[-6.5] * 5),
        ev(3, -4.0, lrp=-4.5, rf=[-7.0] * 5),
        ev(5, -4.0, lrp=-4.5, rf=[-9.0] * 5),
    ])
    assert eid(res, "C2") == 5


# ---------------------------------------------------------------- C3 / C4 (S4)

def test_c3_requires_three_of_four_s4_tp_per_rep_and_three_of_five_reps():
    three = {"ols": ALL, "ridge": ALL, "lasso": ALL}  # knn follows LRP (FN) -> 3/4 TP
    res = world([
        ev(1, -4.0, lrp=-8.0, s4=three),                                   # 3/4 in 5 reps -> qualifies
        ev(2, -2.0, lrp=-8.0, s4={"ols": ALL, "ridge": ALL}),              # only 2/4 TP -> no
        ev(3, -1.0, lrp=-8.0, s4={m: pat("11000") for m in S4[:3]}),       # 3/4 in only 2 reps -> no
        ev(4, -3.0, lrp=-8.0, s4={m: pat("11100") for m in S4[:3]}),       # 3/4 in 3 reps, higher risk than id1
    ])
    assert eid(res, "C1") is None  # trees follow LRP (FN): the S4 events must not leak into C1
    assert eid(res, "C3") == 4
    assert res["assignments"]["C3"]["k"] == 3


def test_c3_tie_break_uses_lrp_as_wrong_and_s4_as_right():
    four = {m: ALL for m in S4}
    res = world([
        ev(1, -4.0, lrp=-6.5, s4=four),
        ev(3, -4.0, lrp=-7.0, s4=four),
        ev(5, -4.0, lrp=-8.0, s4=four),  # biggest LRP miss, S4 equally right -> highest s
    ])
    assert eid(res, "C3") == 5


def test_c4_requires_three_of_four_s4_fn_with_lrp_tp():
    res = world([
        ev(1, -4.0, s4={"ols": NONE, "ridge": NONE, "lasso": NONE}),                  # 3/4 FN -> qualifies
        ev(2, -2.0, s4={"ols": NONE, "ridge": NONE}),                                 # 2/4 FN -> no
        ev(3, -1.0, s4={m: pat("11100") for m in S4[:3]}),                            # FN only in 2 reps -> no
    ])
    assert eid(res, "C4") == 1


# ---------------------------------------------------------------- C5 / C6 / C7

def test_c5_jump_up_hr_with_two_of_three_fn():
    res = world([
        ev(1, -4.0, lrp=-6.5, jump="jump-up", delta=1.2, rf=NONE, gbdt=NONE),   # qualifies, small delta
        ev(6, -4.0, lrp=-6.5, jump="jump-up", delta=3.0, rf=NONE, gbdt=NONE),   # qualifies, largest |delta| -> expected
        ev(2, -7.0, lrp=-9.0, jump="jump-up", delta=8.0),                       # jump-up but y_hr=0 -> no
        ev(3, -5.0, lrp=-3.0, jump="jump-down", delta=-9.0, rf=NONE, gbdt=NONE),  # right outcome, wrong class
        ev(4, -4.0, lrp=-5.5, jump="jump-up", delta=7.0, rf=NONE),              # only 1 of 3 FN -> no
        ev(5, -4.0, lrp=-5.5, jump="jump-up", delta=6.0,
           rf=pat("11100"), gbdt=pat("11100")),                                 # 2 FN but in only 2 reps -> no
        ev(9, -1.0, lrp=-1.0, rf=NONE),                                         # C2 shield (keeps ids 3,4 free)
    ])
    assert eid(res, "C2") == 9
    assert eid(res, "C5") == 6
    assert res["assignments"]["C5"]["k"] == 5


def test_c6_jump_down_non_hr_with_two_of_three_fp_and_tie_smallest_id():
    res = world([
        ev(1, -8.0, lrp=-5.5, jump="jump-down", delta=-2.0, rf=ALL),            # 3 FP, small |delta|
        ev(6, -8.0, lrp=-5.5, jump="jump-down", delta=-3.0, rf=ALL),            # 3 FP, |delta| tie with id7
        ev(7, -8.0, lrp=-5.5, jump="jump-down", delta=-3.0, rf=ALL),
        ev(2, -8.0, lrp=-5.5, jump="jump-down", delta=-9.0, rf=NONE, gbdt=NONE),  # only LRP FP -> no
        ev(3, -7.0, lrp=-9.0, jump="jump-up", delta=8.0, rf=ALL, gbdt=ALL),     # 2 FP but jump-up -> no
        ev(4, -5.0, lrp=-3.0, jump="jump-down", delta=-9.0, rf=ALL, gbdt=ALL),  # jump-down but y_hr=1 -> no
        ev(5, -9.0, lrp=-8.0, jump="jump-down", delta=-9.0,
           rf=pat("11000"), gbdt=pat("11000")),                                 # 2 FP in only 2 reps -> no
    ])
    assert eid(res, "C6") == 6


# ---------------------------------------------------------------- C8

def test_c8_multi_fail_needs_two_fn_and_stability_and_picks_risk():
    res = world([
        ev(1, -5.0, lrp=-8.0),                                                  # 3 FN, lower risk
        ev(2, -3.0, lrp=-8.0, gbdt=ALL),                                        # exactly 2 FN -> expected
        ev(3, -1.0, lrp=-8.0, rf=ALL, gbdt=ALL),                                # only LRP FN, risk higher than id2
        ev(4, -0.5, lrp=-8.0, rf=ALL, gbdt=ALL),                                # only LRP FN, takes C1 (highest risk)
        ev(5, -2.0, lrp=-2.0, rf=pat("00111"), gbdt=pat("00111")),              # 2 FN in only 2 reps -> no
    ])
    assert eid(res, "C1") == 4
    assert eid(res, "C8") == 2


# ---------------------------------------------------------------- exclusion order

def test_exclusion_earlier_slot_wins_and_ids_are_unique():
    res = world([
        ev(1, -4.0, lrp=-8.0, jump="jump-up", delta=4.0, rf=ALL),               # C1 and C5 both qualify
        ev(2, -4.5, lrp=-6.5, jump="jump-up", delta=2.0),                       # only C5 (all 3 FN, no tree TP)
    ])
    assert eid(res, "C1") == 1
    assert eid(res, "C5") == 2  # without the exclusion list C5 would take id1 (|delta| 4 > 2)
    taken = [eid(res, s) for s in ORDER if eid(res, s) is not None]
    assert len(taken) == len(set(taken))


# ---------------------------------------------------------------- O1

def test_o1_uses_range_risk_after_exclusions_and_all_tp_stability():
    res = world([
        ev(1, -4.0, rr=3.0),
        ev(2, -4.0, rr=7.0),                          # all TP in all reps, best range among free events -> expected
        ev(3, -1.0, rf=NONE, rr=9.0),                 # highest range but consumed by C2 (earlier slot)
        ev(4, -4.0, gbdt=pat("11000"), rr=99.0),      # all-TP in only 2 reps -> no
    ])
    assert eid(res, "C2") == 3
    assert eid(res, "O1") == 2


# ---------------------------------------------------------------- O2

def test_o2_flip_count_gate_stability_and_mean_over_qualifying_reps():
    res = world([
        ev(1, -8.0, s6=flips([6] * 5, False)),                  # mean 6 over all reps
        ev(2, -8.0, s6=flips([9, 9, 9, 0, 0], False)),          # 3 qualifying reps, mean 9 over them -> expected
        ev(3, -8.0, s6=flips([9, 9, 0, 0, 0], False)),          # only 2 reps reach >=5 -> no
        ev(4, -8.0, s6=flips([4] * 5, False)),                  # 4 flips < 5 -> no
    ])
    assert eid(res, "O2") == 2
    # boundary: exactly 5 combos qualifies, 4 does not
    assert eid(world([ev(1, -8.0, s6=flips([5] * 5, False))]), "O2") == 1
    assert_empty(world([ev(1, -8.0, s6=flips([4] * 5, False))]), "O2")
    # HR events flip too (FN raw -> TP calibrated)
    # (id9 is an O1 shield: an all-TP HR event would otherwise be consumed by O1, which precedes O2)
    assert eid(world([ev(1, -4.0, s6=flips([5] * 5, True)), ev(9, -4.0, rr=100.0)]), "O2") == 1


def test_o2_raw_alarm_uses_t_raw_not_a_fixed_half():
    logit = lambda p: float(np.log(p / (1 - p)))
    z = np.full((5, 9), logit(0.4))
    # negative event (fold 1): p_raw 0.4 >= t_raw 0.3 -> raw FP, calibrated TN -> flip in all combos
    neg = world([ev(1, -8.0, s6=(z, np.full((5, 9), False)))], t_raw_by_fold={1: 0.3})
    assert eid(neg, "O2") == 1
    # positive event (fold 2): p_raw 0.6 < t_raw 0.7 -> raw FN, calibrated TP -> flip in all combos
    z = np.full((5, 9), logit(0.6))
    pos = world([ev(2, -4.0, s6=(z, np.full((5, 9), True))), ev(9, -4.0, rr=100.0)], t_raw_by_fold={2: 0.7})
    assert eid(pos, "O2") == 2


# ---------------------------------------------------------------- C7 / O3

def test_c7_and_o3_opposite_jump_class_and_c6_shield():
    res = world([
        ev(1, -4.0, lrp=-5.5, jump="jump-up", delta=3.5),                       # 3/3 correct, largest |delta| -> C7
        ev(4, -4.0, lrp=-5.5, jump="jump-up", delta=2.5),                       # qualifies but smaller
        ev(2, -8.0, lrp=-5.5, jump="jump-down", delta=-2.0, rf=NONE, gbdt=NONE),  # 2/3 correct -> O3 expected
        ev(3, -8.0, lrp=-5.5, jump="jump-down", delta=-9.0, rf=ALL, gbdt=NONE),            # only 1/3 correct -> not O3
        ev(6, -8.0, lrp=-5.5, jump="jump-down", delta=-10.0, rf=ALL, gbdt=ALL),  # 3 FP: taken by C6
    ])
    assert eid(res, "C6") == 6
    assert eid(res, "C7") == 1
    assert eid(res, "O3") == 2  # jump-down only (opposite of C7's jump-up), qualified, not excluded


def test_o3_empty_when_c7_empty():
    res = world([
        ev(1, -4.0, lrp=-8.0, jump="jump-up", delta=4.0, rf=ALL, gbdt=ALL),        # 2/3 correct but C1 takes it
        ev(2, -5.0, lrp=-3.0, jump="jump-down", delta=-2.0, rf=NONE, gbdt=ALL),    # 2/3 correct but C2 takes it
        ev(3, -5.0),                                                               # no jump
    ])
    assert eid(res, "C1") == 1
    assert eid(res, "C2") == 2
    assert_empty(res, "C7")
    assert_empty(res, "O3")


# ---------------------------------------------------------------- empty pools

def test_empty_pool_recorded_and_rules_not_relaxed():
    res = world([ev(1, -5.0), ev(2, -8.0)])  # every model agrees everywhere, no jumps, nothing flips
    assert set(res["assignments"]) == set(ORDER)
    assert res["order"] == ORDER
    for slot in ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "O2", "O3"]:
        assert_empty(res, slot)
    assert eid(res, "O1") == 1  # the only all-TP HR event is still picked
    assert "O1" not in res["empty"]


def test_pool_emptied_by_exclusion_is_empty_not_relaxed():
    # the single multi-fail event is consumed by C1 (LRP FN + gbdt FN, rf TP), so C8 stays empty
    res = world([ev(1, -4.0, lrp=-8.0, rf=ALL)])
    assert eid(res, "C1") == 1
    assert_empty(res, "C8")
