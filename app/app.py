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
            --primary: #111111;
            --accent: #9E1B32;
            --background: #F7F6F3;
            --card: #FFFFFF;
            --text: #202124;
            --muted: #6B6F76;
            --border: #E2E0DC;
            --soft-accent: #F6EDEF;
            --soft-neutral: #F1F0ED;
        }

        .stApp {
            background-color: var(--background);
            color: var(--text);
        }

        .block-container {
            max-width: 1240px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Sidebar */

        [data-testid="stSidebar"] {
            background-color: var(--primary);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.16);
        }

        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .stCheckbox label {
            font-weight: 600;
        }

        [data-testid="stSidebar"] [data-baseweb="tag"] {
            background-color: var(--accent);
            border-radius: 5px;
        }

        /* Typography */

        h1, h2, h3, h4 {
            color: var(--primary);
            letter-spacing: -0.025em;
        }

        /* Hero */

        .hero {
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(
                    125deg,
                    #111111 0%,
                    #1C1C1C 58%,
                    #4B111C 100%
                );
            border-radius: 4px;
            padding: 3rem 3.1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 16px 38px rgba(17, 17, 17, 0.16);
        }

        .hero::after {
            content: "";
            position: absolute;
            top: -90px;
            right: -70px;
            width: 280px;
            height: 280px;
            border: 52px solid rgba(158, 27, 50, 0.55);
            border-radius: 50%;
        }

        .hero-label {
            position: relative;
            z-index: 1;
            color: #E6A7B2;
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }

        .hero-title {
            position: relative;
            z-index: 1;
            max-width: 820px;
            color: #FFFFFF;
            font-size: 2.75rem;
            line-height: 1.08;
            font-weight: 760;
            margin: 0;
        }

        .hero-subtitle {
            position: relative;
            z-index: 1;
            max-width: 720px;
            color: rgba(255, 255, 255, 0.76);
            font-size: 1.04rem;
            line-height: 1.65;
            margin-top: 1rem;
            margin-bottom: 0;
        }

        .accent-line {
            position: relative;
            z-index: 1;
            width: 72px;
            height: 4px;
            margin-top: 1.5rem;
            background-color: var(--accent);
        }

        /* Section headings */

        .section-label {
            color: var(--accent);
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        /* Dataset message */

        .progress-box {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-left: 5px solid var(--accent);
            border-radius: 4px;
            padding: 0.95rem 1.1rem;
            margin-bottom: 1.5rem;
            color: var(--text);
            box-shadow: 0 4px 14px rgba(17, 17, 17, 0.04);
        }

        /* Metric cards */

        [data-testid="stMetric"] {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1.05rem 1.15rem;
            box-shadow: 0 4px 14px rgba(17, 17, 17, 0.04);
        }

        [data-testid="stMetricValue"] {
            color: var(--primary);
            font-weight: 750;
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted);
        }

        /* Ranking table */

        div[data-testid="stDataFrame"] {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 0 6px 20px rgba(17, 17, 17, 0.05);
        }

        /* Recommendation */

        .recommendation-card {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-top: 6px solid var(--accent);
            border-radius: 4px;
            padding: 1.7rem 1.8rem;
            margin-top: 0.8rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 8px 26px rgba(17, 17, 17, 0.07);
        }

        .recommendation-label {
            color: var(--accent);
            font-size: 0.75rem;
            font-weight: 750;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }

        .recommendation-school {
            color: var(--primary);
            font-size: 1.85rem;
            line-height: 1.25;
            font-weight: 760;
            margin-top: 0.3rem;
        }

        .recommendation-location {
            color: var(--muted);
            font-size: 0.96rem;
            margin-top: 0.35rem;
        }

        .recommendation-score {
            color: var(--accent);
            font-size: 2.35rem;
            line-height: 1;
            font-weight: 800;
            text-align: right;
        }

        .recommendation-score-label {
            color: var(--muted);
            font-size: 0.8rem;
            text-align: right;
            margin-top: 0.3rem;
        }

        /* Strengths and drawbacks */

        .strength {
            background-color: var(--soft-neutral);
            border-left: 4px solid #333333;
            border-radius: 3px;
            padding: 0.78rem 0.9rem;
            margin-bottom: 0.6rem;
            color: #303234;
        }

        .drawback {
            background-color: var(--soft-accent);
            border-left: 4px solid var(--accent);
            border-radius: 3px;
            padding: 0.78rem 0.9rem;
            margin-bottom: 0.6rem;
            color: #671322;
        }

        /* Notices */

        div[data-testid="stAlert"] {
            border-radius: 4px;
        }

        .disclaimer {
            background-color: var(--card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 1rem 1.1rem;
            color: var(--muted);
            font-size: 0.84rem;
            line-height: 1.55;
            margin-top: 2.2rem;
        }

        /* Buttons */

        .stButton > button {
            background-color: var(--accent);
            color: #FFFFFF;
            border: 1px solid var(--accent);
            border-radius: 3px;
            font-weight: 650;
        }

        .stButton > button:hover {
            background-color: #7F1528;
            border-color: #7F1528;
            color: #FFFFFF;
        }

        /* Inputs */

        div[data-baseweb="select"] > div {
            border-radius: 3px;
        }

        /* Mobile */

        @media (max-width: 800px) {
            .hero {
                padding: 2rem 1.5rem;
            }

            .hero-title {
                font-size: 2.05rem;
            }

            .hero::after {
                opacity: 0.4;
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
