# Health Access Mazes  
### Visualizing Structural Barriers to Healthcare and Food Access in the United States

## Overview

Access to healthcare and healthy food is influenced by a variety of structural factors, including poverty, insurance coverage, transportation access, and the availability of healthcare providers and grocery stores. These factors are often studied as part of the broader **social determinants of health**, but traditional statistical summaries can make disparities difficult to intuitively understand.

This project explores a novel way to represent these barriers by translating them into **algorithmically generated mazes**. Regions with greater structural barriers to health resources generate **more complex mazes**, while regions with fewer barriers produce simpler ones. The goal is to create a visualization that makes differences in health access more tangible and easier to interpret.

This project combines **public health data analysis, algorithmic maze generation, and interactive visualization** using Python.

---

## Problem Statement

Many communities face overlapping barriers that make accessing healthcare and healthy food difficult. These barriers include:

- Lack of health insurance  
- Shortages of healthcare providers  
- Limited access to grocery stores  
- Poverty and transportation limitations  

While these factors are commonly analyzed in public health research, they are usually presented through tables or statistical models. This project investigates whether these structural barriers can be **represented visually as navigational complexity**, allowing users to experience disparities through interactive maze structures.

---

## Dataset

The dataset used in this project will be drawn from publicly available **county-level or state-level public health datasets used in peer-reviewed research**.

Potential sources include:

- USDA Food Access Research Atlas  
- County Health Rankings  
- CDC PLACES  
- American Community Survey (ACS)  
- Area Health Resource File (AHRF)  

These datasets contain indicators related to healthcare access, food access, and socioeconomic conditions.

### Example Input Features

| Feature | Description |
|--------|-------------|
| uninsured_rate | Percent of population without health insurance |
| primary_care_physicians | Primary care physicians per 100,000 residents |
| food_access_low_income | Percent of low-income population far from grocery stores |
| poverty_rate | Percent of population below the federal poverty line |
| no_vehicle_access | Percent of households without vehicle access |
| mental_health_provider_ratio | Availability of mental health providers |

The final dataset will include multiple indicators representing **barriers to healthcare and food access**.

### Dataset Dimensions

Expected dataset scale:

- ~3,000 counties (or 50 states)  
- 5–10 health access indicators  

---

## Methods

The project consists of four major steps.

### 1. Data Processing

Public health indicators are cleaned and standardized using Python tools such as:

- `pandas`
- `numpy`

Variables are normalized to allow comparison across indicators.

---

### 2. Health Access Score

A composite **Health Access Score** is created by combining multiple indicators representing structural barriers to health resources.

Example formulation:

```python
health_access_score = (
    0.25 * uninsured_rate +
    0.25 * food_access_barrier +
    0.20 * poverty_rate +
    0.15 * provider_shortage +
    0.15 * transportation_barrier
)

Higher scores indicate greater barriers to healthcare and food access.

---

### 3. Maze Generation

The composite score is used to parameterize a **maze generation algorithm**.

Maze properties influenced by the score may include:

- Maze size  
- Number of dead ends  
- Branching complexity  

Mazes will be generated using a **depth-first search (DFS) recursive backtracking algorithm**, a common approach for procedural maze generation.

---

### 4. Visualization

Generated mazes will be displayed using Python visualization tools such as:

- `matplotlib`
- `streamlit` (for interactive exploration)

Users will be able to:

- Select a region (state or county)  
- View its health access indicators  
- See a maze representing structural barriers  

---

## Example Output

Example Interface:

Selected Region: Holmes County, Mississippi
Health Access Score: 0.81

---

Major contributing barriers:

- High poverty rate  
- Limited grocery store access  
- Low physician availability  

Generated output:

- Maze visualization representing health access difficulty  
- Indicator summary for the selected region  

---

## Repository Structure
health-access-mazes/
│
├── README.md
│
├── data/
│ ├── raw_data.csv
│ └── processed_data.csv
│
├── scripts/
│ ├── data_processing.py
│ ├── scoring_model.py
│ └── maze_generator.py
│
├── app/
│ └── streamlit_app.py
│
├── notebooks/
│ └── exploration.ipynb
│
└── presentation/
└── slides.pdf
