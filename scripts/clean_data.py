import pandas as pd

df = pd.read_csv("data/FoodAccessResearchAtlasData2019.csv")

cols = [
    "State",
    "County",
    "CensusTract",
    "Pop2010",
    "PovertyRate",
    "MedianFamilyIncome",
    "lapop1share",
    "lalowi1share",
    "TractHUNV",
]

df = df[cols].copy()

# remove missing values
df = df.dropna()

# create vehicle access rate
df["vehicle_barrier_rate"] = df["TractHUNV"] / df["Pop2010"]

# combine location
df["region"] = df["County"] + ", " + df["State"]

df.to_csv("data/processed_food_access.csv", index=False)

print("Clean dataset shape:", df.shape)
print(df.head())
