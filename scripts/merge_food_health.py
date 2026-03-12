import pandas as pd

food = pd.read_csv("data/food_access_with_scores.csv")
medicare = pd.read_csv("data/medicare_chronic_conditions.csv")

# derive county FIPS from tract FIPS in USDA data
food["county_fips"] = (
    food["CensusTract"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    .str.zfill(11)
    .str[:5]
)

# force medicare county_fips to string too
medicare["county_fips"] = (
    pd.to_numeric(medicare["county_fips"], errors="coerce")
    .astype("Int64")
    .astype(str)
    .str.zfill(5)
)

# aggregate food data to county level
agg_dict = {
    "food_access_score": "mean",
    "PovertyRate": "mean",
    "MedianFamilyIncome": "mean",
    "lapop1share": "mean",
    "lalowi1share": "mean",
    "vehicle_barrier_rate": "mean",
}

for col in ["Pop2010", "TractHUNV"]:
    if col in food.columns:
        agg_dict[col] = "mean"

county_food = food.groupby(["county_fips", "State", "County"], as_index=False).agg(
    agg_dict
)

merged = county_food.merge(medicare, on="county_fips", how="left")

merged.to_csv("data/food_health_combined.csv", index=False)

print(merged.head())
print(merged.dtypes[["county_fips"]])
print("Rows:", merged.shape[0])
