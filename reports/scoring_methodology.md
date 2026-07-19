# Scoring Methodology

## Purpose

The CEMS Exchange Destination Optimizer ranks exchange destinations according
to a combination of factual data, constructed indicators and user-selected
preferences.

The model is designed as a decision-support tool. It does not provide an
objective or universally correct ranking of CEMS schools.

---

## Variable categories

### Factual variables

These variables are collected directly from official or reputable sources:

- Teaching language
- Estimated monthly living cost
- Estimated housing cost
- Approximate travel cost from Milan
- Visa requirement for EU citizens

### Constructed scores

These variables are evaluated using a consistent scoring framework:

- Academic score
- Career score
- Lifestyle score
- International environment score
- Housing difficulty score
- English friendliness score

Constructed scores use a scale from 1 to 5 and must be supported by documented
evidence.

---

## Score direction

For the following variables, a higher value is better:

- Academic score
- Career score
- Lifestyle score
- International environment score
- English friendliness score

For the following variables, a lower value is better:

- Estimated monthly living cost
- Housing cost
- Travel cost
- Housing difficulty score

---

## Academic score

The academic score evaluates the relevance and breadth of courses available to
an international management student.

### Factors considered

- Availability of management courses taught in English
- Breadth of subject areas
- Availability of CEMS-specific courses
- Flexibility for exchange students
- Access to graduate-level courses

### Scale

- **1:** Very limited relevant course availability
- **2:** Limited selection of relevant courses
- **3:** Adequate management course offering
- **4:** Strong and diverse course offering
- **5:** Extensive and highly relevant course offering

---

## Career score

The career score evaluates the professional opportunities associated with the
school and destination.

### Factors considered

- Strength of the local employment market
- Presence of multinational companies
- Relevance of major local industries
- Access to networking and employer events
- International accessibility of professional opportunities

### Scale

- **1:** Very limited professional ecosystem
- **2:** Limited international career opportunities
- **3:** Moderate career opportunities
- **4:** Strong career ecosystem
- **5:** Major international business hub

---

## Lifestyle score

The lifestyle score evaluates the overall student experience outside the
classroom.

### Factors considered

- Cultural activities
- Social and nightlife opportunities
- Student population
- Leisure activities
- Accessibility of the city and surrounding area

### Scale

- **1:** Very limited lifestyle offering
- **2:** Limited range of activities
- **3:** Balanced student lifestyle
- **4:** Strong cultural and social environment
- **5:** Exceptional variety of student experiences

---

## International environment score

The international environment score evaluates how internationally oriented the
school and destination are.

### Factors considered

- Number or proportion of international students
- Exchange-student community
- International student organisations
- Buddy and integration programmes
- International character of the city

### Scale

- **1:** Predominantly local environment
- **2:** Limited international presence
- **3:** Moderately international
- **4:** Highly international
- **5:** Exceptionally international

---

## Housing difficulty score

The housing difficulty score evaluates how challenging it is for an exchange
student to find suitable accommodation.

### Factors considered

- Availability of university housing
- Whether housing is guaranteed
- Competition in the private rental market
- Typical search duration
- Evidence of local housing shortages

### Scale

- **1:** Housing is readily available
- **2:** Generally manageable with advance planning
- **3:** Moderate competition or uncertainty
- **4:** Difficult housing market
- **5:** Severe shortage or exceptionally difficult search

---

## English friendliness score

The English friendliness score evaluates whether a student can study and manage
daily life using English.

### Factors considered

- Availability of courses in English
- University administration in English
- English use in daily life
- Availability of services for international students

### Scale

- **1:** English is rarely sufficient
- **2:** Local language is frequently necessary
- **3:** English is sufficient academically but less so in daily life
- **4:** English is widely usable
- **5:** English is sufficient for almost all academic and daily activities

---

## Evidence requirements

Every completed variable must have a corresponding entry in:

`data/raw/data_sources.csv`

Each entry should contain:

- School name
- Variable
- Source
- Source URL
- Date accessed
- Value assigned
- Explanation or limitation

Subjective scores should never be presented as official university ratings.

---

## Missing data

Missing values will initially remain blank.

The project will not replace missing values with invented estimates. Where
necessary, the application will display a warning or exclude the relevant
variable from the calculation.

---

## Initial category weights

The first version will use the following default weights:

- Academic fit: 25%
- Career opportunities: 20%
- Cost: 20%
- Lifestyle: 15%
- International and language environment: 10%
- Practical convenience: 10%

Users will later be able to adjust these weights.
