# Navigating the Food Desert: Visualizing Barriers to Healthy Food Access in the U.S.

## Overview

Limited access to affordable, nutritious food is associated with poorer diet quality and higher risk of chronic conditions such as diabetes, hypertension, and cardiovascular disease, particularly in communities with fewer socioeconomic resources and limited transportation. Public health research often measures these barriers using indicators such as poverty rates, distance to grocery stores, and vehicle availability, but these metrics are typically presented in tables or maps that can be difficult to interpret.

This project explores a different way to visualize these disparities using publicly available **population-level datasets**. Structural barriers are translated into algorithmically generated mazes, where each U.S. county receives a maze whose difficulty is determined by a composite score based on indicators such as supermarket distance, poverty, and transportation barriers. Counties with greater barriers generate larger and more complex mazes, providing a more intuitive way to explore differences in neighborhood food environments through an interactive **Python and Streamlit** application.

The idea was partly inspired by *Food Insecurity, Neighborhood Food Environment, and Health Disparities: State of the Science, Research Gaps and Opportunities* (Odoms-Young et al., 2024), which highlights how structural factors such as poverty, transportation barriers, and geographic food access contribute to health disparities. The project aims to demonstrate how data visualization and algorithmic techniques can help make complex public health patterns more intuitive and accessible!

---

## Live App: **[food-access-mazes.streamlit.app](https://food-access-mazes.streamlit.app/)**

This app allows users to explore food access barriers by region, generate maze visualizations based on barrier scores, compare states, and examine relationships between food access and chronic disease indicators.

---

## Data Sources

This project combines two public datasets. The original datasets were downloaded in their raw form before any cleaning or filtering.

| Dataset | Rows | Columns | Unit of Observation |
|------|------|------|------|
| USDA Food Access Research Atlas | 72,531 | 147 | Census tracts |
| Medicare Geographic Variation Dataset | 33,639 | 247 | Multiple geographic levels (county, state, national) |

---

### USDA Food Access Research Atlas

Provides census tract–level indicators related to food access and socioeconomic conditions across the United States.

**Key variables used:**

| Variable | Description | Unit / Scale | Mean | Min | Max |
|---|---|---|---|---|---|
| `lapop1share` | Population living more than 1 mile from a supermarket | Percent of population (%) | 53.97 | 0.00 | 100.00 |
| `lalowi1share` | Low-income population far from supermarkets | Percent of population (%) | 16.16 | 0.00 | 98.05 |
| `PovertyRate` | Population below the poverty line | Percent of population (%) | 13.70 | 0.00 | 99.50 |
| `MedianFamilyIncome` | Median family income | US dollars ($) | 78,216.87 | 2,499.00 | 250,001.00 |
| `vehicle_barrier_rate` | Households without vehicle access | Proportion of households (0–1) | 0.0245 | 0.00 | 0.6699 |

Across census tracts, the average share of residents living more than one mile from a supermarket is **53.97%**, with values ranging from **0% to 100%**. These indicators capture variation in geographic food access, poverty, income, and transportation barriers across communities.

Source:  
https://www.ers.usda.gov/data-products/food-access-research-atlas/

---

### Medicare Geographic Variation Dataset (CMS)

Provides healthcare utilization and chronic condition indicators used to examine relationships between food access barriers and chronic disease burden.

**Key variables used:**

| Variable | Description | Unit / Scale | Mean | Min | Max |
|---|---|---|---|---|---|
| `PQI03_DBTS_AGE_LT_65` | Diabetes admissions | Admissions per 100,000 beneficiaries | 607.02 | 267 | 1020 |
| `PQI05_COPD_ASTHMA_AGE_40_64` | COPD/asthma admissions | Admissions per 100,000 beneficiaries | 457.98 | 162 | 890 |
| `PQI07_HYPRTNSN_AGE_LT_65` | Hypertension admissions | Admissions per 100,000 beneficiaries | 214.85 | 72 | 878 |
| `PQI15_ASTHMA_AGE_LT_40` | Asthma admissions (<40) | Admissions per 100,000 beneficiaries | 72.83 | 0 | 181 |
| `BENES_TOTAL_CNT` | Medicare beneficiaries | Number of beneficiaries | 1,300,932 | 21,608 | 7,080,940 |

After filtering to **2023 observations** and aggregating metrics at the **state level**, the dataset shows an average of **607 diabetes-related admissions among Medicare beneficiaries under age 65**, with values ranging from **267 to 1,020 across states**. These indicators provide context for variation in chronic disease burden that can be compared alongside food access barriers.

Source:  
https://data.cms.gov/

---

## Methods

### 1. Data Cleaning

Raw datasets were cleaned using Python and the pandas library. The processing steps included filtering the data by geographic level and year, cleaning county and state identifiers, converting variables to numeric format where necessary, and exporting the processed datasets for downstream analysis.

Scripts used:
- scripts/clean_data.py
- scripts/clean_medicare_data.py
- scripts/clean_medicare_state_data.py

---

### 2. Food Access Score

