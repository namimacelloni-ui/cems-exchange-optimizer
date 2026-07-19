from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/raw/cems_universities.csv")


def load_university_data() -> pd.DataFrame:
    """Load the raw CEMS university dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {DATA_PATH.resolve()}"
        )

    data = pd.read_csv(DATA_PATH)

    if data.empty:
        raise ValueError("The university dataset is empty.")

    return data


if __name__ == "__main__":
    universities = load_university_data()

    print("Dataset loaded successfully.")
    print(f"Number of universities: {len(universities)}")
    print(f"Number of variables: {len(universities.columns)}")
    print("\nAvailable columns:")
    print(universities.columns.tolist())
