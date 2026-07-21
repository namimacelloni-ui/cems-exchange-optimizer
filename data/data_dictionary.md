# Data Dictionary

This document describes the datasets used by the CEMS Exchange Destination Optimizer.

## `data/raw/cems_universities.csv`

Contains stable information about each exchange destination and a small number of simplified contextual indicators.

| Column | Description |
|---|---|
| `school_name` | Name of the CEMS partner school |
| `city` | City where the school is located |
| `country` | Country where the school is located |
| `region` | Geographic region used by the application filters |
| `teaching_language` | Main teaching language available to exchange students |
| `flight_cost_from_milan_eur` | Approximate return travel cost from Milan, expressed in euros |
| `lifestyle_score` | Simplified comparative lifestyle score from 1 to 5 |
| `international_environment_score` | Simplified comparative international-environment score from 1 to 5 |
| `english_friendliness_score` | Simplified comparative English-accessibility score from 1 to 5 |
| `visa_required_for_eu` | Whether an EU citizen generally requires a visa for the exchange destination |
| `data_status` | Indicates whether the destination data is complete, partial, or under review |

The lifestyle, international-environment, and English-friendliness scores are project estimates rather than official university ratings.

## `data/raw/cost_estimates.csv`

Contains structured estimates of monthly living and housing costs.

| Column | Description |
|---|---|
| `school_name` | Name used to connect the cost estimate to the university dataset |
| `city` | City where the school is located |
| `housing_low_eur` | Lower monthly housing-cost estimate |
| `housing_typical_eur` | Typical monthly housing-cost estimate |
| `housing_high_eur` | Higher monthly housing-cost estimate |
| `non_housing_monthly_eur` | Typical monthly non-housing expenses |
| `monthly_cost_low_eur` | Lower estimate of total monthly living costs |
| `monthly_cost_typical_eur` | Typical estimate of total monthly living costs |
| `monthly_cost_high_eur` | Higher estimate of total monthly living costs |
| `cost_reference_year` | Year represented by the estimate |
| `source_type` | Type of source used to construct the estimate |
| `confidence_level` | Qualitative assessment of the estimate's reliability |
| `notes` | Assumptions, limitations, or explanatory comments |

The application uses `monthly_cost_typical_eur` for the maximum-budget filter.

The low and high values are shown to communicate uncertainty rather than present one exact cost.

## `data/raw/score_components.csv`

Contains the indicators used to calculate the academic and career category scores.

| Column | Description |
|---|---|
| `school_name` | Name used to connect the component to the university dataset |
| `category` | Scoring category, currently `academic` or `career` |
| `indicator` | Name of the individual component |
| `normalized_score` | Indicator score from 0 to 100 |
| `weight` | Importance of the indicator within its category |
| `weighted_score` | `normalized_score` multiplied by `weight` |
| `source_name` | Name of the information source |
| `source_url` | Link to the supporting source |
| `reference_year` | Year represented by the source or assessment |
| `source_type` | Classification of the supporting source |
| `confidence_level` | Qualitative assessment of evidence quality |
| `notes` | Explanation of the score and its limitations |

For every school and category, the indicator weights should add up to `1.0`.

The category score is calculated as:

```text
category score = sum of weighted indicator scores
```

The result is a score from 0 to 100.

## Calculated fields

Some values used by the application are not stored directly in the original university dataset.

### `estimated_monthly_cost_eur`

Copied from:

```text
monthly_cost_typical_eur
```

It is used by the application's budget filter.

### `academic_score`

Calculated from the weighted academic indicators in `score_components.csv`.

The result is converted into the scale expected by the existing ranking pipeline.

### `career_score`

Calculated from the weighted career indicators in `score_components.csv`.

The result is converted into the scale expected by the existing ranking pipeline.

### `housing_convenience_score`

Calculated from:

- typical housing cost
- difference between the low and high housing estimates

The calculation gives:

- 80% weight to housing affordability
- 20% weight to cost predictability

### `housing_difficulty_score`

Derived from the housing-convenience score because the ranking system currently expects a difficulty measure.

A lower value represents easier housing conditions.

A higher value represents more difficult housing conditions.

## Data limitations

The datasets contain estimates and constructed indicators.

Important limitations include:

- university information changes over time
- course access may change by semester
- living costs depend on personal choices and exchange rates
- published information is not always directly comparable
- some contextual scores are simplified project assessments

The data should therefore support comparison rather than replace official university or government information.
