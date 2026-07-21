# CEMS Exchange Destination Optimizer

A decision-support tool that helps CEMS students compare exchange destinations based on their academic, career, financial, language, housing, and lifestyle preferences.

## Live application

[Open the CEMS Exchange Destination Optimizer](https://cems-exchange-optimizer-qnr3j3ntwhngqd8ke8jgly.streamlit.app/)

## Overview

Choosing an exchange destination requires students to compare information from many different sources, including university websites, cost estimates, exchange requirements, and local living conditions.

The CEMS Exchange Destination Optimizer brings these factors together in one interactive application and produces a personalised ranking based on the user's constraints and priorities.

## Main features

- Ranking of 15 CEMS exchange destinations
- Region and teaching-language filters
- Maximum monthly budget filter
- Visa-free destination filter for EU citizens
- Adjustable importance weights
- Estimated monthly living-cost ranges
- Transparent recommendation explanations
- Automated tests for the scoring and ranking logic

## Criteria

The ranking uses six categories:

- Academic opportunities
- Career opportunities
- Lifestyle
- International environment
- English friendliness
- Housing convenience

Users decide how important each category is, provided that the total weight equals 100%.

## Data structure

The project uses three main datasets.

### `cems_universities.csv`

Contains stable destination information and simplified contextual indicators:

- school and location
- region
- teaching language
- approximate return travel cost from Milan
- lifestyle score
- international-environment score
- English-friendliness score
- visa requirement for EU citizens

### `cost_estimates.csv`

Contains structured living-cost estimates:

- low, typical, and high monthly cost
- housing-cost estimates
- non-housing expenses
- reference year
- confidence level
- source information

The typical monthly estimate is used by the budget filter.

### `score_components.csv`

Contains the component-level academic and career indicators.

Academic indicators include:

- course breadth
- subject-area coverage
- graduate-course access
- course accessibility
- academic flexibility

Career indicators include:

- local business ecosystem
- international employer presence
- relevant industry strength
- career services
- English accessibility in the local labour market

Each component is scored from 0 to 100 and multiplied by its assigned weight.

## Housing calculation

Housing convenience is calculated from the structured housing-cost data.

It combines:

- housing affordability: 80%
- predictability of the cost estimate: 20%

Lower typical housing costs receive higher affordability scores.

A smaller difference between the low and high housing estimates receives a higher predictability score.

## Ranking method

The application:

1. Filters destinations according to region, language, budget, and visa preferences.
2. Prepares the six category scores.
3. Applies the weights selected by the user.
4. Calculates a final weighted compatibility score.
5. Ranks the eligible destinations.

The ranking is relative to the destinations currently included in the dataset.

More detail is available in:

- `reports/methodology.md`
- `data/data_dictionary.md`

## Limitations

This project is a decision-support tool, not an official university ranking.

Important limitations include:

- several indicators are constructed project scores
- university information is not always published in a comparable format
- course availability may change by semester
- costs vary according to accommodation, exchange rates, and personal spending
- lifestyle and international-environment scores remain simplified estimates
- visa and work rules may change

Users should verify important information through official university and government sources before making a final decision.

## Project structure

```text
cems-exchange-optimizer/
│
├── app/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   ├── cems_universities.csv
│   │   ├── cost_estimates.csv
│   │   └── score_components.csv
│   └── data_dictionary.md
│
├── reports/
│   └── methodology.md
│
├── src/
│   ├── component_scores.py
│   ├── explanations.py
│   ├── load_data.py
│   ├── ranking.py
│   └── scoring.py
│
├── tests/
│   ├── test_component_scores.py
│   ├── test_explanations.py
│   ├── test_ranking.py
│   └── test_scoring.py
│
├── README.md
└── requirements.txt
```

## Technologies

- Python
- Pandas
- Streamlit
- Pytest
- GitHub

## Run locally

Clone the repository:

```bash
git clone https://github.com/namimacelloni-ui/cems-exchange-optimizer.git
cd cems-exchange-optimizer
```

Install the dependencies:

```bash
py -m pip install -r requirements.txt
```

Run the tests:

```bash
py -m pytest
```

Launch the application:

```bash
py -m streamlit run app/app.py
```

## Possible future improvements

- validate the remaining contextual indicators
- expand the dataset to additional CEMS schools
- add course-level matching
- add destination-comparison charts
- introduce sensitivity analysis
- automate periodic data updates

## Disclaimer

This is an independent student project and is not an official CEMS or Bocconi University platform.
