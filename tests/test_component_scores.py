import pandas as pd
import pytest

from src.component_scores import (
    calculate_category_scores,
    get_school_category_score,
)


def test_calculate_category_score():
    components = pd.DataFrame(
        {
            "school_name": [
                "Example School",
                "Example School",
            ],
            "category": [
                "academic",
                "academic",
            ],
            "indicator": [
                "course_breadth",
                "course_accessibility",
            ],
            "normalized_score": [
                80,
                60,
            ],
            "weight": [
                0.60,
                0.40,
            ],
            "weighted_score": [
                48,
                24,
            ],
        }
    )

    result = calculate_category_scores(components)

    assert result.loc[0, "category_score"] == 72


def test_weights_must_total_one():
    components = pd.DataFrame(
        {
            "school_name": [
                "Example School",
                "Example School",
            ],
            "category": [
                "academic",
                "academic",
            ],
            "indicator": [
                "course_breadth",
                "course_accessibility",
            ],
            "normalized_score": [
                80,
                60,
            ],
            "weight": [
                0.50,
                0.30,
            ],
            "weighted_score": [
                40,
                18,
            ],
        }
    )

    with pytest.raises(ValueError):
        calculate_category_scores(components)


def test_get_school_category_score():
    scores = pd.DataFrame(
        {
            "school_name": [
                "Example School",
            ],
            "category": [
                "academic",
            ],
            "category_score": [
                88.25,
            ],
        }
    )

    result = get_school_category_score(
        category_scores=scores,
        school_name="Example School",
        category="academic",
    )

    assert result == 88.25


def test_missing_school_score_raises_error():
    scores = pd.DataFrame(
        {
            "school_name": [
                "Example School",
            ],
            "category": [
                "academic",
            ],
            "category_score": [
                88.25,
            ],
        }
    )

    with pytest.raises(ValueError):
        get_school_category_score(
            category_scores=scores,
            school_name="Missing School",
            category="academic",
        )
