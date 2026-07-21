import pandas as pd


SCORE_LABELS = {
    "academic_score_normalized": "academic opportunities",
    "career_score_normalized": "career opportunities",
    "lifestyle_score_normalized": "lifestyle",
    "international_environment_score_normalized": "international environment",
    "english_friendliness_score_normalized": "English friendliness",
    "housing_difficulty_score_normalized": "housing accessibility",
}


def generate_recommendation_explanation(
    university: pd.Series,
    ranked_data: pd.DataFrame,
    weights: dict[str, float],
    maximum_budget: float,
) -> dict[str, list[str]]:
    """
    Generate recommendation strengths and drawbacks using weighted
    contributions, relative performance and budget fit.
    """

    contributions = {}

    for column, label in SCORE_LABELS.items():
        if column in university and pd.notna(university[column]):
            weight = weights.get(column, 0)
            contributions[label] = university[column] * weight

    ranked_contributions = sorted(
        contributions.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    strengths = []
    drawbacks = []

    for label, _ in ranked_contributions[:2]:
        strengths.append(f"Strong match for your {label} priority")

    cost = university.get("monthly_cost_typical_eur")
    cost_low = university.get("monthly_cost_low_eur")
    cost_high = university.get("monthly_cost_high_eur")

    if pd.notna(cost):
        remaining_budget = maximum_budget - cost

        if remaining_budget >= 300:
            strengths.append(
                f"Comfortably within budget, with about €{remaining_budget:.0f} "
                "of monthly flexibility"
            )
        elif remaining_budget >= 0:
            drawbacks.append(
                f"Close to your budget limit, with only about "
                f"€{remaining_budget:.0f} of monthly flexibility"
            )

    if pd.notna(cost_low) and pd.notna(cost_high):
        cost_range = cost_high - cost_low

        if cost_range >= 500:
            drawbacks.append(
                "Actual cost may vary substantially depending on housing"
            )

    for column, label in SCORE_LABELS.items():
        if column not in ranked_data.columns:
            continue

        value = university.get(column)

        if pd.isna(value):
            continue

        average_value = ranked_data[column].mean()

        if value < average_value:
            drawbacks.append(
                f"Below the current shortlist average for {label}"
            )

    strengths = list(dict.fromkeys(strengths))
    drawbacks = list(dict.fromkeys(drawbacks))

    return {
        "strengths": strengths[:3],
        "drawbacks": drawbacks[:3],
    }
