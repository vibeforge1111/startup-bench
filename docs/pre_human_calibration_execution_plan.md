# Pre-Human Calibration Execution Plan

Last updated: 2026-03-07

## Goal

This document defines the next hardening phase before external human/operator calibration begins.

The benchmark is already usable as an internal research benchmark. This phase is about reducing the remaining pre-human risks so the first real operator wave calibrates a stable benchmark rather than a moving target.

## Decision Packet

```json
{
  "stability_score": 0.78,
  "decision": "approve",
  "top_bottleneck": "governance evaluator depth and hidden corpus breadth are still thinner than the rest of the benchmark surface",
  "anti_patterns_detected": [
    {
      "tag": "comfort_zone_optimization",
      "severity": "warn",
      "evidence": [
        "synthetic calibration already corrected the most obvious canary and crisis failures",
        "remaining work should shift from repeated synthetic spot-checking toward realism depth and corpus breadth"
      ],
      "status": "contained"
    },
    {
      "tag": "golden_demo_collapse",
      "severity": "warn",
      "evidence": [
        "board/governance scenarios are still a small family",
        "hidden strategy packs remain illustrative rather than benchmark-scale"
      ],
      "status": "open"
    },
    {
      "tag": "ghost_improvement",
      "severity": "warn",
      "evidence": [
        "packaging, docs, and workflow depth now exceed corpus scale",
        "additional infrastructure should be secondary to evaluator and scenario realism"
      ],
      "status": "contained"
    }
  ],
  "guardrail_status": {
    "schema_gate": "pass",
    "lineage_gate": "pass",
    "complexity_gate": "warn",
    "transfer_gate": "pass",
    "memory_hygiene_gate": "pass",
    "human_gate": "pass"
  },
  "pillar_assessment": {
    "causal_anchor": {
      "status": "pass",
      "evidence": [
        "remaining mutations are tied to the governance watchlist and hidden corpus scale gaps documented in calibration_outcomes.md and benchmark_status.md"
      ]
    },
    "cross_pollination": {
      "status": "pass",
      "evidence": [
        "the next mutations reuse proven trace-aware evaluator patterns from canary and crisis calibration rather than introducing a new scoring subsystem"
      ]
    },
    "entropy_filter": {
      "status": "warn",
      "evidence": [
        "board/governance depth should be added with narrow penalties and one scenario-pair expansion, not a broad evaluator rewrite"
      ]
    },
    "surprise_priority": {
      "status": "pass",
      "evidence": [
        "governance and hidden-corpus breadth are currently the highest-surprise remaining surfaces",
        "human onboarding is intentionally deferred, so pre-human work should focus there"
      ]
    }
  },
  "required_fixes_before_approve": [],
  "next_experiments": [
    "add a trace-aware governance penalty for board-track runs that stay templated or fail to respond to governance pressure events",
    "expand the hidden strategy family with one additional board/finance conflict pair",
    "improve long-horizon baseline board communication so it is less boilerplate and more state-aware",
    "refresh status docs and release notes after the new hardening wave lands"
  ],
  "risk_if_ignored": "the first human calibration wave will spend time discovering already-known governance and corpus-breadth weaknesses instead of validating benchmark quality"
}
```

## Workstreams

### 1. Governance evaluator depth

Objective:

- make `board` scenarios score real governance quality rather than only generic strategic coherence

Tasks:

- add trace-aware board penalties for repeated templated updates
- penalize missed follow-up after board-pressure and customer-pushback events
- penalize unresolved incident/governance issues when the track is explicitly `board`
- keep the mutation narrow and regression-tested

Exit criteria:

- the current board watchlist scenario remains directionally healthy
- governance quality becomes more inspectable in score details

### 2. Hidden strategy corpus expansion

Objective:

- increase hidden board-family coverage before human reviewers arrive

Tasks:

- add one new hidden board scenario to the `test` strategy pack
- add one distinct fresh counterpart to the `fresh` strategy pack
- keep both distinct at the id, file, and latent-conflict levels
- extend suite tests and family-integrity checks

Exit criteria:

- strategy hidden packs are broader than one board slice
- board/governance conclusions are less likely to hinge on one scenario

### 3. Baseline realism improvement

Objective:

- reduce repeated boilerplate behavior in long-horizon governance runs

Tasks:

- make `heuristic_long_horizon_operator` board updates state-aware
- vary asks and summaries based on trust, backlog, incidents, financing pressure, and runway
- preserve deterministic baseline behavior

Exit criteria:

- baseline traces show less repeated boilerplate in board scenarios
- stronger baseline behavior is available for the expanded hidden board pack

### 4. Release packaging

Objective:

- turn the pre-human state into a clear milestone rather than an implicit checkpoint

Tasks:

- refresh benchmark status and calibration docs
- keep a short list of remaining post-pre-human tasks:
  - human/operator review wave
  - adjudication on any disagreements
  - release candidate freeze

Exit criteria:

- the repo clearly distinguishes pre-human hardening from post-human calibration

## Order Of Execution

1. governance evaluator depth
2. hidden strategy corpus expansion
3. baseline realism improvement
4. docs and release packaging

## Out Of Scope For This Phase

These are deliberately deferred until after this pre-human hardening wave:

- recruiting and onboarding the real review taskforce
- leaderboard launch claims
- large-scale corpus generation
- cap-table/debt model expansion
- new semantic judge lanes
