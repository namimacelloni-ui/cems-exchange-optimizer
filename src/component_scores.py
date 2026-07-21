from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCORE_COMPONENTS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "score_components.csv"
)


REQUIRED_COLUMNS = {
    "school_name",
    "category",
    "indicator",
    "normalized_score",
    "weight",
    "weighted_score",
}


def load_score_components() -> pd.DataFrame:
    """Load and validate the score-component dataset."""

    if not SCORE_COMPONENTS_PATH.exists():
        raise FileNotFoundError(
            f"Score-component dataset not found at: "
            f"{SCORE_COMPONENTS_PATH}"
        )

    components = pd.read_csv(SCORE_COMPONENTS_PATH)

    if components.empty:
        raise ValueError("The score-component dataset is empty.")

    missing_columns = REQUIRED_COLUMNS.difference(
        components.columns
    )

    if missing_columns:
        raise ValueError(
            "The score-component dataset is missing columns: "
            f"{sorted(missing_columns)}"
        )

    numeric_columns = [
        "normalized_score",
        "weight",
        "weighted_score",
    ]

    for column in numeric_columns:
        components[column] = pd.to_numeric(
            components[column],
            errors="raise",
        )

    invalid_scores = components[
        ~components["normalized_score"].between(0, 100)
    ]

    if not invalid_scores.empty:
        raise ValueError(
            "Normalized scores must be between 0 and 100."
        )

    invalid_weights = components[
        ~components["weight"].between(0, 1)
    ]

    if not invalid_weights.empty:
        raise ValueError(
            "Indicator weights must be between 0 and 1."
        )

    expected_weighted_scores = (
        components["normalized_score"]
        * components["weight"]
    )

    score_difference = (
        components["weighted_score"]
        - expected_weighted_scores
    ).abs()

    if (score_difference > 0.01).any():
        raise ValueError(
            "One or more weighted scores do not equal "
            "normalized_score multiplied by weight."
        )

    return components


def calculate_category_scores(
    components: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate a 0–100 category score for each school.

    Indicator weights must total 1 within each school and category.
    """

    weight_totals = (
        components
        .groupby(["school_name", "category"])["weight"]
        .sum()
    )

    invalid_weight_totals = weight_totals[
        (weight_totals - 1).abs() > 0.000001
    ]

    if not invalid_weight_totals.empty:
        invalid_groups = [
            f"{school} / {category}: {total:.4f}"
            for (school, category), total
            in invalid_weight_totals.items()
        ]

        raise ValueError(
            "Indicator weights must total 1 for each school "
            "and category. Invalid groups: "
            f"{invalid_groups}"
        )

    category_scores = (
        components
        .groupby(
            ["school_name", "category"],
            as_index=False,
        )["weighted_score"]
        .sum()
        .rename(
            columns={
                "weighted_score": "category_score",
            }
        )
    )

    category_scores["category_score"] = (
        category_scores["category_score"].round(2)
    )

    return category_scores


def get_school_category_score(
    category_scores: pd.DataFrame,
    school_name: str,
    category: str,
) -> float:
    """Return one calculated category score."""

    matching_scores = category_scores[
        (category_scores["school_name"] == school_name)
        & (category_scores["category"] == category)
    ]

    if matching_scores.empty:
        raise ValueError(
            f"No {category} score found for {school_name}."
        )

    if len(matching_scores) > 1:
        raise ValueError(
            f"Multiple {category} scores found for {school_name}."
        )

    return float(
        matching_scores.iloc[0]["category_score"]
    )


if __name__ == "__main__":
    score_components = load_score_components()

    calculated_scores = calculate_category_scores(
        score_components
    )

    print("Category scores calculated successfully.")
    print()
    print(calculated_scores.to_string(index=False))
