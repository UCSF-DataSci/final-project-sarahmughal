import pandas as pd
import numpy as np

df = pd.read_csv("data/processed_food_access.csv")


def normalize(col):
    col = pd.to_numeric(col, errors="coerce")
    min_val = col.min()
    max_val = col.max()

    if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
        return pd.Series(0, index=col.index, dtype=float)

    return (col - min_val) / (max_val - min_val)


# ensure numeric columns are numeric
numeric_cols = [
    "PovertyRate",
    "lapop1share",
    "lalowi1share",
    "vehicle_barrier_rate",
    "MedianFamilyIncome",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# drop rows missing any score inputs
df = df.dropna(subset=numeric_cols).copy()

# normalize barrier variables
df["poverty_norm"] = normalize(df["PovertyRate"]).clip(0, 1)
df["low_access_norm"] = normalize(df["lapop1share"]).clip(0, 1)
df["low_income_access_norm"] = normalize(df["lalowi1share"]).clip(0, 1)
df["vehicle_norm"] = normalize(df["vehicle_barrier_rate"]).clip(0, 1)

# income is reversed: lower income = higher barrier
income_norm = normalize(df["MedianFamilyIncome"]).clip(0, 1)
df["income_inverse_norm"] = 1 - income_norm

# composite score
df["food_access_score"] = (
    0.35 * df["low_access_norm"]
    + 0.25 * df["low_income_access_norm"]
    + 0.20 * df["poverty_norm"]
    + 0.10 * df["vehicle_norm"]
    + 0.10 * df["income_inverse_norm"]
).clip(0, 1)

df.to_csv("data/food_access_with_scores.csv", index=False)

print(df[["region", "food_access_score"]].head())
print(df[["food_access_score"]].describe())
