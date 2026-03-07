# Benchmark Known Issues

Last updated: 2026-03-07

This ledger records benchmark issues that are still open, materially relevant, or intentionally deferred.

## Open

### GOV-001: Board/governance severity still needs human confirmation

Status:

- open

Scope:

- `hidden_board_stakeholder_conflict_test_001`

Why it matters:

- synthetic review converged on `pass`, but Claude was materially harsher on governance quality
- the benchmark now scores board/governance behavior more explicitly, but that severity still needs real operator validation

Current mitigation:

- board-track evaluator is now trace-aware
- long-horizon baseline board updates are now state-aware instead of fully boilerplate

Exit condition:

- human reviewers confirm the current `pass` recommendation or force a targeted governance reweighting

### CORPUS-001: Hidden corpus breadth is still too small for official leaderboard claims

Status:

- open

Why it matters:

- hidden families now exist across real-world, strategy, operator, and canary packs
- but the total hidden corpus is still illustrative rather than benchmark-scale

Current mitigation:

- hidden packs are versioned
- `test`/`fresh` families are distinct
- canary packs exist for exploit detection

Exit condition:

- hidden coverage is materially larger across GTM, finance, people, board, product, scale, and crisis

### CAL-001: Human/operator calibration is not yet complete

Status:

- open

Why it matters:

- synthetic calibration corrected the clearest mismatches
- but real operator judgment is still the bar for a credible release candidate

Current mitigation:

- human review wave 001 is fully packaged
- reviewer assignment, form export/import, and study compilation paths are live

Exit condition:

- first human wave is completed and adjudicated

## Contained

### EVAL-001: Canary GTM trust backlash was over-rewarded

Status:

- contained

Fix:

- trace-aware GTM penalty for unanswered backlash and support-alert neglect

Verification:

- synthetic panel and benchmark now align at recommendation level

### EVAL-002: Canary hiring trap was too lenient on passive no-action loops

Status:

- contained

Fix:

- people-track penalty for unresolved hiring/finance posture under soft demand

Verification:

- synthetic panel and benchmark now align at recommendation level

### EVAL-003: Zoom security backlash was over-rewarded

Status:

- contained

Fix:

- crisis penalty for missing security/product tradeoff, post-shock board follow-up, and compliance follow-through

Verification:

- synthetic panel and benchmark now align at recommendation level

### EVAL-004: Treasury shock was over-rewarded after a single rebalance action

Status:

- contained

Fix:

- crisis penalty for rebalance-only behavior without finance follow-up

Verification:

- synthetic panel and benchmark now align at recommendation level
