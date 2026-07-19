# Cost Data Methodology

## Purpose

This document explains how cost information is collected and standardised for
the CEMS Exchange Destination Optimizer.

All monetary values are expressed in euros.

---

## Estimated monthly cost

`estimated_monthly_cost_eur` represents the expected monthly expenditure of an
exchange student.

It should include:

- Housing
- Food and groceries
- Local transportation
- Basic leisure and personal expenses

It should not include:

- Tuition fees
- Flights to and from the destination
- Visa or residence-permit fees
- Exceptional travel
- Luxury spending

Whenever possible, the estimate should come from an official university
student-budget page.

If the university provides a range, the midpoint will be used.

### Example

If the estimated monthly expenditure is between €1,000 and €1,400:

`estimated_monthly_cost_eur = 1200`

---

## Housing cost

`housing_cost_eur` represents the estimated monthly cost of typical student
accommodation.

The preferred sources are:

1. Official university residence prices
2. University estimates for private student housing
3. Reputable student-accommodation sources

If a range is provided, the midpoint will be used.

The value should reflect a private bedroom in shared accommodation or a
standard student residence, rather than a private apartment.

---

## Flight cost from Milan

`flight_cost_from_milan_eur` represents an approximate economy return fare from
Milan to the destination.

The estimate should:

- Use a return journey
- Include mandatory booking charges
- Exclude optional baggage and seat-selection charges
- Represent a typical fare rather than the lowest promotional price

For destinations that require ground transportation after the flight, the
estimated transfer cost should be included.

Because flight prices change frequently, this variable will have lower
confidence than official university cost estimates.

---

## Currency conversion

When a source uses another currency, the value will be converted to euros using
a single recorded exchange rate.

The following information must be recorded in the source tracker:

- Original amount
- Original currency
- Exchange rate used
- Conversion date
- Converted value in euros

---

## Source priority

Cost sources should be prioritised in this order:

1. Official university source
2. Government or public institution
3. Academic or student organisation
4. Reputable commercial cost-of-living source
5. Project estimate

---

## Missing data

If reliable information cannot be found, the value will remain blank.

Missing values will not be replaced with invented estimates.

---

## Update frequency

Cost information should display the year in which it was collected.

Because living and travel costs change over time, the dataset should be reviewed
at least once per year.
