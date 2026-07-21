from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_PATH = PROJECT_ROOT / "data" / "raw" / "score_components.csv"


CATEGORY_DEFINITIONS = {
    "lifestyle": [
        ("city_quality", 0.60),
        ("social_and_cultural_environment", 0.40),
    ],
    "international": [
        ("campus_internationality", 0.60),
        ("international_city_connectivity", 0.40),
    ],
    "english_friendliness": [
        ("daily_life_english_accessibility", 0.60),
        ("professional_english_accessibility", 0.40),
    ],
    "housing": [
        ("housing_availability", 0.60),
        ("housing_affordability", 0.40),
    ],
}


SCHOOL_SCORES = {
    "Copenhagen Business School": {
        "lifestyle": [92, 90],
        "international": [92, 95],
        "english_friendliness": [95, 75],
        "housing": [55, 45],
    },
    "ESADE": {
        "lifestyle": [88, 95],
        "international": [92, 95],
        "english_friendliness": [85, 75],
        "housing": [55, 50],
    },
    "Nova SBE": {
        "lifestyle": [90, 92],
        "international": [92, 88],
        "english_friendliness": [90, 80],
        "housing": [60, 65],
    },
    "HEC Paris": {
        "lifestyle": [82, 90],
        "international": [96, 98],
        "english_friendliness": [85, 75],
        "housing": [45, 35],
    },
    "Rotterdam School of Management": {
        "lifestyle": [88, 85],
        "international": [95, 95],
        "english_friendliness": [95, 90],
        "housing": [45, 40],
    },
    "University of St. Gallen": {
        "lifestyle": [92, 78],
        "international": [90, 85],
        "english_friendliness": [85, 70],
        "housing": [55, 40],
    },
    "Stockholm School of Economics": {
        "lifestyle": [94, 88],
        "international": [92, 92],
        "english_friendliness": [95, 88],
        "housing": [40, 35],
    },
    "WU Vienna": {
        "lifestyle": [94, 95],
        "international": [92, 95],
        "english_friendliness": [90, 70],
        "housing": [60, 55],
    },
    "Prague University of Economics and Business": {
        "lifestyle": [85, 92],
        "international": [85, 90],
        "english_friendliness": [82, 70],
        "housing": [72, 80],
    },
    "National University of Singapore": {
        "lifestyle": [95, 90],
        "international": [98, 100],
        "english_friendliness": [100, 100],
        "housing": [50, 45],
    },
    "HKUST Business School": {
        "lifestyle": [90, 92],
        "international": [96, 100],
        "english_friendliness": [95, 85],
        "housing": [45, 35],
    },
    "Keio University": {
        "lifestyle": [92, 100],
        "international": [82, 98],
        "english_friendliness": [70, 45],
        "housing": [55, 45],
    },
    "Cornell SC Johnson College of Business": {
        "lifestyle": [88, 72],
        "international": [95, 82],
        "english_friendliness": [100, 100],
        "housing": [55, 35],
    },
    "FGV EAESP": {
        "lifestyle": [72, 95],
        "international": [82, 90],
        "english_friendliness": [60, 40],
        "housing": [65, 75],
    },
    "University of Sydney Business School": {
        "lifestyle": [95, 95],
        "international": [98, 100],
        "english_friendliness": [100, 100],
        "housing": [35, 25],
    },
}


def build_component_rows() -> pd.DataFrame:
    """Create component rows for all remaining categories."""

    rows = []

    for school_name, category_values in SCHOOL_SCORES.items():
        for category, indicator_definitions in CATEGORY_DEFINITIONS.items():
            scores = category_values[category]

            if len(scores) != len(indicator_definitions):
                raise ValueError(
                    f"Incorrect number of {category} scores for "
                    f"{school_name}."
                )

            for score, (indicator, weight) in zip(
                scores,
                indicator_definitions,
            ):
                weighted_score = score * weight

                rows.append(
                    {
                        "school_name": school_name,
                        "category": category,
                        "indicator": indicator,
                        "normalized_score": score,
                        "weight": weight,
                        "weighted_score": weighted_score,
                        "source_name": "Project provisional rubric",
                        "source_url": "",
                        "reference_year": 2026,
                        "source_type": "Provisional project assessment",
                        "confidence_level": "Medium",
                        "notes": (
                            "Initial comparative score created using a "
                            "consistent cross-destination rubric. Replace "
                            "with verified source-based indicators during "
                            "the data-validation phase."
                        ),
                    }
                )

    return pd.DataFrame(rows)


def main() -> None:
    if not COMPONENTS_PATH.exists():
        raise FileNotFoundError(
            f"Component file not found: {COMPONENTS_PATH}"
        )

    existing = pd.read_csv(COMPONENTS_PATH)
    new_rows = build_component_rows()

    categories_to_replace = set(CATEGORY_DEFINITIONS)

    existing = existing[
        ~existing["category"].isin(categories_to_replace)
    ].copy()

    combined = pd.concat(
        [existing, new_rows],
        ignore_index=True,
    )

    combined.to_csv(
        COMPONENTS_PATH,
        index=False,
    )

    print("Remaining component categories added successfully.")
    print(f"Rows added: {len(new_rows)}")
    print(f"Total rows: {len(combined)}")

    summary = (
        new_rows.groupby(
            ["school_name", "category"],
            as_index=False,
        )["weighted_score"]
        .sum()
        .rename(
            columns={
                "weighted_score": "category_score",
            }
        )
    )

    print("\nGenerated category scores:")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
