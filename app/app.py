from pathlib import Path
import sys

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))


from src.explanations import generate_recommendation_explanation
from src.load_data import load_university_data
from src.ranking import calculate_weighted_score
from src.scoring import add_normalized_scores


st.set_page_config(
    page_title="CEMS Exchange Optimizer",
    page_icon="🌍",
    layout="wide",
)


st.title("CEMS Exchange Destination Optimizer")

st.write(
    "Compare CEMS exchange destinations according to your academic, "
    "career, financial, lifestyle and practical preferences."
)


universities = load_university_data()

complete_school_count = (
    universities["data_status"]
    .isin(["partial", "complete"])
    .sum()
)

st.info(
    f"Dataset progress: {complete_school_count} of "
    f"{len(universities)} universities currently contain research data."
)


# -------------------------
# Practical filters
# -------------------------

st.sidebar.header("Practical constraints")

available_regions = sorted(
    universities["region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Preferred regions",
    options=available_regions,
    default=available_regions,
)

available_languages = sorted(
    universities["teaching_language"].dropna().unique().tolist()
)

selected_languages = st.sidebar.multiselect(
    "Teaching language",
    options=available_languages,
    default=available_languages,
)

maximum_budget = st.sidebar.slider(
    "Maximum monthly budget (€)",
    min_value=800,
    max_value=2500,
    value=1800,
    step=50,
)

visa_free_only = st.sidebar.checkbox(
    "Show only destinations without a student visa for EU citizens",
    value=False,
)


filtered_universities = universities[
    universities["region"].isin(selected_regions)
].copy()

filtered_universities = filtered_universities[
    filtered_universities["teaching_language"].isin(selected_languages)
].copy()

filtered_universities = filtered_universities[
    filtered_universities["estimated_monthly_cost_eur"] <= maximum_budget
].copy()

if visa_free_only:
    filtered_universities = filtered_universities[
        filtered_universities["visa_required_for_eu"] == False
    ].copy()


normalized_data = add_normalized_scores(filtered_universities)


# -------------------------
# Priority weights
# -------------------------

st.sidebar.divider()
st.sidebar.header("Your priorities")

academic_weight = st.sidebar.slider(
    "Academic opportunities",
    min_value=0,
    max_value=100,
    value=25,
)

career_weight = st.sidebar.slider(
    "Career opportunities",
    min_value=0,
    max_value=100,
    value=20,
)

lifestyle_weight = st.sidebar.slider(
    "Lifestyle",
    min_value=0,
    max_value=100,
    value=15,
)

international_weight = st.sidebar.slider(
    "International environment",
    min_value=0,
    max_value=100,
    value=15,
)

english_weight = st.sidebar.slider(
    "English friendliness",
    min_value=0,
    max_value=100,
    value=15,
)

housing_weight = st.sidebar.slider(
    "Housing convenience",
    min_value=0,
    max_value=100,
    value=10,
)


total_weight = (
    academic_weight
    + career_weight
    + lifestyle_weight
    + international_weight
    + english_weight
    + housing_weight
)

st.sidebar.write(f"Total weight: {total_weight}%")


if total_weight != 100:
    st.warning(
        "The priority weights must add up to 100% before the ranking "
        "can be calculated."
    )

else:
    weights = {
        "academic_score_normalized": academic_weight / 100,
        "career_score_normalized": career_weight / 100,
        "lifestyle_score_normalized": lifestyle_weight / 100,
        "international_environment_score_normalized": international_weight / 100,
        "english_friendliness_score_normalized": english_weight / 100,
        "housing_difficulty_score_normalized": housing_weight / 100,
    }

    ranked_data = calculate_weighted_score(
        normalized_data,
        weights=weights,
    )

    available_results = ranked_data.dropna(
        subset=["final_score"]
    )

    st.subheader("Current ranking")

    st.caption(
        "Only universities matching the selected constraints and containing "
        "complete scoring data are shown."
    )

    if available_results.empty:
        st.info(
            "No universities match your current filters. Try increasing "
            "your budget or selecting additional regions."
        )

    else:
        st.write(
            f"Showing {len(available_results)} eligible destination(s)."
        )

        display_data = available_results[
            [
                "school_name",
                "city",
                "country",
                "region",
                "estimated_monthly_cost_eur",
                "final_score",
                "academic_score",
                "career_score",
                "lifestyle_score",
                "international_environment_score",
                "english_friendliness_score",
                "housing_difficulty_score",
            ]
        ].copy()

        display_data["final_score"] = (
            display_data["final_score"].round(2)
        )

        display_data = display_data.rename(
            columns={
                "school_name": "School",
                "city": "City",
                "country": "Country",
                "region": "Region",
                "estimated_monthly_cost_eur": "Monthly cost (€)",
                "final_score": "Final score",
                "academic_score": "Academic",
                "career_score": "Career",
                "lifestyle_score": "Lifestyle",
                "international_environment_score": "International",
                "english_friendliness_score": "English",
                "housing_difficulty_score": "Housing difficulty",
            }
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Top recommendation")

        top_school = available_results.iloc[0]
        explanation = generate_recommendation_explanation(top_school)

        st.metric(
            label=top_school["school_name"],
            value=f"{top_school['final_score']:.2f}/100",
        )

        st.write(
            f"{top_school['school_name']} in "
            f"{top_school['city']}, {top_school['country']} currently "
            "has the highest compatibility score based on your filters "
            "and selected priorities."
        )

        st.write(
            f"Estimated monthly student cost: "
            f"€{top_school['estimated_monthly_cost_eur']:.0f}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Main strengths")

            for strength in explanation["strengths"]:
                st.write(f"✓ {strength}")

        with col2:
            st.markdown("#### Potential drawbacks")

            for drawback in explanation["drawbacks"]:
                st.write(f"– {drawback}")


st.divider()

st.caption(
    "This prototype uses constructed scores and approximate cost estimates. "
    "It is intended as a transparent decision-support tool rather "
    "than an objective university ranking."
)