A **composite barrier score** was created using normalized indicators representing structural barriers to accessing healthy food. The score combines several socioeconomic and geographic factors:

- **Food access:** share of the population living far from supermarkets  
- **Low-income food access:** share of low-income residents with limited grocery store access  
- **Poverty:** proportion of residents living below the federal poverty line  
- **Transportation barriers:** share of households without reliable vehicle access  
- **Income:** median family income (inverted to reflect economic disadvantage)

Each variable was normalized before being combined into a single composite score. Higher scores indicate greater structural barriers to accessing affordable and nutritious food.

---

### 3. Maze Generation

Food access scores are translated into maze complexity using a procedural maze generation algorithm. Regions with higher barrier scores produce larger and more difficult mazes, creating a visual metaphor for the difficulty of navigating local food environments.

Maze properties influenced by the score include:

- **Maze size:** higher barrier scores generate larger mazes with longer paths  
- **Branching complexity:** more structural barriers increase the number of branching paths and decision points  
- **Number of dead ends:** regions with higher barriers contain more dead ends, representing obstacles that make reaching healthy food more difficult

Implementation:
- scripts/maze_generator.py


---

### 4. Visualization

The final visualization is built using **Streamlit**, allowing users to interactively explore food access barriers and their relationship with health indicators across regions.

Through the application, users can:

- **Select regions:** choose a state or county to examine local food access conditions  
- **View food access indicators:** explore key socioeconomic and geographic variables contributing to the barrier score  
- **Generate a maze visualization:** see a maze whose complexity reflects the structural barriers to accessing healthy food  
- **Compare states:** view rankings and patterns across states based on average food access scores  
- **Explore correlations with health metrics:** examine relationships between food access barriers and chronic condition indicators such as diabetes and hypertension

---

## Example Output

The Streamlit application allows users to explore food access barriers interactively. The interface includes:

- A **region selector** for choosing a county or state  
- A **generated maze visualization** representing food access difficulty  
- **Summary statistics** describing key food access indicators  
- **Chronic condition indicators** from the Medicare dataset  
- **State rankings and comparison plots** showing broader patterns across regions  

### Example Region

Region: **Holmes County, Mississippi**  
Food Access Score: **0.81**  
Barrier Level: **High**

In this example, the high food access score reflects several structural barriers that make accessing healthy food more difficult. Major contributing factors may include:

- High poverty rates  
- Limited access to nearby supermarkets  
- Transportation barriers such as low vehicle availability  

These conditions result in a **larger and more complex maze**, visually representing the difficulty residents may face when trying to access healthy food options.

---

## Running the App

Install dependencies:

```bash
pip install requirements.txt
```

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

---

## Design Decisions

Several design choices were made to balance interpretability, usability, and project scope.

- **Composite score:** multiple indicators related to food access, poverty, income, and transportation were normalized and combined into a single metric. This simplifies interpretation and visualization, though it may hide variation across individual variables.

- **State-level health metrics:** Medicare health indicators were analyzed at the state level rather than the county level to reduce missing values and simplify comparisons across regions.

- **Maze metaphor:** maze complexity is used as a visual metaphor for structural barriers to accessing healthy food. This approach was inspired by narrative data visualizations such as those created by **The Pudding** (https://www.pudding.cool/), which often translate complex datasets into interactive visual experiences.

- **Streamlit interface:** Streamlit was chosen to build an interactive application quickly, allowing users to explore regions, visualize barrier scores, and examine relationships between food access and health indicators.

---

## Repository Structure

```bash

final-project-sarahmughal/

.
├── README.md
├── assets
│   └── desert.png
├── data
│   ├── FoodAccessResearchAtlasData2019.csv
│   ├── Medicare_GV_by_National_State_County_2023.csv
│   ├── descriptive_statistics.md
│   ├── food_access_with_scores.csv
│   ├── food_health_combined.csv
│   ├── medicare_chronic_conditions.csv
│   ├── medicare_county_metrics.csv
│   └── medicare_state_metrics.csv
├── presentation
│   └── food-access-mazes.pdf
├── references
│   └── Food Insecurity, Neighborhood Food Environment, and Health Disparities- State of the Science, Research Gaps and Opportunities.pdf
├── requirements.txt
├── scripts
│   ├── __pycache__
│   │   └── maze_generator.cpython-313.pyc
│   ├── clean_data.py
│   ├── clean_medicare_data.py
│   ├── clean_medicare_state_data.py
│   ├── create_score.py
│   ├── descriptivestats.py
│   ├── maze_generator.py
│   └── merge_food_health.py
└── streamlit_app.py

```

---

## References
Odoms-Young, A., Brown, A. G. M., Agurs-Collins, T., & Glanz, K. (2022).
Food Insecurity, Neighborhood Food Environment, and Health Disparities: State of the Science, Research Gaps and Opportunities.
American Journal of Clinical Nutrition.

USDA Economic Research Service.
Food Access Research Atlas.

Centers for Medicare & Medicaid Services (CMS).
Medicare Geographic Variation Dataset.