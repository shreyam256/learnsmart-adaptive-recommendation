
from pathlib import Path
import json
import warnings

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# --------------------------------------------------
# 1. Project paths and MLflow setup
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = (
    PROJECT_DIR
    / "data"
    / "processed"
    / "student_performance_clean.csv"
)

REPORT_DIR = PROJECT_DIR / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_PATH = REPORT_DIR / "experiment_results.json"

mlflow.set_tracking_uri(
    f"sqlite:///{(PROJECT_DIR / 'mlflow.db').as_posix()}"
)

mlflow.set_experiment("Cynaris_At_Risk_Experiments")


# --------------------------------------------------
# 2. Load and prepare the dataset
# --------------------------------------------------

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    target_column = "label_at_risk"

    if target_column not in df.columns:
        raise ValueError(
            f"Target column '{target_column}' was not found."
        )

    df = df.dropna(subset=[target_column]).copy()

    y = df[target_column]

    # Remove the target and student identifier from features.
    drop_columns = [target_column]

    if "student_id" in df.columns:
        drop_columns.append("student_id")

    X = df.drop(columns=drop_columns)

    if y.nunique() < 2:
        raise ValueError(
            "The target must contain at least two classes."
        )

    return X, y


# --------------------------------------------------
# 3. Build the preprocessing and model pipeline
# --------------------------------------------------

def build_model(X, n_estimators, max_depth):
    categorical_columns = X.select_dtypes(
        include=["object", "category", "str", "string", "bool"]
    ).columns.tolist()

    numerical_columns = [
        column
        for column in X.columns
        if column not in categorical_columns
    ]

    numerical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore"),
            ),
        ]
    )

    transformers = []

    if numerical_columns:
        transformers.append(
            ("numerical", numerical_pipeline, numerical_columns)
        )

    if categorical_columns:
        transformers.append(
            ("categorical", categorical_pipeline, categorical_columns)
        )

    preprocessing = ColumnTransformer(
        transformers=transformers,
        remainder="drop",
    )

    classifier = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessing", preprocessing),
            ("classifier", classifier),
        ]
    )


# --------------------------------------------------
# 4. Train and evaluate one configuration
# --------------------------------------------------

def run_experiment(X_train, X_test, y_train, y_test, config):
    run_name = (
        f"RF_{config['n_estimators']}_{config['max_depth']}"
    )

    print(f"\nStarting experiment: {run_name}")

    with mlflow.start_run(run_name=run_name):
        model = build_model(
            X_train,
            n_estimators=config["n_estimators"],
            max_depth=config["max_depth"],
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        metrics = {
            "accuracy": float(
                accuracy_score(y_test, predictions)
            ),
            "precision": float(
                precision_score(
                    y_test, predictions, average="weighted",
                    zero_division=0
                )
            ),
            "recall": float(
                recall_score(
                    y_test, predictions, average="weighted",
                    zero_division=0
                )
            ),
            "f1_score": float(
                f1_score(
                    y_test, predictions, average="weighted",
                    zero_division=0
                )
            ),
        }

        mlflow.log_params(config)
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("target_column", "label_at_risk")
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)

        mlflow.log_metrics(metrics)

        # The model is created by this script and its types
        # are explicitly trusted for MLflow's skops validation.
        mlflow.sklearn.log_model(
            sk_model=model,
            name="model",
            skops_trusted_types=[
                "numpy.dtype",
                "sklearn.tree._tree.Tree",
            ],
        )

        result = {
            "run_name": run_name,
            "parameters": config,
            "metrics": metrics,
        }

        print(f"Experiment: {run_name}")
        print(f"Metrics: {json.dumps(metrics, indent=2)}")

        return result


# --------------------------------------------------
# 5. Run both configurations and save the results
# --------------------------------------------------

def main():
    print("Loading student performance dataset...")

    X, y = load_data()

    print(f"Dataset rows: {len(X)}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Target classes: {y.nunique()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    configurations = [
        {
            "n_estimators": 100,
            "max_depth": 5,
        },
        {
            "n_estimators": 200,
            "max_depth": 10,
        },
    ]

    results = []

    for config in configurations:
        result = run_experiment(
            X_train,
            X_test,
            y_train,
            y_test,
            config,
        )
        results.append(result)

    best_result = max(
        results,
        key=lambda item: item["metrics"]["f1_score"],
    )

    report = {
        "experiment_name": "Cynaris_At_Risk_Experiments",
        "task": "Student at-risk classification",
        "dataset": str(DATA_PATH.relative_to(PROJECT_DIR)),
        "test_size": 0.2,
        "random_state": 42,
        "number_of_experiments": len(results),
        "experiments": results,
        "best_configuration": best_result,
        "selection_metric": "weighted_f1_score",
    }

    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\n" + "=" * 50)
    print("ALL EXPERIMENTS COMPLETED")
    print("=" * 50)

    print("\nBest configuration:")
    print(json.dumps(best_result, indent=2))

    print(f"\nResults saved to: {RESULTS_PATH}")
    print("Open MLflow to compare both experiment runs.")


if __name__ == "__main__":
    main()