import math

import pandas as pd
import pytest

from src.scoring import (
    add_normalized_scores,
    convert_negative_score_to_100,
    convert_positive_score_to_100,
)


def test_positive_score_conversion():
    assert convert_positive_score_to_100(1) == 0
    assert convert_positive_score_to_100(3) == 50
    assert convert_positive_score_to_100(5) == 100


def test_negative_score_conversion():
    assert convert_negative_score_to_100(1) == 100
    assert convert_negative_score_to_100(3) == 50
    assert convert_negative_score_to_100(5) == 0


def test_missing_score_remains_missing():
    assert math.isnan(convert_positive_score_to_100(float("nan")))
    assert math.isnan(convert_negative_score_to_100(float("nan")))


def test_invalid_positive_score_raises_error():
    with pytest.raises(ValueError):
        convert_positive_score_to_100(6)


def test_add_normalized_scores():
    sample_data = pd.DataFrame(
        {
            "academic_score": [5],
            "career_score": [4],
            "lifestyle_score": [3],
            "international_environment_score": [2],
            "english_friendliness_score": [1],
            "housing_difficulty_score": [4],
        }
    )

    result = add_normalized_scores(sample_data)

    assert result.loc[0, "academic_score_normalized"] == 100
    assert result.loc[0, "career_score_normalized"] == 75
    assert result.loc[0, "lifestyle_score_normalized"] == 50
    assert result.loc[0, "international_environment_score_normalized"] == 25
    assert result.loc[0, "english_friendliness_score_normalized"] == 0
    assert result.loc[0, "housing_difficulty_score_normalized"] == 25
