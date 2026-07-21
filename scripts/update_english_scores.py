from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "score_components.csv"
)

REFERENCE_YEAR = 2025
EF_MINIMUM_SCORE = 390
EF_MAXIMUM_SCORE = 624


SCHOOL_ENGLISH_DATA = {
    "Copenhagen Business School": {
        "ef_score": 611,
        "country": "Denmark",
    },
    "ESADE": {
        "ef_score": 540,
        "country": "Spain",
    },
    "Nova SBE": {
        "ef_score": 612,
        "country": "Portugal",
    },
    "HEC Paris": {
        "ef_score": 539,
        "country": "France",
    },
    "Rotterdam School of Management": {
        "ef_score": 624,
        "country": "Netherlands",
    },
    "University of St. Gallen": {
        "ef_score": 564,
        "country": "Switzerland",
    },
    "Stockholm School of Economics": {
        "ef_score": 609,
        "country": "Sweden",
    },
    "WU Vienna": {
        "ef_score": 616,
        "country": "Austria",
    },
    "Prague University of Economics and Business": {
        "ef_score": 582,
        "country": "Czech Republic",
    },
    "National University of Singapore": {
        "fixed_score": 100,
        "country": "Singapore",
        "reason": "English is an official and principal working language.",
    },
    "HKUST Business School": {
        "ef_score": 538,
        "country": "Hong Kong",
    },
    "Keio University": {
        "ef_score": 446,
        "country": "Japan",
    },
    "Cornell SC Johnson College of Business": {
        "fixed_score": 100,
        "country": "United States",
        "reason": "English is the primary language of daily and academic life.",
    },
    "FGV EAESP": {
        "ef_score": 482,
        "country": "Brazil",
    },
    "University of Sydney Business School": {
        "fixed_score": 100,
        "country": "Australia",
        "reason": "English is the primary language of daily and academic life.",
    },
}


def normalize_ef_score(ef_score: int) -> float:
    """Convert an EF EPI score to the project's 0–100 scale."""

    normalized = (
        100
        * (ef_score - EF_MINIMUM_SCORE)
        / (EF_MAXIMUM_SCORE - EF_MINIMUM_SCORE)
    )

    return round(max(0, min(100, normalized)), 2)


def build_english_rows() -> pd.DataFrame:
    """Build one evidence-based English component per school."""

    rows = []

    for school_name, values in SCHOOL_ENGLISH_DATA.items():
        country = values["country"]

        if "fixed_score" in values:
            normalized_score = values["fixed_score"]
            source_type = "Official-language classification"
            notes = values["reason"]
        else:
            ef_score = values["ef_score"]
            normalized_score = normalize_ef_score(ef_score)
            source_type = "International proficiency index"
            notes = (
                f"{country} received an EF EPI 2025 score of "
                f"{ef_score}. The value was normalized against the "
                f"2025 EF EPI range of {EF_MINIMUM_SCORE} to "
                f"{EF_MAXIMUM_SCORE}."
            )

        rows.append(
            {
                "school_name": school_name,
                "category": "english_friendliness",
                "indicator": "national_english_accessibility",
                "normalized_score": normalized_score,
                "weight": 1.0,
                "weighted_score": normalized_score,
                "source_name": "EF English Proficiency Index 2025",
                "source_url": "https://www.ef.com/wwen/epi/",
                "reference_year": REFERENCE_YEAR,
                "source_type": source_type,
                "confidence_level": "Medium",
                "notes": notes,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    if not COMPONENTS_PATH.exists():
        raise FileNotFoundError(
            f"Component file not found: {COMPONENTS_PATH}"
        )

    existing = pd.read_csv(COMPONENTS_PATH)

    existing = existing[
        existing["category"] != "english_friendliness"
    ].copy()

    new_rows = build_english_rows()

    combined = pd.concat(
        [existing, new_rows],
        ignore_index=True,
    )

    combined.to_csv(
        COMPONENTS_PATH,
        index=False,
    )

    print("English-friendliness scores updated successfully.")
    print(f"Rows added: {len(new_rows)}")

    print(
        "\n"
        + new_rows[
            [
                "school_name",
                "normalized_score",
                "confidence_level",
            ]
        ].sort_values(
            "normalized_score",
            ascending=False,
        ).to_string(index=False)
    )


if __name__ == "__main__":
    main()
