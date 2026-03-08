param(
    [string]$SyntheticStudyReportPath = "tmp_model_review_wave_001_results/report/calibration_study_report.json",

    [string]$HumanStudyReportPath = "tmp_human_wave_002_results/report/calibration_study_report.json",

    [string]$OutputDir = "tmp_model_human_wave_002_comparison"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $SyntheticStudyReportPath)) {
    throw "Synthetic study report not found: $SyntheticStudyReportPath"
}

if (-not (Test-Path $HumanStudyReportPath)) {
    throw "Human study report not found: $HumanStudyReportPath"
}

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$pythonScript = @"
import json
from pathlib import Path

synthetic_study_report_path = Path(r'''$SyntheticStudyReportPath''')
human_study_report_path = Path(r'''$HumanStudyReportPath''')
output_dir = Path(r'''$OutputDir''')
output_dir.mkdir(parents=True, exist_ok=True)

synthetic_study = json.loads(synthetic_study_report_path.read_text(encoding='utf-8'))
human_study = json.loads(human_study_report_path.read_text(encoding='utf-8'))

synthetic_target_path = Path(synthetic_study['target_reports'][0]['calibration_report_path'])
human_target_path = Path(human_study['target_reports'][0]['calibration_report_path'])

synthetic_target = json.loads(synthetic_target_path.read_text(encoding='utf-8'))
human_target = json.loads(human_target_path.read_text(encoding='utf-8'))

synthetic_lookup = {item['scenario_id']: item for item in synthetic_target['scenario_alignments']}
human_lookup = {item['scenario_id']: item for item in human_target['scenario_alignments']}

comparison_rows = []
for scenario_id in sorted(set(synthetic_lookup) & set(human_lookup)):
    synthetic = synthetic_lookup[scenario_id]
    human = human_lookup[scenario_id]
    comparison_rows.append({
        'scenario_id': scenario_id,
        'track': human['track'],
        'benchmark_recommendation': human['benchmark_recommendation'],
        'synthetic_recommendation': synthetic['operator_recommendation'],
        'human_recommendation': human['operator_recommendation'],
        'synthetic_mean_rubric': synthetic['operator_mean_rubric'],
        'human_mean_rubric': human['operator_mean_rubric'],
        'human_minus_synthetic_rubric': round(float(human['operator_mean_rubric']) - float(synthetic['operator_mean_rubric']), 4),
        'synthetic_absolute_rubric_gap': synthetic['absolute_rubric_gap'],
        'human_absolute_rubric_gap': human['absolute_rubric_gap'],
        'synthetic_disagreement_flag': bool(synthetic['disagreement_flag']),
        'human_disagreement_flag': bool(human['disagreement_flag']),
        'recommendation_match': synthetic['operator_recommendation'] == human['operator_recommendation'],
    })

high_gap = [row for row in comparison_rows if abs(row['human_minus_synthetic_rubric']) >= 0.5]
recommendation_mismatches = [row for row in comparison_rows if not row['recommendation_match']]

result = {
    'comparison_version': '0.1.0',
    'synthetic_study_report_path': str(synthetic_study_report_path),
    'human_study_report_path': str(human_study_report_path),
    'scenario_count': len(comparison_rows),
    'synthetic_overall': synthetic_study['overall'],
    'human_overall': human_study['overall'],
    'promotion_gate_status': {
        'synthetic': synthetic_study['promotion_gate_status'],
        'human': human_study['promotion_gate_status'],
    },
    'recommendation_mismatch_count': len(recommendation_mismatches),
    'high_rubric_gap_count': len(high_gap),
    'scenario_comparisons': comparison_rows,
}

json_path = output_dir / 'model_vs_human_gap_report.json'
json_path.write_text(json.dumps(result, indent=2) + '\\n', encoding='utf-8')

lines = [
    '# Model vs Human Gap Report',
    '',
    f"Synthetic study report: `{synthetic_study_report_path}`",
    f"Human study report: `{human_study_report_path}`",
    '',
    '## Overall',
    '',
    f"- synthetic mean absolute rubric gap: `{synthetic_study['overall']['mean_absolute_rubric_gap']}`",
    f"- human mean absolute rubric gap: `{human_study['overall']['mean_absolute_rubric_gap']}`",
    f"- synthetic recommendation agreement rate: `{synthetic_study['overall']['recommendation_agreement_rate']}`",
    f"- human recommendation agreement rate: `{human_study['overall']['recommendation_agreement_rate']}`",
    f"- recommendation mismatch count: `{len(recommendation_mismatches)}`",
    f"- high rubric-gap count (`|human - synthetic| >= 0.5`): `{len(high_gap)}`",
    '',
    '## Scenario Comparison',
    '',
    '| Scenario | Track | Benchmark | Synthetic | Human | Synthetic Rubric | Human Rubric | Human - Synthetic | Match |',
    '|---|---|---|---|---|---:|---:|---:|---|',
]

for row in comparison_rows:
    lines.append(
        f"| `{row['scenario_id']}` | `{row['track']}` | `{row['benchmark_recommendation']}` | `{row['synthetic_recommendation']}` | `{row['human_recommendation']}` | `{row['synthetic_mean_rubric']}` | `{row['human_mean_rubric']}` | `{row['human_minus_synthetic_rubric']}` | `{str(row['recommendation_match']).lower()}` |"
    )

if recommendation_mismatches:
    lines.extend([
        '',
        '## Recommendation Mismatches',
        '',
    ])
    for row in recommendation_mismatches:
        lines.append(
            f"- `{row['scenario_id']}`: synthetic=`{row['synthetic_recommendation']}`, human=`{row['human_recommendation']}`, benchmark=`{row['benchmark_recommendation']}`"
        )

if high_gap:
    lines.extend([
        '',
        '## High Rubric Gaps',
        '',
    ])
    for row in high_gap:
        lines.append(
            f"- `{row['scenario_id']}`: synthetic rubric `{row['synthetic_mean_rubric']}`, human rubric `{row['human_mean_rubric']}`, delta `{row['human_minus_synthetic_rubric']}`"
        )

md_path = output_dir / 'model_vs_human_gap_report.md'
md_path.write_text('\\n'.join(lines) + '\\n', encoding='utf-8')

print(json.dumps({
    'json_report_path': str(json_path),
    'markdown_report_path': str(md_path),
    'scenario_count': len(comparison_rows),
    'recommendation_mismatch_count': len(recommendation_mismatches),
    'high_rubric_gap_count': len(high_gap),
}, indent=2))
"@

python -c $pythonScript

Write-Host ""
Write-Host "Completed model-vs-human wave 002 comparison."
Write-Host "Comparison output: $OutputDir"
