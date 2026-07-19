from load_data import load_university_data
from ranking import calculate_weighted_score
from scoring import add_normalized_scores


def main() -> None:
    """Load, normalize and rank the available university data."""

    universities = load_university_data()
    normalized_data = add_normalized_scores(universities)
    ranked_data = calculate_weighted_score(normalized_data)

    columns_to_display = [
        "school_name",
        "city",
        "country",
        "final_score",
    ]

    available_results = ranked_data.dropna(
        subset=["final_score"]
    )

    print("\nCEMS Exchange Destination Ranking\n")

    if available_results.empty:
        print("No universities currently have enough data to be ranked.")
        return

    print(
        available_results[columns_to_display]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
