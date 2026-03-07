# Hidden Eval And Refresh Policy

## 1. Purpose

This policy defines how TheStartupBench manages hidden `test` and rolling `fresh` scenario packs so the benchmark remains useful after public release.

## 2. Split meanings

- `dev`: public, stable enough for iteration and baseline building
- `test`: official hidden evaluation pack used for leaderboard scoring
- `fresh`: newly authored hidden scenarios reserved for contamination-resistant reporting windows

## 3. Pack separation rules

Official hidden packs SHOULD NOT reuse public scenario ids.

Hidden scenarios MAY share high-level archetypes with public scenarios, but they SHOULD differ in:

- initial conditions
- event timing
- latent causes
- metric thresholds
- action tradeoffs

The hidden pack should measure transfer, not memorization.

## 4. Minimum hidden-pack metadata

Every hidden pack MUST define:

- `benchmark_version`
- `scenario_pack_version`
- `split`
- scenario ids
- track assignments
- hidden file paths in the private manifest only

The public manifest MUST NOT expose paths, full summaries, or latent-state hints.

## 5. Redaction rules

Public manifests for hidden packs MAY include:

- scenario id
- track
- mode
- hidden reference token

They MUST NOT include:

- scenario file path
- latent state
- detailed summaries
- event schedules
- exact thresholds

## 6. Refresh cadence

Recommended cadence:

- refresh `fresh` every quarter
- promote selected `fresh` scenarios into the next hidden `test` major or minor pack
- retire stale `test` packs once contamination risk becomes material

## 7. Versioning policy

Use separate version lines for:

- benchmark version
- scenario pack version
- scaffold version

Suggested pack semantics:

- patch: metadata-only fix
- minor: hidden scenario additions or replacements within a comparable pack family
- major: evaluation distribution meaningfully changed

Do not merge leaderboard tables across incompatible major pack versions without a visible boundary.

## 8. Promotion pipeline

Recommended promotion path:

1. Author scenario in internal draft form.
2. Run lint and schema validation.
3. Run baseline smoke checks.
4. Run exploit review.
5. Decide whether it belongs in `dev`, `test`, or `fresh`.
6. If promoted to `test` or `fresh`, generate a redacted public manifest.

## 9. Contamination response

If hidden content leaks or becomes too easy to infer:

- mark the affected pack as contaminated
- stop accepting leaderboard submissions for that pack
- generate a successor hidden pack version
- publish a changelog note describing the transition

## 10. Governance recommendations

Maintainers SHOULD keep:

- a private pack registry
- a public changelog of pack promotions and retirements
- exploit notes
- known contamination notes
- a mapping from retired hidden refs to replacement pack versions

## 11. Current repository status

Current repository support now includes:

- public `dev` packs
- hidden `test` suite packaging
- redacted public manifest generation
- a private real-world hidden test pack

What still remains:

- rolling `fresh` pack generation
- explicit retirement ledger
- public contamination changelog
- hidden-pack review checklist automation
