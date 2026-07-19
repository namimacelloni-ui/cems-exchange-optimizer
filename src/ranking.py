import pandas as pd


DEFAULT_WEIGHTS = {
    "academic_score_normalized": 0.25,
    "career_score_normalized": 0.20,
    "lifestyle_score_normalized": 0.15,
    "international_environment_score_normalized": 0.15,
    "english_friendliness_score_normalized": 0.15,
    "housing_difficulty_score_normalized": 0.10,
}


def validate_weights(weights: dict[str, float]) -> None:
    """
    Validate that all weights are non-negative and sum to 1.
    """
    if not weights:
        raise ValueError("Weights cannot be empty.")

    if any(weight < 0 for weight in weights.values()):
        raise ValueError("Weights cannot be negative.")

    if round(sum(weights.values()), 6) != 1:
        raise ValueError("Weights must sum to 1.")


def calculate_weighted_score(
    data: pd.DataFrame,
    weights: dict[str, float] | None = None,
) -> pd.DataFrame:
    """
    Calculate a weighted final score for each university.

    Rows with missing values in one or more scoring columns
    will receive a missing final score.
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    validate_weights(weights)

    missing_columns = [
        column for column in weights
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    ranked_data = data.copy()

    ranked_data["final_score"] = 0.0

    for column, weight in weights.items():
        ranked_data["final_score"] += (
            ranked_data[column] * weight
        )

    return ranked_data.sort_values(
        by="final_score",
        ascending=False,
        na_position="last",
    ).reset_index(drop=True)
