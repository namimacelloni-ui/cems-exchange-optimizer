import pandas as pd

from src.explanations import generate_recommendation_explanation


DEFAULT_WEIGHTS = {
    "academic_score_normalized": 0.25,
    "career_score_normalized": 0.20,
    "lifestyle_score_normalized": 0.15,
    "international_environment_score_normalized": 0.15,
    "english_friendliness_score_normalized": 0.15,
    "housing_difficulty_score_normalized": 0.10,
}


def test_explanation_identifies_strengths():
    university = pd.Series(
        {
            "academic_score_normalized": 100,
            "career_score_normalized": 100,
            "lifestyle_score_normalized": 50,
            "international_environment_score_normalized": 75,
            "english_friendliness_score_normalized": 75,
            "housing_difficulty_score_normalized": 25,
            "monthly_cost_typical_eur": 1200,
            "monthly_cost_low_eur": 1050,
            "monthly_cost_high_eur": 1400,
        }
    )

    ranked_data = pd.DataFrame(
        [
            university,
            pd.Series(
                {
                    "academic_score_normalized": 75,
                    "career_score_normalized": 75,
                    "lifestyle_score_normalized": 75,
                    "international_environment_score_normalized": 75,
                    "english_friendliness_score_normalized": 75,
                    "housing_difficulty_score_normalized": 50,
                    "monthly_cost_typical_eur": 1300,
                    "monthly_cost_low_eur": 1100,
                    "monthly_cost_high_eur": 1500,
                }
            ),
        ]
    )

    explanation = generate_recommendation_explanation(
        university=university,
        ranked_data=ranked_data,
        weights=DEFAULT_WEIGHTS,
        maximum_budget=1800,
    )

    assert len(explanation["strengths"]) >= 2
    assert any(
        "academic opportunities" in strength
        for strength in explanation["strengths"]
    )


def test_easy_housing_is_treated_as_positive():
    university = pd.Series(
        {
            "academic_score_normalized": 50,
            "career_score_normalized": 50,
            "lifestyle_score_normalized": 50,
            "international_environment_score_normalized": 50,
            "english_friendliness_score_normalized": 50,
            "housing_difficulty_score_normalized": 100,
            "monthly_cost_typical_eur": 900,
            "monthly_cost_low_eur": 800,
            "monthly_cost_high_eur": 1000,
        }
    )

    ranked_data = pd.DataFrame([university])

    housing_focused_weights = {
        "academic_score_normalized": 0.10,
        "career_score_normalized": 0.10,
        "lifestyle_score_normalized": 0.10,
        "international_environment_score_normalized": 0.10,
        "english_friendliness_score_normalized": 0.10,
        "housing_difficulty_score_normalized": 0.50,
    }

    explanation = generate_recommendation_explanation(
        university=university,
        ranked_data=ranked_data,
        weights=housing_focused_weights,
        maximum_budget=1500,
    )

    assert any(
        "housing accessibility" in strength
        for strength in explanation["strengths"]
    )


def test_budget_warning_is_generated_when_close_to_limit():
    university = pd.Series(
        {
            "academic_score_normalized": 75,
            "career_score_normalized": 75,
            "lifestyle_score_normalized": 75,
            "international_environment_score_normalized": 75,
            "english_friendliness_score_normalized": 75,
            "housing_difficulty_score_normalized": 50,
            "monthly_cost_typical_eur": 1450,
            "monthly_cost_low_eur": 1200,
            "monthly_cost_high_eur": 1700,
        }
    )

    ranked_data = pd.DataFrame([university])

    explanation = generate_recommendation_explanation(
        university=university,
        ranked_data=ranked_data,
        weights=DEFAULT_WEIGHTS,
        maximum_budget=1500,
    )

    assert any(
        "Close to your budget limit" in drawback
        for drawback in explanation["drawbacks"]
    )
