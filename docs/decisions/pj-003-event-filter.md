# pj-003. Event filter for S1 (train and validation)

- **Status:** accepted
- **Date:** 2026-10-24
- **Tags:** modeling | data | evaluation
- **Decided by:** Pedro
- **AI involvement:** options + critique

## Context

pj-001 defines the label as the `risk` of the last CDM and pj-002 removes events without a CDM with `time_to_tca >= 2`. In 3032 events (25 % of the base) the last CDM has `time_to_tca >= 2`, so the label CDM is also an input: LRP reproduces the label exactly (F2 = 1, L = 0). These events hold 228 of 321 HR events of the base.

## Mathematical framing

Kept events satisfy: at least one CDM with `time_to_tca >= 2` AND last CDM with `time_to_tca < 2`. This implies Uriot et al. criteria (i) and (iii). Counts in train: 8892 events, 93 HR (1.05 %): 8293 events / 66 HR with last `time_to_tca < 1` (type X), 599 / 27 with last `time_to_tca` in [1, 2) (type Y). Type Z (last `time_to_tca >= 2`, 3032 events, 228 HR) is excluded.

## Options considered

1. **Exclude Z** — removes the label/input overlap; loses 228 HR.
2. **Keep Z, drop the last CDM from its inputs** — keeps HR; label sits >= 2 d from TCA, a different task from the test's.
3. **Keep Z as is** — the model can copy `risk`; invalid for validation.

Validation: type Y included or excluded (criterion ii strict: last `time_to_tca < 1`).

## Decision

Chose option 1: Z is excluded from S1. A separate model for Z is recorded as fog. Type Y stays in both training and validation.

## Rationale (developer's own words)

Z must be removed from S1 (or handled with a different model, left as fog). The data suggest that including Y in validation is not a big problem, provided its implications are fully acknowledged and stated in every report.

## Checks raised

- Y supplies 27 of the 93 HR (29 %) and is easier for LRP (L = 0.148, bootstrap SE 0.096) → validation is somewhat optimistic; developer accepted.
- 71 % of base HR are in Z; hypothesis (unverified) that manoeuvre-related truncation hides the most dangerous events → scope limitation.
- HR prevalence 1.05 % vs 6.9 % in the official test.

## Expected behavior and validation

Filtered train has 8892 events and 93 HR; `last_ttc < 2` for every event.

## Consequences

- Every report must state: Z excluded; Y included in validation and its optimism; 93 HR → wide uncertainty; prevalence mismatch with test.
- Not doing: modeling Z events.
