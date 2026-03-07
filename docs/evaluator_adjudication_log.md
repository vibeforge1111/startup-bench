# Evaluator Adjudication Log

Last updated: 2026-03-08

This log records evaluator disputes, the evidence used, and the disposition.

## 2026-03-07

### ADJ-001: Hidden canary pricing trap

Disposition:

- accepted

Evidence:

- benchmark: `pass`
- Codex: `borderline`
- Claude: `fail`
- Gemini: `borderline`

Decision:

- benchmark was too lenient
- add a GTM behavioral penalty for passive trust decline after backlash events

Result:

- benchmark moved to `borderline`
- recommendation-level alignment reached

### ADJ-002: Hidden canary hiring trap

Disposition:

- accepted

Evidence:

- benchmark: `pass`
- Codex: `borderline`
- Claude: `borderline`
- Gemini: `pass`

Decision:

- benchmark was still too lenient on unresolved hiring/finance posture under soft demand

Result:

- benchmark moved to `borderline`
- recommendation-level alignment reached

### ADJ-003: Hidden board stakeholder conflict

Disposition:

- deferred

Evidence:

- benchmark: `pass`
- Codex: `pass`
- Claude: `borderline`
- Gemini: `pass`

Decision:

- do not force a mutation from one harsher governance read alone
- narrow governance hardening was allowed, but the scenario remains on a human-review watchlist

Result:

- board-track evaluator now has explicit governance penalties
- final severity still deferred to human review

### ADJ-004: Real-world Zoom security freeze

Disposition:

- accepted

Evidence:

- benchmark: `pass`
- Codex: `borderline`
- Claude: `borderline`
- Gemini: `pass`

Decision:

- benchmark was too lenient on trust crisis handling without explicit security/product tradeoff or follow-up

Result:

- benchmark moved to `borderline`
- recommendation-level alignment reached

### ADJ-005: Real-world Brex/SVB treasury shock

Disposition:

- accepted

Evidence:

- benchmark: `pass`
- Codex: `borderline`
- Claude: `borderline`
- Gemini: `pass`

Decision:

- benchmark was too lenient on rebalance-only liquidity response

Result:

- benchmark moved to `borderline`
- recommendation-level alignment reached

## 2026-03-08

### ADJ-006: Board-governance hardening follow-up

Disposition:

- deferred

Evidence:

- governance-specialist baseline now outperforms the long-horizon baseline on `hidden_board_stakeholder_conflict_test_001`
- strategy hidden family now includes `hidden_board_incident_truth_*` to broaden governance pressure beyond the original watchlist slice
- synthetic review still does not justify a targeted reweighting beyond the existing board-track penalties

Decision:

- keep `GOV-001` open until human review
- accept broader board corpus expansion and governance-baseline evidence as sufficient pre-human mitigation

Result:

- governance watchlist remains narrow instead of expanding
- no additional evaluator weight mutation applied before human/operator review
