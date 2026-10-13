
from pathlib import Path
import json
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def main():
    performance_path = DATA_DIR / "aiml_student_performance.csv"
    engagement_path = DATA_DIR / "aiml_content_engagement.csv"
    tests_path = DATA_DIR / "aiml_edtech_tests.json"

    # Load datasets
    performance = pd.read_csv(performance_path)
    engagement = pd.read_csv(engagement_path)

    with open(tests_path, "r", encoding="utf-8") as file:
        tests = json.load(file)

    # Inspect original data
    print("\nSTUDENT PERFORMANCE")
    print("Shape:", performance.shape)
    print("Columns:", performance.columns.tolist())
    print(performance.head())

    print("\nCONTENT ENGAGEMENT")
    print("Shape:", engagement.shape)
    print("Columns:", engagement.columns.tolist())
    print(engagement.head())

    print("\nTEST CASES")
    print("Type:", type(tests).__name__)
    print("Number of cases:", len(tests))

    # Standardize column names and remove duplicate rows
    for dataframe in [performance, engagement]:
        dataframe.columns = (
            dataframe.columns.str.strip()
            .str.lower()
            .str.replace(r"[^a-z0-9]+", "_", regex=True)
            .str.strip("_")
        )
        dataframe.drop_duplicates(inplace=True)

    # Save processed datasets
    performance.to_csv(
        PROCESSED_DIR / "student_performance_clean.csv",
        index=False
    )
    engagement.to_csv(
        PROCESSED_DIR / "content_engagement_clean.csv",
        index=False
    )

    with open(
        PROCESSED_DIR / "edtech_tests.json", "w", encoding="utf-8"
    ) as file:
        json.dump(tests, file, indent=2, ensure_ascii=False)

    print("\nPipeline completed successfully.")
    print("Processed files saved in:", PROCESSED_DIR)


if __name__ == "__main__":
    main()