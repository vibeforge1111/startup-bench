# TheStartupBench Pack Lifecycle Changelog

Last updated: 2026-03-08

This document is the public-facing summary of hidden-pack promotions, fresh-pack creation, and retirement events. The machine-readable source of truth is [public_pack_changelog.json](/C:/Users/USER/Desktop/startup-bench/examples/public_pack_changelog.json).

## Active packs

- `real-world-test-pack-0.3.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [real_world_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_test_manifest.json)
  - status: active, clean

- `real-world-fresh-pack-0.3.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [real_world_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_fresh_manifest.json)
  - status: active, clean

- `operator-test-pack-0.4.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [operator_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_public_test_manifest.json)
  - status: active, clean

- `operator-fresh-pack-0.4.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [operator_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_public_fresh_manifest.json)
  - status: active, clean

- `strategy-test-pack-0.4.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [strategy_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/strategy_public_test_manifest.json)
  - status: active, clean

- `strategy-fresh-pack-0.4.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [strategy_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/strategy_public_fresh_manifest.json)
  - status: active, clean

- `coverage-test-pack-0.8.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [coverage_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/coverage_public_test_manifest.json)
  - status: active, clean

- `coverage-fresh-pack-0.8.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [coverage_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/coverage_public_fresh_manifest.json)
  - status: active, clean

- `canary-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [canary_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/canary_public_test_manifest.json)
  - status: active, clean

- `canary-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [canary_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/canary_public_fresh_manifest.json)
  - status: active, clean

## Retired packs

- `private-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-test-pack-0.1.0`

- `real-world-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-test-pack-0.2.0`

- `real-world-test-pack-0.2.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-test-pack-0.3.0`

- `real-world-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-fresh-pack-0.2.0`

- `real-world-fresh-pack-0.2.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-fresh-pack-0.3.0`

- `operator-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-test-pack-0.2.0`

- `operator-test-pack-0.2.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-test-pack-0.3.0`

- `operator-test-pack-0.3.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-test-pack-0.4.0`

- `operator-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-fresh-pack-0.2.0`

- `operator-fresh-pack-0.2.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-fresh-pack-0.3.0`

- `operator-fresh-pack-0.3.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `operator-fresh-pack-0.4.0`

- `strategy-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-test-pack-0.2.0`

- `strategy-test-pack-0.2.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-test-pack-0.3.0`

- `strategy-test-pack-0.3.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-test-pack-0.4.0`

- `strategy-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-fresh-pack-0.2.0`

- `strategy-fresh-pack-0.2.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-fresh-pack-0.3.0`

- `strategy-fresh-pack-0.3.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `strategy-fresh-pack-0.4.0`

- `coverage-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.2.0`

- `coverage-test-pack-0.2.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.3.0`

- `coverage-test-pack-0.3.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.4.0`

- `coverage-test-pack-0.4.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.5.0`

- `coverage-test-pack-0.5.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.6.0`

- `coverage-test-pack-0.6.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.7.0`

- `coverage-test-pack-0.7.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-test-pack-0.8.0`

- `coverage-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.2.0`

- `coverage-fresh-pack-0.2.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.3.0`

- `coverage-fresh-pack-0.3.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.4.0`

- `coverage-fresh-pack-0.4.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.5.0`

- `coverage-fresh-pack-0.5.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.6.0`

- `coverage-fresh-pack-0.6.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.7.0`

- `coverage-fresh-pack-0.7.0`
  - split: `fresh`
  - visibility: `hidden`
  - status: retired
  - successor: `coverage-fresh-pack-0.8.0`

## Operational notes

- `fresh` packs are intended for short-lived, contamination-resistant reporting windows.
- Promotions and retirements should update both this document and [public_pack_changelog.json](/C:/Users/USER/Desktop/startup-bench/examples/public_pack_changelog.json).
- If a hidden pack is leaked or materially inferable, mark it contaminated in the JSON changelog, retire it, and publish the successor pack manifest.
