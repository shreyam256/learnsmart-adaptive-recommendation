
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"


def load_data():
    performance = pd.read_csv(
        DATA_DIR / "student_performance_clean.csv"
    )
    engagement = pd.read_csv(
        DATA_DIR / "content_engagement_clean.csv"
    )
    return performance, engagement


def build_baseline(performance, engagement):
    # Average performance for each subject
    subject_stats = performance.groupby("subject").agg(
        avg_score=("post_test_score", "mean"),
        avg_completion=("completion_pct", "mean")
    ).reset_index()

    # Lower scores and completion indicate greater learning needs
    subject_stats["recommendation_score"] = (
        0.6 * (1 - subject_stats["avg_score"] / 100)
        + 0.4 * (1 - subject_stats["avg_completion"] / 100)
    )

    # Summarize engagement by student and subject
    engagement_stats = engagement.groupby(
        ["student_id", "subject"]
    ).agg(
        avg_engagement=("engagement_score", "mean"),
        completed_count=("completed", "sum")
    ).reset_index()

    return subject_stats.sort_values(
        "recommendation_score", ascending=False
    ), engagement_stats


def recommend_courses(
    student_id, performance, subject_stats, engagement_stats, top_n=5
):
    student_data = performance[
        performance["student_id"] == student_id
    ]

    if student_data.empty:
        # Cold-start: recommend subjects with the greatest
        # overall learning needs.
        candidates = subject_stats.copy()
        mode = "Cold-start"
    else:
        # Warm-start: prioritize subjects where this student
        # has lower scores and lower completion.
        student_stats = student_data.groupby("subject").agg(
            student_score=("post_test_score", "mean"),
            student_completion=("completion_pct", "mean")
        ).reset_index()

        candidates = subject_stats.merge(
            student_stats, on="subject", how="left"
        )

        candidates["student_need"] = (
            0.6 * (1 - candidates["student_score"] / 100)
            + 0.4 * (1 - candidates["student_completion"] / 100)
        )

        candidates["recommendation_score"] = (
            0.5 * candidates["recommendation_score"]
            + 0.5 * candidates["student_need"].fillna(
                candidates["recommendation_score"]
            )
        )
        mode = "Warm-start"

    # Use engagement as a small adjustment where available
    history = engagement_stats[
        engagement_stats["student_id"] == student_id
    ]

    if not history.empty:
        candidates = candidates.merge(
            history[["subject", "avg_engagement"]],
            on="subject", how="left"
        )
        candidates["recommendation_score"] += (
            0.1 * (1 - candidates["avg_engagement"].fillna(0.5))
        )

    recommendations = candidates.sort_values(
        "recommendation_score", ascending=False
    ).drop_duplicates("subject").head(top_n)

    return mode, recommendations[
        ["subject", "recommendation_score"]
    ]


def main():
    performance, engagement = load_data()
    subject_stats, engagement_stats = build_baseline(
        performance, engagement
    )

    print("Baseline model trained successfully.")
    print("Students:", performance["student_id"].nunique())
    print("Subjects:", performance["subject"].nunique())

    # Warm-start example
    sample_student = performance["student_id"].iloc[0]
    mode, results = recommend_courses(
        sample_student, performance, subject_stats, engagement_stats
    )

    print(f"\n{mode} recommendations for {sample_student}:")
    print(results.to_string(index=False))

    # Cold-start example
    mode, results = recommend_courses(
        "NEW-STUDENT", performance, subject_stats, engagement_stats
    )

    print(f"\n{mode} recommendations:")
    print(results.to_string(index=False))


if __name__ == "__main__":
    main()