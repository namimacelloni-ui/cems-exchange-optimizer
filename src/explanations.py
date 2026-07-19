import pandas as pd


SCORE_LABELS = {
    "academic_score": "academic opportunities",
    "career_score": "career opportunities",
    "lifestyle_score": "lifestyle",
    "international_environment_score": "international environment",
    "english_friendliness_score": "English friendliness",
}

LOWER_IS_BETTER_LABELS = {
    "housing_difficulty_score": "housing accessibility",
}


def generate_recommendation_explanation(
    university: pd.Series,
) -> dict[str, list[str]]:
    """
    Identify the strongest and weakest aspects of a university.

    Returns a dictionary containing strengths and drawbacks.
    """
    positive_scores = {
        label: university[column]
        for column, label in SCORE_LABELS.items()
        if column in university and pd.notna(university[column])
    }

    if (
        "housing_difficulty_score" in university
        and pd.notna(university["housing_difficulty_score"])
    ):
        housing_convenience = 6 - university["housing_difficulty_score"]
        positive_scores["housing accessibility"] = housing_convenience

    ranked_scores = sorted(
        positive_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    strengths = [
        f"Strong {label}"
        for label, _ in ranked_scores[:2]
    ]

    drawbacks = [
        f"Relatively weaker {label}"
        for label, _ in ranked_scores[-2:]
    ]

    return {
        "strengths": strengths,
        "drawbacks": drawbacks,
    }
