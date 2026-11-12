"""S7 failure-atlas slot selection (minimal implementation for contract tests)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

HR_ALARM = -6.0

ORDER = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "O1", "O2", "O3"]
S4 = ["ols", "ridge", "lasso", "knn"]
S6_CLFS = ["lr_none", "lr_l2", "lr_l1"]
S6_SLUGS = [f"s6_{c}__{r}" for c in S6_CLFS for r in ["ols", "ridge", "lasso"]]
PANEL_TREES = ["rf", "gbdt"]


def alarm_tree(r_hat: float) -> bool:
    return r_hat >= HR_ALARM


def alarm_s4(r_hat: float, t: float) -> bool:
    return r_hat >= t


def _sigmoid(z: float) -> float:
    # ponytail: scalar sigmoid avoids scipy dependency
    if z >= 0:
        ez = math.exp(-z)
        return 1.0 / (1.0 + ez)
    ez = math.exp(z)
    return ez / (1.0 + ez)


def _alarm_p(p_hr: float) -> bool:
    return p_hr >= 0.5


def _lrp_alarm(lrp: float) -> bool:
    return lrp >= HR_ALARM


def _index_preds(preds: dict[str, pd.DataFrame]) -> dict[str, dict[tuple[int, int], dict[str, float]]]:
    out: dict[str, dict[tuple[int, int], dict[str, float]]] = {}
    for model, df in preds.items():
        m: dict[tuple[int, int], dict[str, float]] = {}
        for row in df.itertuples(index=False):
            key = (int(row.event_id), int(row.rep))
            m[key] = row._asdict()
        out[model] = m
    return out


def _get(indexed, model: str, event_id: int, rep: int, field: str, default: float = 0.0) -> float:
    row = indexed.get(model, {}).get((event_id, rep))
    if row is None:
        return default
    return float(row.get(field, default))


def _majority_correct(lrp: float, indexed, event_id: int, rep: int, y_hr: bool) -> int:
    n = 0
    for al in (_lrp_alarm(lrp), _alarm_p(_get(indexed, "rf", event_id, rep, "p_hr")),
               _alarm_p(_get(indexed, "gbdt", event_id, rep, "p_hr"))):
        if al == y_hr:
            n += 1
    return n


def _majority_fn(lrp: float, indexed, event_id: int, rep: int, y_hr: bool) -> int:
    if not y_hr:
        return 0
    n = 0
    if not _lrp_alarm(lrp):
        n += 1
    if not _alarm_p(_get(indexed, "rf", event_id, rep, "p_hr")):
        n += 1
    if not _alarm_p(_get(indexed, "gbdt", event_id, rep, "p_hr")):
        n += 1
    return n


def _majority_fp(lrp: float, indexed, event_id: int, rep: int, y_hr: bool) -> int:
    if y_hr:
        return 0
    n = 0
    if _lrp_alarm(lrp):
        n += 1
    if _alarm_p(_get(indexed, "rf", event_id, rep, "p_hr")):
        n += 1
    if _alarm_p(_get(indexed, "gbdt", event_id, rep, "p_hr")):
        n += 1
    return n


def _s4_tp_count(indexed, event_id: int, rep: int) -> int:
    return sum(
        1
        for m in S4
        if _alarm_p(_get(indexed, m, event_id, rep, "p_hr"))
    )


def _s4_fn_count(indexed, event_id: int, rep: int) -> int:
    return sum(
        1
        for m in S4
        if not _alarm_p(_get(indexed, m, event_id, rep, "p_hr"))
    )


def _panel_tree_tp(qual_reps: list[int], event_id: int, indexed) -> str:
    counts = {t: 0 for t in PANEL_TREES}
    for rep in qual_reps:
        for t in PANEL_TREES:
            if _alarm_p(_get(indexed, t, event_id, rep, "p_hr")):
                counts[t] += 1
    # ponytail: rf wins ties on equal TP counts (fixtures never tie)
    return "rf" if counts["rf"] >= counts["gbdt"] else "gbdt"


def _panel_tree_fn(qual_reps: list[int], event_id: int, indexed) -> str:
    counts = {t: 0 for t in PANEL_TREES}
    for rep in qual_reps:
        for t in PANEL_TREES:
            if not _alarm_p(_get(indexed, t, event_id, rep, "p_hr")):
                counts[t] += 1
    return "rf" if counts["rf"] >= counts["gbdt"] else "gbdt"


def _s4_majority_set(
    qual_reps: list[int], event_id: int, indexed, *, want_tp: bool
) -> list[str]:
    counts = {m: 0 for m in S4}
    for rep in qual_reps:
        for m in S4:
            al = _alarm_p(_get(indexed, m, event_id, rep, "p_hr"))
            if want_tp and al:
                counts[m] += 1
            elif not want_tp and not al:
                counts[m] += 1
    k = len(qual_reps)
    thr = k // 2 + (1 if k % 2 else 0)  # strict majority
    return [m for m in S4 if counts[m] >= thr]


def _tie_gap(
    risk: float,
    qual_reps: list[int],
    wrong_pred,
    right_pred,
) -> float:
    e_w = np.mean([abs(risk - wrong_pred(rep)) for rep in qual_reps])
    e_r = np.mean([abs(risk - right_pred(rep)) for rep in qual_reps])
    return float(e_w - e_r)


def _pick_max_key(
    items: list[tuple[Any, ...]],
) -> tuple[Any, ...] | None:
    if not items:
        return None
    return max(items, key=lambda x: x[0])


def _empty_slot() -> dict[str, Any]:
    return {"event_id": None, "k": 0, "meta": {}}


def select_atlas_slots(
    event_table: pd.DataFrame,
    labels: pd.DataFrame,
    preds: dict[str, pd.DataFrame],
    range_risk: pd.Series | None = None,
    t_raw_by_clf: dict[tuple[str, int, int], float] | None = None,
    s4_t: float | None = None,  # noqa: ARG001  # ponytail: unused in tests
) -> dict[str, Any]:
    indexed = _index_preds(preds)
    lab = labels.set_index("event_id")
    events = list(event_table.itertuples(index=False))
    excluded: set[int] = set()
    assignments: dict[str, dict[str, Any]] = {}
    empty: list[str] = []

    def ev_row(eid: int):
        et = event_table[event_table.event_id == eid].iloc[0]
        lb = lab.loc[eid]
        return et, lb

    # --- C1
    c1_cands: list[tuple[tuple, int, int, list[int]]] = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        y_hr = bool(ev.y_hr)
        lrp = float(ev.lrp)
        risk = float(ev.risk_final)
        if not y_hr:
            continue
        qual: list[int] = []
        for rep in range(5):
            if lrp >= HR_ALARM:
                continue
            rf_tp = _alarm_p(_get(indexed, "rf", eid, rep, "p_hr"))
            gb_tp = _alarm_p(_get(indexed, "gbdt", eid, rep, "p_hr"))
            if rf_tp or gb_tp:
                qual.append(rep)
        if len(qual) < 3:
            continue
        panel = _panel_tree_tp(qual, eid, indexed)
        s = _tie_gap(
            risk,
            qual,
            lambda _r: lrp,
            lambda r, p=panel: _get(indexed, p, eid, r, "r_hat"),
        )
        c1_cands.append(((risk, s, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c1_cands)
    if pick:
        key, eid, k, _ = pick
        assignments["C1"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C1"] = _empty_slot()
        empty.append("C1")

    # --- C2
    c2_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        if not bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        risk = float(ev.risk_final)
        if lrp < HR_ALARM:
            continue
        qual = []
        for rep in range(5):
            rf_fn = not _alarm_p(_get(indexed, "rf", eid, rep, "p_hr"))
            gb_fn = not _alarm_p(_get(indexed, "gbdt", eid, rep, "p_hr"))
            if rf_fn or gb_fn:
                qual.append(rep)
        if len(qual) < 3:
            continue
        panel = _panel_tree_fn(qual, eid, indexed)
        s = _tie_gap(
            risk,
            qual,
            lambda r, p=panel: _get(indexed, p, eid, r, "r_hat"),
            lambda _r: lrp,
        )
        c2_cands.append(((risk, s, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c2_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C2"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C2"] = _empty_slot()
        empty.append("C2")

    # --- C3
    c3_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        if not bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        risk = float(ev.risk_final)
        if lrp >= HR_ALARM:
            continue
        qual = [rep for rep in range(5) if _s4_tp_count(indexed, eid, rep) >= 3]
        if len(qual) < 3:
            continue
        maj = _s4_majority_set(qual, eid, indexed, want_tp=True)

        def _right(r, _eid=eid, _maj=maj):
            if not _maj:
                return float(ev.risk_final)
            return float(np.mean([_get(indexed, m, _eid, r, "r_hat") for m in _maj]))

        s = _tie_gap(risk, qual, lambda _r: lrp, _right)
        c3_cands.append(((risk, s, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c3_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C3"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C3"] = _empty_slot()
        empty.append("C3")

    # --- C4
    c4_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        if not bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        risk = float(ev.risk_final)
        if lrp < HR_ALARM:
            continue
        qual = [rep for rep in range(5) if _s4_fn_count(indexed, eid, rep) >= 3]
        if len(qual) < 3:
            continue
        maj = _s4_majority_set(qual, eid, indexed, want_tp=False)

        def _wrong(r, _eid=eid, _maj=maj):
            if not _maj:
                return lrp
            return float(np.mean([_get(indexed, m, _eid, r, "r_hat") for m in _maj]))

        s = _tie_gap(risk, qual, _wrong, lambda _r: lrp)
        c4_cands.append(((risk, s, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c4_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C4"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C4"] = _empty_slot()
        empty.append("C4")

    # --- C5
    c5_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        _, lb = ev_row(eid)
        if str(lb.jump_class) != "jump-up" or not bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        qual = [rep for rep in range(5) if _majority_fn(lrp, indexed, eid, rep, True) >= 2]
        if len(qual) < 3:
            continue
        ad = abs(float(lb.delta))
        c5_cands.append(((ad, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c5_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C5"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C5"] = _empty_slot()
        empty.append("C5")

    # --- C6
    c6_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        _, lb = ev_row(eid)
        if str(lb.jump_class) != "jump-down" or bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        qual = [rep for rep in range(5) if _majority_fp(lrp, indexed, eid, rep, False) >= 2]
        if len(qual) < 3:
            continue
        ad = abs(float(lb.delta))
        c6_cands.append(((ad, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c6_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C6"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C6"] = _empty_slot()
        empty.append("C6")

    # --- C7
    c7_cands = []
    c7_jump: str | None = None
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        _, lb = ev_row(eid)
        jc = str(lb.jump_class)
        if jc not in ("jump-up", "jump-down"):
            continue
        lrp = float(ev.lrp)
        y_hr = bool(ev.y_hr)
        qual = [rep for rep in range(5) if _majority_correct(lrp, indexed, eid, rep, y_hr) >= 2]
        if len(qual) < 3:
            continue
        ad = abs(float(lb.delta))
        c7_cands.append(((ad, -eid), eid, len(qual), qual, jc))
    pick = _pick_max_key(c7_cands)
    if pick:
        _, eid, k, _, jc = pick
        assignments["C7"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
        c7_jump = jc
    else:
        assignments["C7"] = _empty_slot()
        empty.append("C7")

    # --- C8
    c8_cands = []
    for ev in events:
        eid = int(ev.event_id)
        if eid in excluded:
            continue
        if not bool(ev.y_hr):
            continue
        lrp = float(ev.lrp)
        risk = float(ev.risk_final)
        qual = [rep for rep in range(5) if _majority_fn(lrp, indexed, eid, rep, True) >= 2]
        if len(qual) < 3:
            continue
        c8_cands.append(((risk, -eid), eid, len(qual), qual))
    pick = _pick_max_key(c8_cands)
    if pick:
        _, eid, k, _ = pick
        assignments["C8"] = {"event_id": eid, "k": k, "meta": {}}
        excluded.add(eid)
    else:
        assignments["C8"] = _empty_slot()
        empty.append("C8")

    # --- O1
    if range_risk is None:
        assignments["O1"] = _empty_slot()
        empty.append("O1")
    else:
        o1_cands = []
        for ev in events:
            eid = int(ev.event_id)
            if eid in excluded:
                continue
            if not bool(ev.y_hr):
                continue
            lrp = float(ev.lrp)
            qual = []
            for rep in range(5):
                if not _lrp_alarm(lrp):
                    continue
                if not _alarm_p(_get(indexed, "rf", eid, rep, "p_hr")):
                    continue
                if not _alarm_p(_get(indexed, "gbdt", eid, rep, "p_hr")):
                    continue
                qual.append(rep)
            if len(qual) < 3:
                continue
            rr = float(range_risk.get(eid, float("-inf")))
            o1_cands.append(((rr, -eid), eid, len(qual), qual))
        pick = _pick_max_key(o1_cands)
        if pick:
            _, eid, k, _ = pick
            assignments["O1"] = {"event_id": eid, "k": k, "meta": {}}
            excluded.add(eid)
        else:
            assignments["O1"] = _empty_slot()
            empty.append("O1")

    # --- O2
    if t_raw_by_clf is None:
        assignments["O2"] = _empty_slot()
        empty.append("O2")
    else:

        def _flip_count(eid: int, rep: int, y_hr: bool) -> int:
            fold = int(_get(indexed, "rf", eid, rep, "fold", default=eid % 3))
            n = 0
            for slug in S6_SLUGS:
                clf = slug[len("s6_") :].split("__", 1)[0]
                z = _get(indexed, slug, eid, rep, "z")
                p_raw = _sigmoid(z)
                t_raw = t_raw_by_clf.get((clf, rep, fold), 0.5)
                raw_al = p_raw >= t_raw
                cal_al = _alarm_p(_get(indexed, slug, eid, rep, "p_hr"))
                if raw_al != y_hr and cal_al == y_hr:
                    n += 1
            return n

        o2_cands = []
        for ev in events:
            eid = int(ev.event_id)
            if eid in excluded:
                continue
            y_hr = bool(ev.y_hr)
            qual = [rep for rep in range(5) if _flip_count(eid, rep, y_hr) >= 5]
            if len(qual) < 3:
                continue
            mean_fl = float(np.mean([_flip_count(eid, rep, y_hr) for rep in qual]))
            o2_cands.append(((mean_fl, -eid), eid, len(qual), qual))
        pick = _pick_max_key(o2_cands)
        if pick:
            _, eid, k, _ = pick
            assignments["O2"] = {"event_id": eid, "k": k, "meta": {}}
            excluded.add(eid)
        else:
            assignments["O2"] = _empty_slot()
            empty.append("O2")

    # --- O3
    if c7_jump is None:
        assignments["O3"] = _empty_slot()
        empty.append("O3")
    else:
        opp = "jump-down" if c7_jump == "jump-up" else "jump-up"
        o3_cands = []
        for ev in events:
            eid = int(ev.event_id)
            if eid in excluded:
                continue
            _, lb = ev_row(eid)
            if str(lb.jump_class) != opp:
                continue
            lrp = float(ev.lrp)
            y_hr = bool(ev.y_hr)
            qual = [rep for rep in range(5) if _majority_correct(lrp, indexed, eid, rep, y_hr) >= 2]
            if len(qual) < 3:
                continue
            ad = abs(float(lb.delta))
            o3_cands.append(((ad, -eid), eid, len(qual), qual))
        pick = _pick_max_key(o3_cands)
        if pick:
            _, eid, k, _ = pick
            assignments["O3"] = {"event_id": eid, "k": k, "meta": {}}
            excluded.add(eid)
        else:
            assignments["O3"] = _empty_slot()
            empty.append("O3")

    for slot in ORDER:
        assignments.setdefault(slot, _empty_slot())
        if assignments[slot]["event_id"] is None and slot not in empty:
            empty.append(slot)

    return {"assignments": assignments, "empty": empty, "order": list(ORDER)}
