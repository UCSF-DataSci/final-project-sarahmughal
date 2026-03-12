import pandas as pd

df = pd.read_csv("data/Medicare_GV_by_National_State_County_2023.csv", low_memory=False)

# Keep county rows
df = df[df["BENE_GEO_LVL"] == "County"]

# Keep all ages
df = df[df["BENE_AGE_LVL"] == "All"]

# Keep 2023
df = df[df["YEAR"] == 2023]

# Create county FIPS
df["county_fips"] = (
    pd.to_numeric(df["BENE_GEO_CD"], errors="coerce")
    .astype("Int64")
    .astype(str)
    .str.zfill(5)
)

# Clean county names (remove "AK-" etc)
df["County"] = df["BENE_GEO_DESC"].str.split("-", n=1).str[1]

cols = [
    "county_fips",
    "County",
    "BENES_TOTAL_CNT",
    "PQI03_DBTS_AGE_LT_65",
    "PQI05_COPD_ASTHMA_AGE_40_64",
    "PQI15_ASTHMA_AGE_LT_40",
]

cols = [c for c in cols if c in df.columns]

df = df[cols]

df.to_csv("data/medicare_chronic_conditions.csv", index=False)

print(df.head())
