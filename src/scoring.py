import pandas as pd


POSITIVE_SCORE_COLUMNS = [
    "academic_score",
    "career_score",
    "lifestyle_score",
    "international_environment_score",
    "english_friendliness_score",
]

NEGATIVE_SCORE_COLUMNS = [
    "housing_difficulty_score",
]


def convert_positive_score_to_100(score: float) -> float:
    """
    Convert a positive 1–5 score into a 0–100 score.

    Example:
    1 -> 0
    3 -> 50
    5 -> 100
    """
    if pd.isna(score):
        return float("nan")

    if score < 1 or score > 5:
        raise ValueError("Score must be between 1 and 5.")

    return (score - 1) * 25


def convert_negative_score_to_100(score: float) -> float:
    """
    Convert a negative 1–5 score into a 0–100 score.

    For negative variables, a lower raw value is better.

    Example:
    1 -> 100
    3 -> 50
    5 -> 0
    """
    if pd.isna(score):
        return float("nan")

    if score < 1 or score > 5:
        raise ValueError("Score must be between 1 and 5.")

    return (5 - score) * 25


def add_normalized_scores(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add normalized 0–100 columns to the university dataset.
    """
    normalized_data = data.copy()

    for column in POSITIVE_SCORE_COLUMNS:
        normalized_data[f"{column}_normalized"] = normalized_data[column].apply(
            convert_positive_score_to_100
        )

    for column in NEGATIVE_SCORE_COLUMNS:
        normalized_data[f"{column}_normalized"] = normalized_data[column].apply(
            convert_negative_score_to_100
        )

    return normalized_data
