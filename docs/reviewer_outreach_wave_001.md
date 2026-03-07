# Reviewer Outreach Wave 001

Last updated: 2026-03-07

This file contains ready-to-send outreach copy for the first human calibration wave.

Reference assets:

- Study manifest: [operator_human_review_wave_001_manifest.json](/C:/Users/USER/Desktop/startup-bench/examples/operator_human_review_wave_001_manifest.json)
- Assignments: [review_assignments.json](/C:/Users/USER/Desktop/startup-bench/tmp_human_wave_assignments/review_assignments.json)
- Reviewer export manifest: [review_form_export.json](/C:/Users/USER/Desktop/startup-bench/tmp_human_wave_forms/review_form_export.json)

## Founder 001

Subject:

`TheStartupBench founder calibration request: wave 001`

Message:

```text
You're part of the first founder/operator calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

Your role is to review completed benchmark runs and judge whether the benchmark's automated evaluation matches credible founder-level judgment.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- survival-quality, not just survival
- capital discipline
- customer trust and stakeholder handling
- strategic coherence under uncertainty
- whether the operator actually made the hard tradeoff the situation required

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if you think the benchmark is rewarding the wrong thing, say so directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\founder_001\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\founder_001\review_form.csv

Return:
- the completed `review_form.csv`
```

## Ops 001

Subject:

`TheStartupBench ops calibration request: wave 001`

Message:

```text
You're part of the first operator calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

Your role is to review completed benchmark runs and judge whether the benchmark's automated evaluation matches credible operating judgment, especially on finance, treasury, resilience, and execution under pressure.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- runway and liquidity judgment
- operational response quality under pressure
- customer trust recovery and incident handling
- whether finance and execution tradeoffs were made explicitly

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if a run looks passive, benchmark-gamed, or operationally unserious, say so directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\ops_001\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\ops_001\review_form.csv

Return:
- the completed `review_form.csv`
```

## Product 001

Subject:

`TheStartupBench product calibration request: wave 001`

Message:

```text
You're part of the first product/operator calibration wave for TheStartupBench, a benchmark for evaluating how well models and agents direct a startup under uncertainty.

Your role is to review completed benchmark runs and judge whether the benchmark's automated evaluation matches credible product and product-strategy judgment.

Please:
1. Read the attached `review_instructions.md`
2. Fill out the attached `review_form.csv`
3. Return the completed CSV

What to optimize for:
- whether the operator chose the right product or quality tradeoff
- whether customer trust and support risk were handled credibly
- whether the run showed real prioritization rather than a mechanical loop

Please review independently:
- do not coordinate scores with other reviewers
- do not try to match the benchmark's score
- if a scenario feels unrealistic or benchmark-gameable, note that directly

Your files:
- Instructions: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\product_001\review_instructions.md
- Form: C:\Users\USER\Desktop\startup-bench\tmp_human_wave_forms\product_001\review_form.csv

Return:
- the completed `review_form.csv`
```

## Short DM Version

```text
You're assigned to TheStartupBench human calibration wave 001.

Please:
1. Read the attached `review_instructions.md`
2. Fill the attached `review_form.csv`
3. Return the completed CSV

This is a review of completed benchmark runs, not a live simulation. We want your independent judgment on whether the benchmark's scoring matches real startup decision quality.
```

## Return Path

After reviewers send the forms back:

```powershell
powershell -File scripts/compile_human_review_wave_001.ps1 -CompletedFormsDir <folder-with-returned-csvs>
```

That command will:

- import the completed CSV files into operator-review JSON artifacts
- compile the calibration study report
- write outputs under `tmp_human_wave_001_results`
