from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

UNIVERSITIES_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cems_universities.csv"
)

COST_ESTIMATES_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cost_estimates.csv"
)


def load_university_data() -> pd.DataFrame:
    """
    Load the university dataset and merge the improved cost estimates.

    The app continues to use `estimated_monthly_cost_eur`, but this
    value is updated using `monthly_cost_typical_eur` from the new
    structured cost dataset.
    """

    if not UNIVERSITIES_PATH.exists():
        raise FileNotFoundError(
            f"University dataset not found at: {UNIVERSITIES_PATH}"
        )

    if not COST_ESTIMATES_PATH.exists():
        raise FileNotFoundError(
            f"Cost dataset not found at: {COST_ESTIMATES_PATH}"
        )

    universities = pd.read_csv(UNIVERSITIES_PATH)
    costs = pd.read_csv(COST_ESTIMATES_PATH)

    if universities.empty:
        raise ValueError("The university dataset is empty.")

    if costs.empty:
        raise ValueError("The cost estimate dataset is empty.")

    required_cost_columns = {
        "school_name",
        "housing_low_eur",
        "housing_typical_eur",
        "housing_high_eur",
        "monthly_cost_low_eur",
        "monthly_cost_typical_eur",
        "monthly_cost_high_eur",
        "confidence_level",
    }

    missing_columns = required_cost_columns.difference(costs.columns)

    if missing_columns:
        raise ValueError(
            "The cost dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if costs["school_name"].duplicated().any():
        duplicated_schools = costs.loc[
            costs["school_name"].duplicated(),
            "school_name",
        ].tolist()

        raise ValueError(
            "Duplicate schools found in the cost dataset: "
            f"{duplicated_schools}"
        )

    data = universities.merge(
        costs,
        on="school_name",
        how="left",
        validate="one_to_one",
        suffixes=("", "_cost"),
    )

    missing_costs = data.loc[
        data["monthly_cost_typical_eur"].isna(),
        "school_name",
    ].tolist()

    if missing_costs:
        raise ValueError(
            "Missing structured cost estimates for: "
            f"{missing_costs}"
        )

    data["estimated_monthly_cost_eur"] = (
        data["monthly_cost_typical_eur"]
    )

    return data


if __name__ == "__main__":
    university_data = load_university_data()

    print("Datasets loaded and merged successfully.")
    print(f"Number of universities: {len(university_data)}")

    print("\nUpdated monthly costs:")
    print(
        university_data[
            [
                "school_name",
                "monthly_cost_low_eur",
                "monthly_cost_typical_eur",
                "monthly_cost_high_eur",
                "confidence_level",
            ]
        ].to_string(index=False)
    )
