import pandas as pd

from config import TRAINING_DATA_PATH


def load_training_data() -> pd.DataFrame:
    """Load the provided training CSV dataset."""
    return pd.read_csv(TRAINING_DATA_PATH)


def validate_training_data(data: pd.DataFrame) -> None:
    """Validate the basic structure of the training dataset."""
    required_columns = {"text", "intent", "confidence"}

    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )


if __name__ == "__main__":
    training_data = load_training_data()
    validate_training_data(training_data)

    print("Training data loaded successfully.")
    print(f"Rows: {len(training_data)}")
    print(f"Columns: {training_data.columns.tolist()}")