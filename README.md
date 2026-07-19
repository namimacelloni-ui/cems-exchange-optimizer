# CEMS Exchange Destination Optimizer

A decision-support tool that helps CEMS students compare exchange destinations according to their academic, career, financial, language and lifestyle preferences.

## Live application

[Open the CEMS Exchange Destination Optimizer](https://cems-exchange-optimizer-qnr3j3ntwhngqd8ke8jgly.streamlit.app/)

## Overview

Choosing an exchange destination requires students to compare fragmented information about universities, living costs, language, housing, professional opportunities and student life.

The CEMS Exchange Destination Optimizer brings these factors together in one interactive application and produces a personalised ranking based on the user's constraints and priorities.

## Key features

- Personalised ranking of 15 CEMS exchange destinations
- Region and teaching-language filters
- Maximum monthly budget filter
- Visa-free destination filter for EU citizens
- Adjustable priority weights
- Transparent compatibility score
- Estimated monthly student costs
- Explanation of the main strengths and drawbacks of the top recommendation
- Automated tests for the scoring and ranking logic


## How it works

The application follows four main steps:

1. It filters destinations according to practical constraints such as region, language, budget and visa requirements.
2. It converts raw 1–5 scores into a standardised 0–100 scale.
3. It applies the user's selected weights to the following categories:
   - Academic opportunities
   - Career opportunities
   - Lifestyle
   - International environment
   - English friendliness
   - Housing convenience
4. It ranks the eligible universities according to their final weighted score.

## Default weighting

The initial model uses the following default weights:

| Category | Weight |
|---|---:|
| Academic opportunities | 25% |
| Career opportunities | 20% |
| Lifestyle | 15% |
| International environment | 15% |
| English friendliness | 15% |
| Housing convenience | 10% |

Users can change these weights, provided that the total remains equal to 100%.

## Dataset

The prototype currently includes 15 CEMS destinations across Europe, Asia, North America, South America and Oceania.

The dataset contains:

- School, city, country and region
- Teaching language
- Estimated monthly student cost
- Estimated housing cost
- Approximate return travel cost from Milan
- Academic score
- Career score
- Lifestyle score
- International environment score
- Housing difficulty score
- English friendliness score
- Visa requirement for EU citizens

## Methodology

Positive indicators such as academic quality and career opportunities are scored from 1 to 5 and converted to a 0–100 scale:

```text
1 → 0
2 → 25
3 → 50
4 → 75
5 → 100
```

Housing difficulty is treated as a negative variable, meaning that a lower raw score produces a higher convenience score.

The final score is calculated as:

```text
Final score =
Academic score × academic weight
+ Career score × career weight
+ Lifestyle score × lifestyle weight
+ International environment score × international weight
+ English friendliness score × English weight
+ Housing convenience score × housing weight
```

More detailed documentation is available in:

- `reports/scoring_methodology.md`
- `reports/cost_methodology.md`
- `data/data_dictionary.md`

## Data limitations

This is a prototype and the data should not be interpreted as an official university ranking.

Important limitations include:

- Several scores are constructed project indicators rather than official university ratings.
- Cost figures are approximate and may change over time.
- Lifestyle and career scores include a degree of subjective judgement.
- Course availability may vary by semester.
- Visa requirements depend on nationality, study duration and current regulations.
- The dataset should be validated further before being used for high-stakes decisions.

The application is intended to support comparison, not replace official university information or personal judgement.

## Project structure

```text
cems-exchange-optimizer/
│
├── app/
│   └── app.py
├── assets/
├── data/
│   ├── raw/
│   │   ├── cems_universities.csv
│   │   └── data_sources.csv
│   ├── processed/
│   └── data_dictionary.md
├── notebooks/
├── reports/
│   ├── cost_methodology.md
│   ├── data_collection_checklist.md
│   └── scoring_methodology.md
├── src/
│   ├── explanations.py
│   ├── load_data.py
│   ├── ranking.py
│   ├── run_ranking.py
│   └── scoring.py
├── tests/
│   ├── test_explanations.py
│   ├── test_ranking.py
│   └── test_scoring.py
├── README.md
└── requirements.txt
```

## Technologies used

- Python
- Pandas
- Streamlit
- Pytest
- Git
- GitHub

## Run the application locally

### 1. Clone the repository

```bash
git clone https://github.com/namimacelloni-ui/cems-exchange-optimizer.git
cd cems-exchange-optimizer
```

### 2. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

On Windows, you may need to use:

```bash
py -m pip install -r requirements.txt
```

### 3. Run the tests

```bash
python -m pytest
```

or:

```bash
py -m pytest
```

### 4. Launch the application

```bash
python -m streamlit run app/app.py
```

or:

```bash
py -m streamlit run app/app.py
```

## Future improvements

Possible next versions could include:

- Fully validated cost and housing data
- All CEMS member schools
- Course-level academic matching
- Destination comparison charts
- Student-review data
- More detailed explanations of recommendations
- Sensitivity analysis
- Downloadable recommendation reports
- Automatic data updates

## Disclaimer

This is an independent student project and is not an official CEMS or Bocconi University platform.
