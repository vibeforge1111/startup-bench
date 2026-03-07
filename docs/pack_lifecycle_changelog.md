# TheStartupBench Pack Lifecycle Changelog

Last updated: 2026-03-07

This document is the public-facing summary of hidden-pack promotions, fresh-pack creation, and retirement events. The machine-readable source of truth is [public_pack_changelog.json](/C:/Users/USER/Desktop/startup-bench/examples/public_pack_changelog.json).

## Active packs

- `real-world-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [real_world_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_test_manifest.json)
  - status: active, clean

- `real-world-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [real_world_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/real_world_public_fresh_manifest.json)
  - status: active, clean

- `operator-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - public manifest: [operator_public_test_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_public_test_manifest.json)
  - status: active, clean

- `operator-fresh-pack-0.1.0`
  - split: `fresh`
  - visibility: `hidden`
  - public manifest: [operator_public_fresh_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_public_fresh_manifest.json)
  - status: active, clean

## Retired packs

- `private-test-pack-0.1.0`
  - split: `test`
  - visibility: `hidden`
  - status: retired
  - successor: `real-world-test-pack-0.1.0`

## Operational notes

- `fresh` packs are intended for short-lived, contamination-resistant reporting windows.
- Promotions and retirements should update both this document and [public_pack_changelog.json](/C:/Users/USER/Desktop/startup-bench/examples/public_pack_changelog.json).
- If a hidden pack is leaked or materially inferable, mark it contaminated in the JSON changelog, retire it, and publish the successor pack manifest.
