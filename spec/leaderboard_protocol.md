# Leaderboard Protocol

## 1. Goal

The leaderboard exists to compare agents fairly under a fixed benchmark, scenario pack, and scaffold.

## 2. Submission requirements

Every official submission MUST declare:

- benchmark version
- scenario pack version
- scaffold version
- model id
- provider
- model release date if known
- system prompt policy
- agent code availability policy
- contamination declaration
- repeated-run count

## 3. Trace requirements

Each submission MUST include or make available:

- run traces
- score summary
- cost summary
- failure summary

Official hosted evaluations MAY keep full hidden traces private while publishing redacted summaries.

## 4. Repeat count

Recommended minimum:

- 5 runs per scenario slice for stochastic systems

If a system is effectively deterministic, the submission SHOULD still include repeated verification runs.

## 5. Contamination policy

Submissions MUST disclose known benchmark exposure such as:

- training data overlap
- scenario leakage
- evaluator leakage
- benchmark-specific tuning on hidden content

The leaderboard SHOULD support flags such as:

- `clean`
- `possible_contamination`
- `known_contamination`

## 6. Fresh split policy

The `fresh` leaderboard slice SHOULD be reported separately from the main `test` slice.

Fresh scenarios SHOULD be tied to release windows to reduce contamination risk.

## 7. Exploit and rule-violation handling

The benchmark maintainers MAY:

- invalidate submissions that exploit benchmark bugs
- mark runs with policy-violation flags
- re-score prior submissions after evaluator bug fixes

All such actions SHOULD be logged in a public changelog.

## 8. Published metrics

Leaderboard views SHOULD include:

- overall score
- track scores
- pass@1
- pass@k where relevant
- confidence interval or SEM
- API cost
- wall-clock time
- contamination flag
- benchmark version

## 9. Versioning policy

Benchmark changes MUST be versioned.

Leaderboard entries from different major benchmark versions SHOULD NOT be merged into one ranking table without a clear boundary.

## 10. Baseline publication policy

Maintainers SHOULD publish:

- random baseline
- trivial heuristic baseline
- strong scripted baseline
- human baseline summaries

## 11. Governance pack

Operational leaderboard handling SHOULD be frozen in a versioned governance pack that defines:

- entry types
- contamination response paths
- release-note requirements
- retirement rules

Current reference:

- [leaderboard_governance_pack_v0_9_0.json](/C:/Users/USER/Desktop/startup-bench/examples/leaderboard_governance_pack_v0_9_0.json)
