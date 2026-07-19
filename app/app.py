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
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        :root {
            --primary: #183C34;
            --accent: #C59A4A;
            --background: #F5F1E8;
            --card: #FFFDF8;
            --text: #1F2A26;
            --muted: #6F756F;
            --border: #DED8CC;
            --soft-green: #E8F0EC;
            --soft-warm: #F5EAE2;
        }

        .stApp {
            background-color: var(--background);
            color: var(--text);
        }

        .block-container {
            max-width: 1280px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background-color: var(--primary);
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.18);
        }

        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stCheckbox label {
            font-weight: 600;
        }

        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background-color: var(--accent);
        }

        h1, h2, h3, h4 {
            color: var(--primary);
            letter-spacing: -0.02em;
        }

        .hero {
            background:
                linear-gradient(
                    120deg,
                    rgba(24, 60, 52, 0.98),
                    rgba(44, 82, 70, 0.92)
                );
            border-radius: 18px;
            padding: 2.4rem 2.6rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 30px rgba(24, 60, 52, 0.15);
        }

        .hero-label {
            color: #F0D9A7;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .hero-title {
            color: #FFFFFF;
            font-size: 2.65rem;
            line-height: 1.08;
            font-weight: 750;
            margin: 0;
        }

        .hero-subtitle {
            color: rgba(255, 255, 255, 0.82);
            font-size: 1.05rem;
            line-height: 1.6;
            max-width: 760px;
            margin-top: 1rem;
            margin-bottom: 0;
        }

        .accent-line {
            width: 64px;
            height: 5px;
            background-color: var(--accent);
            border-radius: 20px;
            margin-top: 1.4rem;
        }

        .section-label {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 750;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        .progress-box {
            background-color: #EEE8DC;
            border-left: 4px solid var(--primary);
            border-radius: 9px;
            padding: 0.85rem 1rem;
            margin-bottom: 1.3rem;
            color: var(--primary);
        }

        .recommendation-card {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-left: 6px solid var(--accent);
            border-radius: 14px;
            padding: 1.55rem 1.65rem;
            box-shadow: 0 7px 22px rgba(31, 42, 38, 0.07);
            margin-top: 0.8rem;
            margin-bottom: 1rem;
        }

        .recommendation-label {
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 750;
            letter-spacing: 0.11em;
            text-transform: uppercase;
        }

        .recommendation-school {
            color: var(--primary);
            font-size: 1.75rem;
            font-weight: 750;
            margin-top: 0.25rem;
        }

        .recommendation-location {
            color: var(--muted);
            font-size: 0.98rem;
            margin-top: 0.15rem;
        }

        .recommendation-score {
            color: var(--primary);
            font-size: 2.2rem;
            font-weight: 800;
            text-align: right;
        }

        .recommendation-score-label {
            color: var(--muted);
            font-size: 0.82rem;
            text-align: right;
        }

        .strength {
            background-color: var(--soft-green);
            border-radius: 9px;
            padding: 0.7rem 0.8rem;
            margin-bottom: 0.55rem;
            color: #315E50;
        }

        .drawback {
            background-color: var(--soft-warm);
            border-radius: 9px;
            padding: 0.7rem 0.8rem;
            margin-bottom: 0.55rem;
            color: #7A5140;
        }

        .disclaimer {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.9rem 1rem;
            color: var(--muted);
            font-size: 0.84rem;
            margin-top: 2rem;
        }

        div[data-testid="stDataFrame"] {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }

        div[data-testid="stAlert"] {
            border-radius: 10px;
        }

        .stButton > button {
            background-color: var(--accent);
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            font-weight: 650;
        }

        .stButton > button:hover {
            background-color: #A67C34;
            color: #FFFFFF;
        }

        @media (max-width: 800px) {
            .hero {
                padding: 1.7rem 1.4rem;
            }

            .hero-title {
                font-size: 2rem;
            }

            .recommendation-score,
            .recommendation-score-label {
                text-align: left;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Hero section
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-label">Global exchange decision tool</div>
        <div class="hero-title">Find the CEMS destination that fits you.</div>
        <p class="hero-subtitle">
            Compare international exchange opportunities using your academic,
            career, financial and lifestyle priorities.
        </p>
        <div class="accent-line"></div>
    </div>
    """,
    unsafe_allow_html=True,
)


universities = load_university_data()

complete_school_count = (
    universities["data_status"]
    .isin(["partial", "complete"])
    .sum()
)

st.markdown(
    f"""
    <div class="progress-box">
        <strong>Prototype dataset:</strong>
        {complete_school_count} of {len(universities)} destinations currently
        contain research data.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.markdown("## Exchange preferences")
st.sidebar.caption(
    "Set your practical constraints and decide what matters most to you."
)

st.sidebar.markdown("### Practical constraints")

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
    "Only destinations without a student visa for EU citizens",
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


st.sidebar.divider()
st.sidebar.markdown("### Your priorities")
st.sidebar.caption("The six weights must add up to 100%.")

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

if total_weight == 100:
    st.sidebar.success("Priority total: 100%")
else:
    st.sidebar.error(f"Priority total: {total_weight}%")


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if total_weight != 100:
    st.warning(
        "Adjust the priority sliders so that the total equals 100%."
    )

else:
    weights = {
        "academic_score_normalized": academic_weight / 100,
        "career_score_normalized": career_weight / 100,
        "lifestyle_score_normalized": lifestyle_weight / 100,
        "international_environment_score_normalized":
            international_weight / 100,
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

    st.markdown(
        '<div class="section-label">Personalised results</div>',
        unsafe_allow_html=True,
    )

    st.subheader("Your destination ranking")

    if available_results.empty:
        st.info(
            "No destinations match your current filters. Increase your "
            "budget or select additional regions."
        )

    else:
        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            st.metric(
                "Eligible destinations",
                len(available_results),
            )

        with metric_col2:
            st.metric(
                "Maximum monthly budget",
                f"€{maximum_budget:,}",
            )

        with metric_col3:
            best_score = available_results.iloc[0]["final_score"]
            st.metric(
                "Highest match score",
                f"{best_score:.1f}/100",
            )

        st.write("")

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
                "final_score": "Match score",
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
            column_config={
                "Monthly cost (€)": st.column_config.NumberColumn(
                    format="€%d"
                ),
                "Match score": st.column_config.ProgressColumn(
                    min_value=0,
                    max_value=100,
                    format="%.1f",
                ),
            },
        )

        st.write("")

        st.markdown(
            '<div class="section-label">Best match</div>',
            unsafe_allow_html=True,
        )

        top_school = available_results.iloc[0]
        explanation = generate_recommendation_explanation(top_school)

        st.markdown(
            f"""
            <div class="recommendation-card">
                <div style="
                    display:flex;
                    justify-content:space-between;
                    gap:2rem;
                    align-items:center;
                    flex-wrap:wrap;
                ">
                    <div>
                        <div class="recommendation-label">
                            Top recommendation
                        </div>
                        <div class="recommendation-school">
                            {top_school["school_name"]}
                        </div>
                        <div class="recommendation-location">
                            {top_school["city"]}, {top_school["country"]}
                            &nbsp;·&nbsp;
                            Estimated monthly cost:
                            €{top_school["estimated_monthly_cost_eur"]:.0f}
                        </div>
                    </div>
                    <div>
                        <div class="recommendation-score">
                            {top_school["final_score"]:.1f}
                        </div>
                        <div class="recommendation-score-label">
                            compatibility score
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        strength_column, drawback_column = st.columns(2)

        with strength_column:
            st.markdown("#### Why it matches")

            for strength in explanation["strengths"]:
                st.markdown(
                    f'<div class="strength">✓ {strength}</div>',
                    unsafe_allow_html=True,
                )

        with drawback_column:
            st.markdown("#### Points to consider")

            for drawback in explanation["drawbacks"]:
                st.markdown(
                    f'<div class="drawback">– {drawback}</div>',
                    unsafe_allow_html=True,
                )


st.markdown(
    """
    <div class="disclaimer">
        <strong>Independent student project.</strong>
        This prototype is not an official CEMS platform. Scores are constructed
        indicators and cost figures are approximate. The tool is intended to
        support comparison, not replace official university information or
        personal judgement.
    </div>
    """,
    unsafe_allow_html=True,
)
