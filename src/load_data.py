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


CATEGORY_COLUMN_MAP = {
    "academic": "academic_score",
    "career": "career_score",
    "lifestyle": "lifestyle_score",
    "international": "international_score",
    "english_friendliness": "english_friendliness_score",
}


def validate_cost_data(costs: pd.DataFrame) -> None:
    """Validate the structured monthly-cost dataset."""

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

    missing_columns = required_cost_columns.difference(
        costs.columns
    )

    if missing_columns:
        raise ValueError(
            "The cost dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if costs.empty:
        raise ValueError("The cost estimate dataset is empty.")

    if costs["school_name"].duplicated().any():
        duplicated_schools = costs.loc[
            costs["school_name"].duplicated(),
            "school_name",
        ].tolist()

        raise ValueError(
            "Duplicate schools found in the cost dataset: "
            f"{duplicated_schools}"
        )


def add_housing_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a housing-practicality score from structured cost data.

    The score combines:
    - affordability: 80%
    - cost predictability: 20%

    Lower typical housing cost receives a higher score.
    A smaller gap between low and high estimates receives a higher score.
    """

    minimum_typical_cost = data["housing_typical_eur"].min()
    maximum_typical_cost = data["housing_typical_eur"].max()

    typical_cost_range = (
        maximum_typical_cost - minimum_typical_cost
    )

    if typical_cost_range == 0:
        data["housing_affordability_component"] = 100.0
    else:
        data["housing_affordability_component"] = (
            100
            * (
                maximum_typical_cost
                - data["housing_typical_eur"]
            )
            / typical_cost_range
        )

    data["housing_cost_spread_eur"] = (
        data["housing_high_eur"]
        - data["housing_low_eur"]
    )

    minimum_spread = data["housing_cost_spread_eur"].min()
    maximum_spread = data["housing_cost_spread_eur"].max()

    spread_range = maximum_spread - minimum_spread

    if spread_range == 0:
        data["housing_predictability_component"] = 100.0
    else:
        data["housing_predictability_component"] = (
            100
            * (
                maximum_spread
                - data["housing_cost_spread_eur"]
            )
            / spread_range
        )

    data["housing_score_component"] = (
        0.80 * data["housing_affordability_component"]
        + 0.20 * data["housing_predictability_component"]
    )

    data["housing_score"] = (
        1 + data["housing_score_component"] / 25
    )

    return data


def merge_component_scores(
    data: pd.DataFrame,
    category_scores: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge every available component-based category score.

    Component scores use a 0–100 scale. They are converted to the
    existing 1–5 scale so the current ranking system remains compatible.
    """

    for category, score_column in CATEGORY_COLUMN_MAP.items():
        category_data = category_scores[
            category_scores["category"] == category
        ][
            [
                "school_name",
                "category_score",
            ]
        ].copy()

        if category_data.empty:
            continue

        component_column = f"{score_column}_component"

        category_data = category_data.rename(
            columns={
                "category_score": component_column,
            }
        )

        data = data.merge(
            category_data,
            on="school_name",
            how="left",
            validate="one_to_one",
        )

        missing_scores = data.loc[
            data[component_column].isna(),
            "school_name",
        ].tolist()

        if missing_scores:
            raise ValueError(
                f"Missing component-based {category} scores for: "
                f"{missing_scores}"
            )

        data[score_column] = (
            1 + data[component_column] / 25
        )

    return data


def load_university_data() -> pd.DataFrame:
    """
    Load university, cost and component-score data.

    Housing scores are calculated directly from structured housing costs.
    Other component categories are loaded from score_components.csv.
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

    validate_cost_data(costs)

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

    data = add_housing_score(data)

    score_components = load_score_components()

    category_scores = calculate_category_scores(
        score_components
    )

    data = merge_component_scores(
        data=data,
        category_scores=category_scores,
    )

    return data


if __name__ == "__main__":
    university_data = load_university_data()

    print("Datasets loaded and merged successfully.")
    print(f"Number of universities: {len(university_data)}")

    display_columns = [
        "school_name",
        "housing_typical_eur",
        "housing_affordability_component",
        "housing_predictability_component",
        "housing_score_component",
        "housing_score",
        "academic_score_component",
        "career_score_component",
    ]

    available_columns = [
        column
        for column in display_columns
        if column in university_data.columns
    ]

    print("\nCurrent component scores and housing data:")

    print(
        university_data[
            available_columns
        ].to_string(index=False)
    )
