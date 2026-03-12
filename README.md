# Food Access Mazes: Visualizing Barriers to Healthy Food Access

## Overview

This project explores a different way to visualize disparities in access to healthy food. Instead of relying only on traditional charts or tables, structural barriers are translated into **algorithmically generated mazes**. Regions with greater barriers to food access generate larger and more complex mazes, while regions with fewer barriers produce simpler ones.

The goal is to create a visualization that makes differences in neighborhood food environments easier to understand. The project combines **public health data analysis, procedural maze generation, and interactive visualization using Python and Streamlit.**

---

## Live App

Interactive App:  

**[(Add Streamlit deployment link here)](https://food-access-mazes.streamlit.app/)**

The app allows users to:

- Explore food access barriers by region  
- Generate maze visualizations based on barrier scores  
- Compare states  
- View relationships between food access and chronic disease indicators  

---

## Background

Limited access to affordable, nutritious food is associated with poorer diet quality and increased risk of diseases such as diabetes and cardiovascular disease. These disparities often affect communities with lower socioeconomic resources and limited transportation access.

Public health research typically measures these barriers using indicators such as poverty rates, distance to grocery stores, and vehicle availability. However, these indicators are usually presented in statistical tables or maps. This project explores whether structural barriers can instead be represented through **navigational complexity**, using mazes as a visual metaphor.

---

## Data Sources

This project combines two public datasets.

### USDA Food Access Research Atlas

Provides census-tract level indicators related to food access and socioeconomic conditions.

Key variables used:

| Feature | Description |
|------|------|
| `lapop1share` | Population living more than 1 mile from a supermarket |
| `lalowi1share` | Low-income population far from supermarkets |
| `PovertyRate` | Population below the poverty line |
| `MedianFamilyIncome` | Median family income |
| `vehicle_barrier_rate` | Households without vehicle access |

Source:  
https://www.ers.usda.gov/data-products/food-access-research-atlas/

---

### Medicare Geographic Variation Dataset (CMS)

Provides healthcare utilization and chronic condition indicators.

Variables used:

| Variable | Description |
|------|------|
| `PQI03_DBTS_AGE_LT_65` | Diabetes admissions |
| `PQI05_COPD_ASTHMA_AGE_40_64` | COPD/asthma admissions |
| `PQI07_HYPRTNSN_AGE_LT_65` | Hypertension admissions |
| `PQI15_ASTHMA_AGE_LT_40` | Asthma admissions (<40) |
| `BENES_TOTAL_CNT` | Medicare beneficiaries |

Source:  
https://data.cms.gov/

---

## Methods

### 1. Data Cleaning

Raw datasets were cleaned using **Python and pandas**.

Processing steps include:

- filtering geographic levels and years  
- cleaning county and state identifiers  
- converting values to numeric format  
- exporting processed datasets for analysis  

Scripts used:
- scripts/clean_data.py
- scripts/clean_medicare_data.py
- scripts/clean_medicare_state_data.py


---

### 2. Food Access Score

A **composite barrier score** was created using normalized indicators related to:

- food access  
- poverty  
- transportation barriers  
- income  

Higher scores indicate greater structural barriers to healthy food access.

---

### 3. Maze Generation

Food access scores are translated into maze complexity using a procedural maze generator.

Maze properties affected by the score include:

- maze size  
- branching complexity  
- number of dead ends  

Implementation:
- scripts/maze_generator.py


---

### 4. Visualization

The final visualization is built using **Streamlit**.

Users can:

- select regions  
- view food access indicators  
- generate a maze representing structural barriers  
- compare states  
- explore correlations with health metrics  

---

## Example Output

Example interface features include:

- region selector  
- generated maze visualization  
- region summary statistics  
- chronic condition indicators  
- state rankings and comparison plots  

Example interpretation:
- Region: Holmes County, Mississippi
- Food Access Score: 0.81
- Barrier Level: High

Major contributing barriers may include:

- high poverty  
- limited supermarket access  
- transportation barriers  

---

## Running the App

Install dependencies:

```bash
pip install streamlit pandas altair matplotlib numpy
```

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

---

## Design Decisions

Some key design choices include:

- **Composite score** — simplifies multiple indicators into one metric, though it may hide variation across individual variables.

- **State-level health metrics** — used for easier comparison and fewer missing values.

- **Maze metaphor** — provides an intuitive representation of structural barriers but is not intended as a formal statistical model.

- **Streamlit interface** — chosen for quick development and interactive exploration.

---

## Repository Structure

```bash

final-project-sarahmughal/

├── streamlit_app.py
├── README.md

├── assets/
│   └── desert.png

├── data/
│   ├── FoodAccessResearchAtlasData2019.csv
│   ├── Medicare_GV_by_National_State_County_2023.csv
│   ├── food_access_with_scores.csv
│   ├── medicare_state_metrics.csv
│   └── processed_food_access.csv

├── scripts/
│   ├── clean_data.py
│   ├── clean_medicare_data.py
│   ├── clean_medicare_state_data.py
│   ├── create_score.py
│   ├── merge_food_health.py
│   └── maze_generator.py

└── references/
    └── Food Insecurity, Neighborhood Food Environment, and Health Disparities.pdf

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