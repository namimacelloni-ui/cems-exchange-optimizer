import pandas as pd

from src.load_data import load_university_data


def test_load_university_data_returns_all_schools():
    data = load_university_data()

    assert isinstance(data, pd.DataFrame)
    assert len(data) == 15


def test_load_university_data_contains_required_columns():
    data = load_university_data()

    required_columns = {
        "school_name",
        "estimated_monthly_cost_eur",
        "academic_score",
        "career_score",
        "housing_convenience_score",
        "housing_difficulty_score",
        "lifestyle_score",
        "international_environment_score",
        "english_friendliness_score",
    }

    assert required_columns.issubset(data.columns)


def test_no_required_scores_are_missing():
    data = load_university_data()

    required_score_columns = [
        "academic_score",
        "career_score",
        "housing_convenience_score",
        "housing_difficulty_score",
        "lifestyle_score",
        "international_environment_score",
        "english_friendliness_score",
    ]

    assert not data[required_score_columns].isna().any().any()


def test_monthly_cost_matches_typical_cost_estimate():
    data = load_university_data()

    assert (
        data["estimated_monthly_cost_eur"]
        == data["monthly_cost_typical_eur"]
    ).all()


def test_housing_difficulty_is_between_one_and_five():
    data = load_university_data()

    assert data["housing_difficulty_score"].between(1, 5).all()
