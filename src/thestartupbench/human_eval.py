"""Human calibration artifact helpers."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from .validation import validate_artifact_file, validate_instance


RUBRIC_KEYS = (
    "survival_and_risk",
    "capital_allocation",
    "customer_trust",
    "people_leadership",
    "strategic_quality",
)

RECOMMENDATION_ORDER = ("pass", "borderline", "fail")


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def aggregate_operator_reviews(review_paths: list[Path]) -> dict:
    if not review_paths:
        raise ValueError("At least one operator review is required.")

    reviews: list[dict] = []
    review_validations = []
    for path in review_paths:
        review = _load_json(path)
        validation = validate_instance(
            artifact_type="operator-review",
            instance=review,
            path=path,
        )
        review_validations.append(validation.to_dict())
        if not validation.ok:
            return {
                "summary": None,
                "validation": {
                    "artifact_type": "operator-review-summary",
                    "path": "operator_review_summary.json",
                    "schema_name": "tsb_operator_review_summary.schema.json",
                    "ok": False,
                    "issues": validation.to_dict()["issues"],
                },
                "review_validations": review_validations,
            }
        reviews.append(review)

    scenario_buckets: dict[tuple[str, str], list[dict]] = defaultdict(list)
    rubric_totals = {key: 0.0 for key in RUBRIC_KEYS}
    recommendation_counter: Counter[str] = Counter()
    reviewer_ids: set[str] = set()
    pack_versions: set[str] = set()

    for review in reviews:
        scenario = review["scenario"]
        key = (scenario["scenario_id"], scenario["track"])
        scenario_buckets[key].append(review)
        recommendation = review["rubric"]["overall_recommendation"]
        recommendation_counter[recommendation] += 1
        reviewer_ids.add(review["reviewer"]["reviewer_id"])
        pack_versions.add(scenario["scenario_pack_version"])
        for rubric_key in RUBRIC_KEYS:
            rubric_totals[rubric_key] += review["rubric"][rubric_key]

    scenario_summaries = []
    for (scenario_id, track), bucket in sorted(scenario_buckets.items()):
        local_recommendations = Counter(item["rubric"]["overall_recommendation"] for item in bucket)
        mean_scores = {
            rubric_key: round(sum(item["rubric"][rubric_key] for item in bucket) / len(bucket), 4)
            for rubric_key in RUBRIC_KEYS
        }
        scenario_summaries.append(
            {
                "scenario_id": scenario_id,
                "track": track,
                "review_count": len(bucket),
                "mean_scores": mean_scores,
                "recommendation_distribution": {
                    name: local_recommendations.get(name, 0) for name in RECOMMENDATION_ORDER
                },
                "disagreement_flag": len([name for name, count in local_recommendations.items() if count > 0]) > 1,
            }
        )

    summary = {
        "summary_version": "0.1.0",
        "benchmark_version": reviews[0]["benchmark_version"],
        "scenario_pack_versions": sorted(pack_versions),
        "review_count": len(reviews),
        "reviewer_count": len(reviewer_ids),
        "scenario_count": len(scenario_summaries),
        "overall": {
            "mean_scores": {
                rubric_key: round(rubric_totals[rubric_key] / len(reviews), 4)
                for rubric_key in RUBRIC_KEYS
            },
            "recommendation_distribution": {
                name: recommendation_counter.get(name, 0) for name in RECOMMENDATION_ORDER
            },
        },
        "scenario_summaries": scenario_summaries,
    }
    validation = validate_instance(
        artifact_type="operator-review-summary",
        instance=summary,
        path=Path("operator_review_summary.json"),
    )
    return {
        "summary": summary,
        "validation": validation.to_dict(),
        "review_validations": review_validations,
    }


def validate_operator_review(path: Path) -> dict:
    return validate_artifact_file(artifact_type="operator-review", path=path).to_dict()
