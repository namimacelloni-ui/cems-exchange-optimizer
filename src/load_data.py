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


def validate_cost_data(costs: pd.DataFrame) -> None:
    """Check that the cost dataset is complete and usable."""

    required_columns = {
        "school_name",
        "housing_low_eur",
        "housing_typical_eur",
        "housing_high_eur",
        "monthly_cost_low_eur",
        "monthly_cost_typical_eur",
        "monthly_cost_high_eur",
    }

    missing_columns = required_columns.difference(costs.columns)

    if missing_columns:
        raise ValueError(
            "The cost dataset is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if costs.empty:
        raise ValueError("The cost dataset is empty.")

    if costs["school_name"].duplicated().any():
        raise ValueError(
            "The cost dataset contains duplicate schools."
        )


def add_housing_score(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate housing convenience from housing cost data.

    The score combines:
    - affordability: 80%
    - predictability of the estimate: 20%

    The final value is stored as housing_difficulty_score because
    that is the column currently expected by the ranking system.

    A value of 1 means housing is relatively easy.
    A value of 5 means housing is relatively difficult.
    """

    data = data.copy()

    minimum_cost = data["housing_typical_eur"].min()
    maximum_cost = data["housing_typical_eur"].max()

    cost_range = maximum_cost - minimum_cost

    if cost_range == 0:
        affordability_score = pd.Series(
            100.0,
            index=data.index,
        )
    else:
        affordability_score = (
            100
            * (
                maximum_cost
                - data["housing_typical_eur"]
            )
            / cost_range
        )

    housing_spread = (
        data["housing_high_eur"]
        - data["housing_low_eur"]
    )

    minimum_spread = housing_spread.min()
    maximum_spread = housing_spread.max()

    spread_range = maximum_spread - minimum_spread

    if spread_range == 0:
        predictability_score = pd.Series(
            100.0,
            index=data.index,
        )
    else:
        predictability_score = (
            100
            * (
                maximum_spread
                - housing_spread
            )
            / spread_range
        )

    housing_convenience_score = (
        0.80 * affordability_score
        + 0.20 * predictability_score
    )

    data["housing_convenience_score"] = (
        housing_convenience_score
    )

    data["housing_difficulty_score"] = (
        5 - housing_convenience_score / 25
    )

    return data


def add_component_score(
    data: pd.DataFrame,
    category_scores: pd.DataFrame,
    category: str,
    target_column: str,
) -> pd.DataFrame:
    """Merge one component-based category into the main dataset."""

    selected_scores = category_scores.loc[
        category_scores["category"] == category,
        ["school_name", "category_score"],
    ].rename(
        columns={
            "category_score": target_column,
        }
    )

    if selected_scores.empty:
        raise ValueError(
            f"No component scores found for category: {category}"
        )

    data = data.merge(
        selected_scores,
        on="school_name",
        how="left",
        validate="one_to_one",
    )

    missing_schools = data.loc[
        data[target_column].isna(),
        "school_name",
    ].tolist()

    if missing_schools:
        raise ValueError(
            f"Missing {category} scores for: {missing_schools}"
        )

    data[target_column] = (
        1 + data[target_column] / 25
    )

    return data


def load_university_data() -> pd.DataFrame:
    """Load the datasets used by the optimizer."""

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
            f"Missing cost estimates for: {missing_costs}"
        )

    data["estimated_monthly_cost_eur"] = (
        data["monthly_cost_typical_eur"]
    )

    data = add_housing_score(data)

    components = load_score_components()
    category_scores = calculate_category_scores(components)

    data = add_component_score(
        data=data,
        category_scores=category_scores,
        category="academic",
        target_column="academic_score",
    )

    data = add_component_score(
        data=data,
        category_scores=category_scores,
        category="career",
        target_column="career_score",
    )

    return data


if __name__ == "__main__":
    university_data = load_university_data()

    columns_to_show = [
        "school_name",
        "academic_score",
        "career_score",
        "housing_typical_eur",
        "housing_convenience_score",
        "housing_difficulty_score",
        "estimated_monthly_cost_eur",
    ]

    print(
        university_data[
            columns_to_show
        ].to_string(index=False)
    )
