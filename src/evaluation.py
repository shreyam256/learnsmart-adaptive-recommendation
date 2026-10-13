
from pathlib import Path
import json
import pandas as pd

from baseline_model import (
    load_data,
    build_baseline,
    recommend_courses
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"
REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    performance, engagement = load_data()

    subject_stats, engagement_stats = build_baseline(
        performance, engagement
    )

    # Test warm-start using an existing student
    student_id = performance["student_id"].iloc[0]

    warm_mode, warm_results = recommend_courses(
        student_id,
        performance,
        subject_stats,
        engagement_stats,
        top_n=5
    )

    # Test cold-start using an unknown student
    cold_mode, cold_results = recommend_courses(
        "NEW-STUDENT-001",
        performance,
        subject_stats,
        engagement_stats,
        top_n=5
    )

    # Basic system checks
    checks = {
        "warm_start_returns_five": len(warm_results) == 5,
        "cold_start_returns_five": len(cold_results) == 5,
        "warm_start_has_no_duplicate_subjects":
            warm_results["subject"].is_unique,
        "cold_start_has_no_duplicate_subjects":
            cold_results["subject"].is_unique,
        "recommendation_scores_are_finite":
            bool(
                pd.concat([
                    warm_results["recommendation_score"],
                    cold_results["recommendation_score"]
                ]).map(lambda x: pd.notna(x) and abs(x) != float("inf")).all()
            )
    }

    results = {
        "students": int(performance["student_id"].nunique()),
        "subjects": int(performance["subject"].nunique()),
        "engagement_records": int(len(engagement)),
        "warm_start_student": student_id,
        "warm_start_recommendations":
            warm_results.to_dict(orient="records"),
        "cold_start_recommendations":
            cold_results.to_dict(orient="records"),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "precision_at_5": None,
        "precision_note": (
            "Not calculated: the provided test cases label at-risk "
            "students, not relevant courses for recommendation."
        )
    }

    output_path = REPORT_DIR / "evaluation_results.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Evaluation completed.")
    print("Warm-start mode:", warm_mode)
    print("Cold-start mode:", cold_mode)
    print("\nChecks:")
    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("\nPrecision@5: NOT YET MEASURED")
    print("Results saved to:", output_path)


if __name__ == "__main__":
    main()