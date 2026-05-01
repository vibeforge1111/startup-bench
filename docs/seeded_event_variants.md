# Seeded Event Variants

Startup Bench scenarios can now make scheduled events genuinely seed-dependent by adding `seed_variants` to an event.

This is useful when repeated-seed validation should measure more than command repeatability. A scenario can keep the same founder problem while varying the severity, timing pressure, or operational consequences of a scheduled event.

The first public example is `examples/minimal_gtm_seeded_variance_scenario.json`, grouped by `examples/startup_yc_seeded_variance_suite.json`. It keeps the standard GTM channel-reset operating problem but varies the early market shock and later design-partner expansion signal by seed.

## Contract

Each scheduled event may include:

```json
{
  "event_id": "ev_market_001",
  "at_turn": 1,
  "event_type": "market_shock",
  "visible_message": "A market shock hit the pipeline.",
  "operations": [
    { "op": "increment", "path": "market.demand_index", "value": -0.04 }
  ],
  "seed_variants": [
    {
      "variant_id": "soft_shock",
      "weight": 1,
      "visible_message": "A softer market shock hit pipeline quality.",
      "operations": [
        { "op": "increment", "path": "sales.weighted_pipeline_usd", "value": -10000 }
      ]
    },
    {
      "variant_id": "hard_shock",
      "weight": 1,
      "visible_message": "A harder market shock hit pipeline quality.",
      "operations": [
        { "op": "increment", "path": "sales.weighted_pipeline_usd", "value": -60000 }
      ]
    }
  ]
}
```

When the event fires:

- base `operations` or primitive operations still apply,
- one seed variant is selected deterministically from the run seed and event id,
- the selected variant's `operations` and `effects` are applied,
- the visible event includes `seed_variant_id`,
- the same scenario and seed replay the same variant.

## Promotion Discipline

Seeded variants should be used for robustness claims only when the variants change the scored operating problem.

Good uses:

- customer demand shock severity,
- market pricing pressure,
- incident or support-load severity,
- financing window tightening,
- team capacity drag,
- board or customer pressure timing/severity.

Bad uses:

- cosmetic message-only variants,
- variants that do not change world state,
- variants that leak the hidden answer,
- variants that punish one fixed script without modeling a plausible operating uncertainty.

## Interpretation

Repeated-seed reports mean different things depending on the scenario:

- If seed summaries are identical, the run is repeatability evidence.
- If seed summaries differ because seeded variants changed world state, the run is variance evidence.
- If all seeds still win under meaningful variants, the claim can move toward robustness.

Do not call a specialization path "stochastically robust" unless the benchmark actually uses seed-dependent state changes or another randomized event model.
