# Data Dictionary

This document defines the variables used in the CEMS Exchange Destination Optimizer.

## Identification variables

### school_name

- **Description:** Official or commonly used name of the CEMS member school
- **Type:** Text
- **Example:** Copenhagen Business School
- **Source:** CEMS or the university’s official website

### city

- **Description:** Main city in which the school is located
- **Type:** Text
- **Example:** Copenhagen

### country

- **Description:** Country in which the school is located
- **Type:** Text
- **Example:** Denmark

### region

- **Description:** Broad geographical region used for filtering destinations
- **Type:** Category
- **Possible values:** Southern Europe, Western Europe, Northern Europe, Central Europe, Asia, North America, South America, Oceania

---

## Language variables

### teaching_language

- **Description:** Main language in which exchange or CEMS courses are taught
- **Type:** Text
- **Example:** English
- **Possible values:** English, English and local language, Local language
- **Source:** Official university course catalogue or exchange information

### english_friendliness_score

- **Description:** Estimated ease with which an international student can study and manage daily life using English
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Higher is better

#### Scoring criteria

- **1:** English is rarely sufficient for study or daily life
- **2:** Some English support, but the local language is frequently necessary
- **3:** Courses are available in English, but daily life may require the local language
- **4:** English is widely usable in both university and daily life
- **5:** English is sufficient for almost all academic and daily activities

---

## Cost variables

### estimated_monthly_cost_eur

- **Description:** Estimated total monthly student expenditure, including housing, food, local transport and basic leisure
- **Type:** Number
- **Unit:** EUR per month
- **Direction:** Lower is better
- **Source:** University estimates and reputable cost-of-living sources
- **Limitation:** Actual spending depends on accommodation and lifestyle

### housing_cost_eur

- **Description:** Estimated average monthly housing cost for an exchange student
- **Type:** Number
- **Unit:** EUR per month
- **Direction:** Lower is better
- **Source:** Official university housing information or student-budget estimates

### flight_cost_from_milan_eur

- **Description:** Approximate return travel cost from Milan to the destination
- **Type:** Number
- **Unit:** EUR
- **Direction:** Lower is better
- **Method:** Representative economy return fare
- **Limitation:** Prices vary significantly by season and booking date

---

## Evaluation scores

### academic_score

- **Description:** Overall assessment of academic opportunities for an international management student
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Higher is better

#### Scoring criteria

- **1:** Very limited relevant course availability
- **2:** Limited selection of relevant courses
- **3:** Adequate range of relevant management courses
- **4:** Strong course selection across several management areas
- **5:** Extensive and highly relevant course offering

### career_score

- **Description:** Assessment of the destination’s career and professional-development opportunities
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Higher is better

#### Factors considered

- Local job market
- Presence of multinational companies
- Strength of relevant industries
- Networking opportunities
- Employer access

#### Scoring criteria

- **1:** Very limited career ecosystem
- **2:** Some opportunities, but limited international accessibility
- **3:** Moderate professional opportunities
- **4:** Strong market with good international opportunities
- **5:** Major international business hub with extensive opportunities

### lifestyle_score

- **Description:** Overall assessment of student lifestyle, culture, leisure and social environment
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Higher is better

#### Scoring criteria

- **1:** Limited student and leisure environment
- **2:** Some activities, but relatively limited
- **3:** Balanced lifestyle and social opportunities
- **4:** Strong cultural and social environment
- **5:** Exceptional student lifestyle and variety of activities

### international_environment_score

- **Description:** Assessment of the school and city’s international student environment
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Higher is better

#### Scoring criteria

- **1:** Predominantly local environment
- **2:** Limited international presence
- **3:** Moderately international
- **4:** Highly international university or city
- **5:** Exceptionally international academic and social environment

### housing_difficulty_score

- **Description:** Assessment of how difficult it is for an exchange student to secure suitable accommodation
- **Type:** Integer
- **Scale:** 1–5
- **Direction:** Lower is better

#### Scoring criteria

- **1:** Housing is readily available and supported by the university
- **2:** Generally manageable with some advance planning
- **3:** Moderate competition or limited university accommodation
- **4:** Difficult and expensive housing market
- **5:** Severe housing shortage or extremely difficult search process

---

## Administrative variable

### visa_required_for_eu

- **Description:** Whether an EU citizen normally requires a student visa or equivalent study authorisation
- **Type:** Boolean
- **Possible values:** TRUE, FALSE
- **Direction:** FALSE is more convenient
- **Limitation:** Immigration requirements may depend on nationality, study duration and current regulations
