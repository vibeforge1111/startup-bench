# Reviewer Outreach Wave 002

Last updated: 2026-03-08

This file contains ready-to-send outreach copy for the second human calibration wave.

Reference assets:

- Study manifest: [operator_human_review_wave_002_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_002_manifest.json)
- Assignments: [review_assignments.json](/C:/Users/USER/Desktop/startup-bench/tmp_human_wave_002/review_assignments.json)
- Reviewer export manifest: [review_form_export.json](/C:/Users/USER/Desktop/startup-bench/tmp_human_wave_002/review_form_export.json)

## Founder 002

Subject:

`TheStartupBench founder calibration request: wave 002`

Message:

```text
You're part of the second founder/operator calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

This wave focuses on promoted strategy families that were added after the first human review pass. Your job is to review completed benchmark runs and judge whether the automated evaluation matches credible founder-level judgment on truthfulness, sequencing, and financing quality.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- whether the operator told the truth when the board or financing situation got uncomfortable
- whether the run made real multi-quarter tradeoffs instead of reactive cleanup
- whether product, GTM, and capital decisions were sequenced credibly
- whether the benchmark is rewarding real judgment rather than polished artifacts

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if you think the benchmark is rewarding the wrong thing, say so directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\founder_002\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\founder_002\review_form.csv

Return:
- the completed `review_form.csv`
```

## Ops 002

Subject:

`TheStartupBench ops calibration request: wave 002`

Message:

```text
You're part of the second operator calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

This wave focuses on long-horizon strategy slices with financing, incident, execution, and operating-system implications. Your job is to review completed benchmark runs and judge whether the automated evaluation matches credible operating judgment.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- financing realism and capital-quality judgment
- whether risk and trust issues were handled early enough
- whether the operator sequenced execution load credibly over multiple turns
- whether the run avoided passive or benchmark-shaped loops

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if a run looks passive, benchmark-gamed, or operationally unserious, say so directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\ops_002\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\ops_002\review_form.csv

Return:
- the completed `review_form.csv`
```

## Product Or Growth 002

Subject:

`TheStartupBench product-growth calibration request: wave 002`

Message:

```text
You're part of the second product/growth calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

This wave focuses on strategy scenarios where roadmap truth, product readiness, channel sequencing, and adoption proof all matter. Your job is to review completed benchmark runs and judge whether the benchmark's automated evaluation matches credible product and GTM judgment.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- whether the operator made the right roadmap and readiness tradeoff
- whether GTM proof and sequencing choices were credible
- whether customer trust and migration risk were handled with enough seriousness
- whether the run shows real prioritization rather than a mechanical checklist

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if a scenario feels unrealistic or benchmark-gameable, note that directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\product_growth_002\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_002\product_growth_002\review_form.csv

Return:
- the completed `review_form.csv`
```

## Short DM Version

```text
You're assigned to TheStartupBench human calibration wave 002.

Please:
1. Read the attached `review_instructions.md`
2. Fill the attached `review_form.csv`
3. Return the completed CSV

This wave reviews completed strategy-pack runs added after the first human review pass. We want your independent judgment on whether the benchmark's scoring matches real startup decision quality.
```

## Return Path

After reviewers send the forms back:

```powershell
powershell -File scripts/compile_human_review_wave_002.ps1 -CompletedFormsDir <folder-with-returned-csvs>
```

That command will:

- import the completed CSV files into operator-review JSON artifacts
- compile the calibration study report
- write outputs under `tmp_human_wave_002_results`
