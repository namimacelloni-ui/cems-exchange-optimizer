import pandas as pd

from src.explanations import generate_recommendation_explanation


def test_explanation_identifies_strengths():
    university = pd.Series(
        {
            "academic_score": 5,
            "career_score": 5,
            "lifestyle_score": 3,
            "international_environment_score": 4,
            "english_friendliness_score": 4,
            "housing_difficulty_score": 4,
        }
    )

    explanation = generate_recommendation_explanation(university)

    assert len(explanation["strengths"]) == 2
    assert len(explanation["drawbacks"]) == 2
    assert "Strong academic opportunities" in explanation["strengths"]


def test_easy_housing_is_treated_as_positive():
    university = pd.Series(
        {
            "academic_score": 3,
            "career_score": 3,
            "lifestyle_score": 3,
            "international_environment_score": 3,
            "english_friendliness_score": 3,
            "housing_difficulty_score": 1,
        }
    )

    explanation = generate_recommendation_explanation(university)

    assert "Strong housing accessibility" in explanation["strengths"]
