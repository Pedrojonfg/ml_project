# 021. Methodology framing in the proposal PDF

- **Status:** accepted
- **Date:** 2026-10-11
- **Tags:** product | research | process
- **Decided by:** human

## Context

Options A–D framed a static ladder. The user proposed an epistemic attitude better aligned with 011 (post-PCA honesty): name what is already taught, what is upcoming in the syllabus, openness to out-of-syllabus study, contrast with the competition paper, and redirect to *this* project’s aims (not paper/leaderboard replication).

## Options considered

1. **A** — Baselines + “models TBD”.
2. **B** — Fixed ladder baselines → classical → two-stage/cal → PyTorch stretch.
3. **C** — B + Magpies-like LSTM named as core.
4. **D** — Long technique menu.
5. **E (user)** — Layered attitude: already-in-class / upcoming-in-class / out-of-syllabus interest; cite paper methods; then “we are not replicating the paper, we pursue … so we will likely try …”.

## Decision

Chose **E** — the user’s framing. Concrete fill for the PDF (editable names, fixed logic):

**Already covered (as of proposal):** material through PCA (and earlier linear algebra / basic supervised ideas as taught). Use for EDA (e.g. PCA as exploration if useful) and any simple linear baselines we can run honestly.

**Upcoming in the course (planned to use as they appear):** course-path models suitable for tabular/event features — e.g. linear/logistic regression refinements, trees / ensembles, neural nets via PyTorch when taught — under a shared evaluation protocol.

**Out-of-syllabus (interested to explore if needed):** calibration / reliability analysis; two-stage decision structure (high-risk detection + magnitude); imbalance-aware metrics and thresholding; optionally light sequence models — studied in a directed way, not assumed mastered now.

**In the original challenge/paper:** strong LRP/CRP baselines; many teams used static tabular models; winners included metric-aware rule cascades (sesc) and a Magpies Manhattan-LSTM / anomaly-style approach; post-comp analysis also explored residual boosting, etc. (cite Uriot et al.).

**Nevertheless:** we are **not** trying to re-run or beat the 2019 leaderboard. We pursue (1) a fair bake-off vs LRP under rare-event metrics and (2) calibrated two-stage early warning with honest failure analysis on jump-like events. Therefore we will **probably try** protocol-first baselines, then course models as available, then two-stage + calibration as the project differentiator, with PyTorch as a fair ablation—not a Magpies re-implementation as the claim.

## Why

Matches the team’s real knowledge state and ADRs 007–011, 016–018. Reads as mature course work rather than fake expertise or Kelvins cosplay.

## Consequences

- Methodology section uses this narrative spine; avoid promising Magpies/siamese LSTM as core.
- Verbs stay plan-oriented (*will use / plan to / interested in exploring*).
- Prelim section stays CRP/LRP only (017); learned models appear under next steps / methodology plan.
