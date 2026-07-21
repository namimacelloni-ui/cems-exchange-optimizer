from pathlib import Path

import pandas as pd

from src.component_scores import (
    calculate_category_scores,
    load_score_components,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

UNIVERSITIES_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cems_universities.csv"
)

COST_ESTIMATES_PATH = (
    PROJECT_ROOT / "data" / "raw" / "cost_estimates.csv"
)


def load_university_data() -> pd.DataFrame:
    """
    Load and merge university, cost and component-score data.

    Structured monthly costs replace the original prototype costs.

    Academic and career component scores are converted from 0–100
    to the equivalent 1–5 scale so the existing scoring pipeline
    remains compatible.
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

    missing_cost_columns = required_cost_columns.difference(
        costs.columns
    )

    if missing_cost_columns:
        raise ValueError(
            "The cost dataset is missing required columns: "
            f"{sorted(missing_cost_columns)}"
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

    score_components = load_score_components()

    category_scores = calculate_category_scores(
        score_components
    )

    academic_scores = category_scores[
        category_scores["category"] == "academic"
    ][
        [
            "school_name",
            "category_score",
        ]
    ].rename(
        columns={
            "category_score": "academic_score_component",
        }
    )

    data = data.merge(
        academic_scores,
        on="school_name",
        how="left",
        validate="one_to_one",
    )

    missing_academic_scores = data.loc[
        data["academic_score_component"].isna(),
        "school_name",
    ].tolist()

    if missing_academic_scores:
        raise ValueError(
            "Missing component-based academic scores for: "
            f"{missing_academic_scores}"
        )

    data["academic_score"] = (
        1 + data["academic_score_component"] / 25
    )

    career_scores = category_scores[
        category_scores["category"] == "career"
    ][
        [
            "school_name",
            "category_score",
        ]
    ].rename(
        columns={
            "category_score": "career_score_component",
        }
    )

    data = data.merge(
        career_scores,
        on="school_name",
        how="left",
        validate="one_to_one",
    )

    missing_career_scores = data.loc[
        data["career_score_component"].isna(),
        "school_name",
    ].tolist()

    if missing_career_scores:
        raise ValueError(
            "Missing component-based career scores for: "
            f"{missing_career_scores}"
        )

    data["career_score"] = (
        1 + data["career_score_component"] / 25
    )

    return data


if __name__ == "__main__":
    university_data = load_university_data()

    print("Datasets loaded and merged successfully.")
    print(f"Number of universities: {len(university_data)}")

    print("\nUpdated academic, career and monthly cost data:")

    print(
        university_data[
            [
                "school_name",
                "academic_score_component",
                "academic_score",
                "career_score_component",
                "career_score",
                "monthly_cost_low_eur",
                "monthly_cost_typical_eur",
                "monthly_cost_high_eur",
                "confidence_level",
            ]
        ].to_string(index=False)
    )
