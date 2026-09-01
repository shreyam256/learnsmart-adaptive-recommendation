from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"

# Dataset paths
TRAINING_DATA_PATH = DATA_DIR / "aiml_training_data.csv"
LABELLED_SAMPLES_PATH = DATA_DIR / "aiml_labelled_samples.json"
TEST_CASES_PATH = DATA_DIR / "aiml_test_cases.txt"