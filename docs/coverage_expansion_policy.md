# Coverage Expansion Policy

Last updated: 2026-03-08

This policy defines how TheStartupBench should expand benchmark coverage without drifting away from benchmark-standard methodology.

The goal is not to add more startup topics at any cost. The goal is to add coverage while preserving:

- executable evaluation
- programmatic scoring as the primary signal
- hidden-eval integrity
- anti-gaming pressure
- repeated-run reporting
- operator calibration
- versioned benchmark governance

## 1. Core rule

Coverage expansion MUST increase domain breadth or realism without weakening the benchmark invariants defined in:

- [benchmark_contract.md](/C:/Users/USER/Desktop/startup-bench/spec/benchmark_contract.md)
- [scoring_contract.md](/C:/Users/USER/Desktop/startup-bench/spec/scoring_contract.md)
- [hidden_eval_policy.md](/C:/Users/USER/Desktop/startup-bench/spec/hidden_eval_policy.md)
- [leaderboard_protocol.md](/C:/Users/USER/Desktop/startup-bench/spec/leaderboard_protocol.md)
- [operator_eval_protocol.md](/C:/Users/USER/Desktop/startup-bench/spec/operator_eval_protocol.md)

In practice, new coverage is acceptable only if it makes the benchmark broader or more realistic while remaining comparably auditable and difficult to game.

## 2. Non-negotiable standards

All promoted coverage expansions MUST preserve the following properties:

- stateful, executable scenarios rather than essay-style tasks
- explicit world-state transitions and bounded tools
- partial observability
- seeded reproducibility
- programmatic evaluation for most scored outcomes
- auditable traces, artifacts, and score decomposition
- hidden `test` and hidden `fresh` split discipline
- repeated-run reporting with uncertainty
- contamination-aware leaderboard handling

Official benchmark expansion MUST NOT depend primarily on:

- free-form LLM judging
- public-only scenario growth without hidden counterparts
- single-run reporting
- static prompt collections without executable state changes
- benchmark-specific shortcuts that are not operator-quality behavior

## 3. What counts as valid coverage expansion

Valid expansion includes:

- new scenario families in under-covered startup functions
- richer causal mechanics inside the world model
- new evaluator components that remain auditable
- new hidden pack families or deeper hidden-pack breadth
- stronger constraint logic for survival, trust, compliance, or collateral damage
- track-balanced additions that reduce crisis overconcentration

Examples of high-value expansion areas:

- `0to1` and PMF search
- fundraising, debt, and cap-table mechanics
- growth experimentation and launch quality
- people leadership and executive management quality
- legal and regulatory progression
- long-horizon strategy and delayed consequences

## 4. What does not count

The following SHOULD NOT be treated as benchmark-strength coverage gains on their own:

- adding only public scenarios
- adding only surface-level tool names without runtime support
- adding only prose rubrics without executable evaluator changes
- adding scenarios that duplicate existing archetypes with cosmetic changes
- increasing scenario count without hidden-pack separation or validation
- replacing state checks with subjective grading for convenience

## 5. Expansion bar for new scenario families

A new scenario family SHOULD satisfy all of the following before being described as benchmark-grade:

1. It covers a real startup operating problem not already well represented.
2. It introduces meaningful tradeoffs rather than one obvious optimal move.
3. It has delayed or collateral consequences, not only immediate rewards.
4. It uses the canonical state model or a justified track extension.
5. It has programmatic evaluator logic for the majority of score impact.
6. It has at least one hidden `test` or `fresh` counterpart before official promotion.
7. It has exploit review notes if the action pattern is gameable.
8. It is understandable and directionally aligned with operator judgment.

## 6. Evaluator policy for new coverage

New coverage SHOULD prefer one of two paths:

- extend existing programmatic components with new measurable state
- add a new explicit component with clear normalization, weights, and constraints

Semantic judging MAY be added for artifacts such as:

- board updates
- customer communications
- hiring plans

But only if all of the following hold:

- it is rubric-bound
- evaluator versioning is explicit
- rationale metadata is retained
- it remains a minority share of the total score
- the scenario still stands on programmatic state-based evaluation

If a new area cannot be scored mostly through executable state and bounded rubrics, it SHOULD remain draft-only until the evaluation path is stronger.

## 7. Hidden-pack requirements for expansion

Any coverage area that becomes part of an official claim SHOULD have hidden-eval support.

Minimum expectation:

- public `dev` scenarios for iteration
- hidden `test` scenarios for stable official scoring
- hidden `fresh` scenarios for contamination-resistant reporting windows when practical

Hidden variants MUST measure transfer, not memorization. They SHOULD differ in:

- initial conditions
- event timing
- latent causes
- thresholds
- action tradeoffs

## 8. Calibration and promotion policy

No scenario family should be promoted from draft expansion to official benchmark coverage without calibration evidence.

Promotion expectations:

1. validation and lint pass
2. baseline smoke coverage
3. hidden-pack placement decision
4. exploit review
5. synthetic calibration if used internally
6. operator review on a representative sample
7. adjudication of major score disagreements

If operator judgment and benchmark scores materially diverge, the correct action is to revise the scenario or evaluator, not to quietly lower the bar.

## 9. Coverage balance policy

Coverage expansion SHOULD improve balance across startup success domains, not just increase total count.

Maintainers SHOULD monitor whether the corpus overweights:

- crisis response
- finance survival
- one-step operational fixes

Maintainers SHOULD intentionally add underrepresented areas such as:

- PMF discovery
- growth systems
- product strategy
- people leadership
- board truth-telling
- legal and regulatory drag

## 10. Runtime and tool-surface policy

A coverage claim is stronger when the runtime, tools, scenarios, and evaluators all support it.

New coverage SHOULD NOT rely on tool-catalog surface area alone. If a new domain is exposed in official scenarios, the reference runtime or official scaffold SHOULD implement it, and tests SHOULD exercise it.

Tool additions SHOULD come with:

- runtime behavior
- schema-valid traces
- evaluator relevance
- regression tests

## 11. Versioning and governance policy

Coverage expansion MUST respect benchmark version boundaries.

Use version bumps when expansion changes:

- scoring semantics
- official scenario distribution
- hidden-pack composition
- required artifacts
- leaderboard comparability

Do not merge leaderboard results across incompatible benchmark or pack versions without a visible boundary.

## 12. Practical expansion workflow

Recommended sequence:

1. identify the missing startup-success area
2. define the state additions and causal mechanics
3. add draft `dev` scenarios
4. add or extend programmatic evaluators and constraints
5. add runtime support for any new official tools
6. add tests, smoke paths, and baseline checks
7. author distinct hidden `test` and `fresh` variants as appropriate
8. run exploit review and calibration review
9. document promotion, versioning, and pack lifecycle impact

## 13. Current implication for TheStartupBench

For the current repository state, the right next move is to expand coverage in areas such as PMF search, fundraising, growth experimentation, people leadership, and legal progression while keeping the current benchmark philosophy unchanged.

The standard is:

- broader coverage
- deeper realism
- same or stricter benchmark discipline

Not:

- broader coverage at the cost of rigor
