import pandas as pd
import pytest

from src.ranking import (
    calculate_weighted_score,
    validate_weights,
)


def test_weights_must_sum_to_one():
    invalid_weights = {
        "academic_score_normalized": 0.50,
        "career_score_normalized": 0.30,
    }

    with pytest.raises(ValueError):
        validate_weights(invalid_weights)


def test_weights_cannot_be_negative():
    invalid_weights = {
        "academic_score_normalized": 1.10,
        "career_score_normalized": -0.10,
    }

    with pytest.raises(ValueError):
        validate_weights(invalid_weights)


def test_ranking_orders_highest_score_first():
    sample_data = pd.DataFrame(
        {
            "school_name": ["School A", "School B"],
            "academic_score_normalized": [100, 50],
            "career_score_normalized": [100, 50],
            "lifestyle_score_normalized": [100, 50],
            "international_environment_score_normalized": [100, 50],
            "english_friendliness_score_normalized": [100, 50],
            "housing_difficulty_score_normalized": [100, 50],
        }
    )

    result = calculate_weighted_score(sample_data)

    assert result.loc[0, "school_name"] == "School A"
    assert result.loc[0, "final_score"] == 100
    assert result.loc[1, "school_name"] == "School B"
    assert result.loc[1, "final_score"] == 50


def test_custom_weights_change_ranking():
    sample_data = pd.DataFrame(
        {
            "school_name": ["Academic School", "Career School"],
            "academic_score_normalized": [100, 40],
            "career_score_normalized": [20, 100],
            "lifestyle_score_normalized": [50, 50],
            "international_environment_score_normalized": [50, 50],
            "english_friendliness_score_normalized": [50, 50],
            "housing_difficulty_score_normalized": [50, 50],
        }
    )

    academic_weights = {
        "academic_score_normalized": 0.70,
        "career_score_normalized": 0.10,
        "lifestyle_score_normalized": 0.05,
        "international_environment_score_normalized": 0.05,
        "english_friendliness_score_normalized": 0.05,
        "housing_difficulty_score_normalized": 0.05,
    }

    result = calculate_weighted_score(
        sample_data,
        weights=academic_weights,
    )

    assert result.loc[0, "school_name"] == "Academic School"
