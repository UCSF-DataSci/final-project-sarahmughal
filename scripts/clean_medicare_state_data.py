import pandas as pd

STATE_ABBREV_TO_NAME = {
    "AK": "Alaska",
    "AL": "Alabama",
    "AR": "Arkansas",
    "AZ": "Arizona",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DC": "District of Columbia",
    "DE": "Delaware",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "IA": "Iowa",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "MA": "Massachusetts",
    "MD": "Maryland",
    "ME": "Maine",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MO": "Missouri",
    "MS": "Mississippi",
    "MT": "Montana",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "NE": "Nebraska",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NV": "Nevada",
    "NY": "New York",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VA": "Virginia",
    "VT": "Vermont",
    "WA": "Washington",
    "WI": "Wisconsin",
    "WV": "West Virginia",
    "WY": "Wyoming",
}

df = pd.read_csv("data/Medicare_GV_by_National_State_County_2023.csv", low_memory=False)

df = df[df["BENE_GEO_LVL"] == "State"]
df = df[df["BENE_AGE_LVL"] == "All"]
df = df[df["YEAR"] == 2023].copy()

# convert state abbreviations to full names
df["State"] = df["BENE_GEO_DESC"].astype(str).str.strip().map(STATE_ABBREV_TO_NAME)

cols = [
    "State",
    "BENES_TOTAL_CNT",
    "PQI03_DBTS_AGE_LT_65",
    "PQI05_COPD_ASTHMA_AGE_40_64",
    "PQI07_HYPRTNSN_AGE_LT_65",
    "PQI15_ASTHMA_AGE_LT_40",
]

df = df[cols].copy()

df.to_csv("data/medicare_state_metrics.csv", index=False)

print(df.head())
print(df[df["State"] == "California"])
