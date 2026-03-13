import pandas as pd

# load raw datasets
df_food_raw = pd.read_csv("data/FoodAccessResearchAtlasData2019.csv")

df_medicare_raw = pd.read_csv(
    "data/Medicare_GV_by_National_State_County_2023.csv",
    low_memory=False,
    na_values=["*"],
)

# load cleaned datasets
df_food_clean = pd.read_csv("data/food_access_with_scores.csv")

df_medicare_clean = pd.read_csv(
    "data/medicare_state_metrics.csv",
    na_values=["*"],
)

# load merged dataset
df_combined = pd.read_csv("data/food_health_combined.csv")

# convert numeric columns for food dataset
food_cols = [
    "lapop1share",
    "lalowi1share",
    "PovertyRate",
    "MedianFamilyIncome",
    "vehicle_barrier_rate",
]

for col in food_cols:
    df_food_clean[col] = pd.to_numeric(df_food_clean[col], errors="coerce")

# convert numeric columns for health dataset
health_cols = [
    "PQI03_DBTS_AGE_LT_65",
    "PQI05_COPD_ASTHMA_AGE_40_64",
    "PQI07_HYPRTNSN_AGE_LT_65",
    "PQI15_ASTHMA_AGE_LT_40",
    "BENES_TOTAL_CNT",
]

for col in health_cols:
    df_medicare_clean[col] = pd.to_numeric(df_medicare_clean[col], errors="coerce")

# calculate descriptive statistics
food_stats = df_food_clean[food_cols].describe().round(2)
health_stats = df_medicare_clean[health_cols].describe().round(2)

# create tables for readme
food_readme = food_stats.loc[["mean", "min", "max"]].T
food_readme.columns = ["Mean", "Min", "Max"]

health_readme = health_stats.loc[["mean", "min", "max"]].T
health_readme.columns = ["Mean", "Min", "Max"]

# create output markdown file
with open("data/descriptive_statistics.md", "w") as f:
    f.write("# Dataset Descriptive Statistics\n\n")

    f.write("## Dataset Dimensions\n\n")

    f.write("| dataset | rows | columns |\n")
    f.write("|--------|------|------|\n")

    f.write(
        f"| food access atlas (raw) | {df_food_raw.shape[0]:,} | {df_food_raw.shape[1]} |\n"
    )

    f.write(
        f"| medicare geographic variation (raw) | {df_medicare_raw.shape[0]:,} | {df_medicare_raw.shape[1]} |\n"
    )

    f.write(
        f"| food access dataset (cleaned) | {df_food_clean.shape[0]:,} | {df_food_clean.shape[1]} |\n"
    )

    f.write(
        f"| medicare state metrics (cleaned) | {df_medicare_clean.shape[0]:,} | {df_medicare_clean.shape[1]} |\n"
    )

    f.write(
        f"| final merged dataset | {df_combined.shape[0]:,} | {df_combined.shape[1]} |\n\n"
    )

    f.write("## Food Access Variables\n\n")
    f.write(food_readme.to_markdown())
    f.write("\n\n")

    f.write("## Medicare Health Indicators (state level)\n\n")
    f.write(health_readme.to_markdown())
    f.write("\n")

print("descriptive statistics saved to: data/descriptive_statistics.md")
