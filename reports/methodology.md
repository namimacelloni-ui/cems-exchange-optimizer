# Methodology

## Overview

The CEMS Exchange Destination Optimizer compares exchange destinations using six criteria:

- academic opportunities
- career opportunities
- lifestyle
- international environment
- English friendliness
- housing convenience

Users choose the importance of each criterion. The application then calculates a weighted score and ranks the available destinations.

## Cost estimates

Monthly costs are stored in `data/raw/cost_estimates.csv`.

Each destination includes:

- low monthly estimate
- typical monthly estimate
- high monthly estimate
- housing estimate
- non-housing estimate
- reference year
- confidence level
- source information

The application uses the typical monthly estimate for the budget filter.

These values are estimates rather than guaranteed expenses. Actual costs depend on accommodation type, lifestyle, exchange rates, and personal spending habits.

## Academic scores

Academic scores are stored in `data/raw/score_components.csv`.

The academic category combines:

- course breadth
- subject-area coverage
- graduate-course access
- course accessibility
- academic flexibility

Each indicator is scored from 0 to 100 and multiplied by its assigned weight.

The weighted indicators are added together to create the final academic score.

## Career scores

Career scores are also stored in `data/raw/score_components.csv`.

The career category combines:

- local business ecosystem
- international employer presence
- relevant industry strength
- career services
- English accessibility in the local labour market

Each indicator is scored from 0 to 100 and multiplied by its assigned weight.

The weighted indicators are added together to create the final career score.

## Housing convenience

Housing convenience is calculated from the structured housing estimates in `cost_estimates.csv`.

It combines:

- housing affordability: 80%
- predictability of the housing estimate: 20%

Lower typical housing costs receive higher affordability scores.

A smaller difference between the low and high housing estimates receives a higher predictability score.

The result is converted into the housing-difficulty format expected by the ranking system.

## Other destination indicators

Lifestyle, international environment, and English friendliness are currently stored as simplified comparative indicators in `cems_universities.csv`.

These values are intended to support comparison rather than represent official university ratings.

They should be interpreted as provisional project estimates.

## Ranking

The application converts the category values into a common scoring format and applies the weights selected by the user.

The final score is the weighted sum of the six categories.

The ranking is relative to the destinations currently included in the dataset.

## Limitations

The project has several limitations:

- universities publish information in different formats
- some course and exchange rules change each semester
- living costs vary according to personal choices
- city-level indicators may not perfectly represent each student's experience
- some destination indicators remain simplified estimates

The optimizer should therefore be used as a decision-support tool rather than as a definitive ranking.
