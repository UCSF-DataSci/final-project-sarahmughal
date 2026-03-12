import base64
import hashlib
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from scripts.maze_generator import generate_maze_from_score

st.set_page_config(
    page_title="Navigating the Food Desert",
    layout="wide",
)


def get_base64_image(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


desert_path = Path("assets/desert.png")
desert_base64 = get_base64_image(desert_path) if desert_path.exists() else ""

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    f"""
    <style>
        .stApp {{
            background: linear-gradient(180deg, #fff8fb 0%, #fff3f7 45%, #fdf7f2 100%);
            color: #2b2b2b;
        }}

        .block-container {{
            max-width: 1250px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}

        .hero-section {{
            background:
                linear-gradient(rgba(255, 248, 251, 0.55), rgba(255, 248, 251, 0.82)),
                url("data:image/png;base64,{desert_base64}");
            background-size: cover;
            background-position: center bottom;
            background-repeat: no-repeat;
            border-radius: 28px;
            padding: 3.5rem 2rem 4rem 2rem;
            margin-bottom: 2rem;
            min-height: 360px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 8px 24px rgba(120, 90, 120, 0.08);
        }}

        .splash {{
            min-height: 78vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeIn 1.1s ease-in-out;
            text-align: center;
        }}

        .splash-title {{
            font-size: 4.2rem;
            font-weight: 800;
            line-height: 1.05;
            color: #2c1f57;
            margin-bottom: 0.6rem;
        }}

        .splash-subtitle {{
            font-size: 1.25rem;
            max-width: 760px;
            color: #5d5248;
            margin-bottom: 1.5rem;
        }}

        .main-title {{
            font-size: clamp(2.6rem, 5vw, 3.4rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 0.25rem;
            text-align: center;
            color: #2c1f57;
        }}

        .subtitle {{
            font-size: 1.2rem;
            text-align: center;
            color: #5d5248;
            margin-bottom: 1.2rem;
        }}

        .intro-text {{
            font-size: 1.05rem;
            max-width: 820px;
            margin: 0 auto 0 auto;
            text-align: center;
            color: #4f463f;
        }}

        .info-card {{
            background: rgba(255,255,255,0.55);
            padding: 1rem 1.2rem;
            border-radius: 18px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }}

        .small-note {{
            color: #6b625b;
            font-size: 0.95rem;
        }}

        .rank-card {{
            background: rgba(255,255,255,0.5);
            padding: 0.8rem 1rem;
            border-radius: 14px;
            margin-bottom: 0.55rem;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(18px); }}
            to   {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Session state for splash page
# -----------------------------
if "entered" not in st.session_state:
    st.session_state.entered = False


# -----------------------------
# Helpers
# -----------------------------
@st.cache_data
def load_food_data() -> pd.DataFrame:
    df = pd.read_csv("data/food_access_with_scores.csv")
    df["region"] = df["County"].astype(str) + ", " + df["State"].astype(str)

    numeric_cols = [
        "food_access_score",
        "PovertyRate",
        "MedianFamilyIncome",
        "lapop1share",
        "lalowi1share",
        "TractHUNV",
        "vehicle_barrier_rate",
        "Pop2010",
        "low_access_norm",
        "low_income_access_norm",
        "poverty_norm",
        "vehicle_norm",
        "income_inverse_norm",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["region", "food_access_score"])
    return df


@st.cache_data
def load_state_health_data() -> pd.DataFrame:
    df = pd.read_csv("data/medicare_state_metrics.csv")

    numeric_cols = [
        "BENES_TOTAL_CNT",
        "PQI03_DBTS_AGE_LT_65",
        "PQI05_COPD_ASTHMA_AGE_40_64",
        "PQI07_HYPRTNSN_AGE_LT_65",
        "PQI15_ASTHMA_AGE_LT_40",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


@st.cache_data
def aggregate_state_data(df: pd.DataFrame) -> pd.DataFrame:
    agg_dict = {"food_access_score": "mean"}

    for col in [
        "PovertyRate",
        "MedianFamilyIncome",
        "lapop1share",
        "lalowi1share",
        "vehicle_barrier_rate",
    ]:
        if col in df.columns:
            agg_dict[col] = "mean"

    state_df = (
        df.groupby("State", as_index=False)
        .agg(agg_dict)
        .sort_values("food_access_score", ascending=False)
        .reset_index(drop=True)
    )
    return state_df


@st.cache_data
def build_state_analysis_df(
    food_df: pd.DataFrame, health_df: pd.DataFrame
) -> pd.DataFrame:
    state_food = food_df.groupby("State", as_index=False).agg(
        {
            "food_access_score": "mean",
            "PovertyRate": "mean",
            "MedianFamilyIncome": "mean",
            "lapop1share": "mean",
            "lalowi1share": "mean",
            "vehicle_barrier_rate": "mean",
        }
    )

    merged = state_food.merge(health_df, on="State", how="left")
    return merged


def stable_seed(text: str) -> int:
    digest = hashlib.md5(text.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def classify_score(score: float) -> str:
    if score < 0.33:
        return "Low"
    if score < 0.66:
        return "Moderate"
    return "High"


def top_barriers(row: pd.Series) -> list[tuple[str, float]]:
    candidates = {
        "Low Access": row.get("low_access_norm"),
        "Low-Income Low Access": row.get("low_income_access_norm"),
        "Poverty": row.get("poverty_norm"),
        "Vehicle Barrier": row.get("vehicle_norm"),
        "Income Barrier": row.get("income_inverse_norm"),
    }
    clean = [(name, value) for name, value in candidates.items() if pd.notna(value)]
    clean.sort(key=lambda x: x[1], reverse=True)
    return clean[:3]


def metric_or_na(label: str, value, fmt: str = "{:.1f}"):
    if pd.notna(value):
        st.metric(label, fmt.format(value))
    else:
        st.metric(label, "N/A")


def format_percent_smart(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    value = float(value)
    if 0 <= value <= 1:
        return f"{value:.2%}"
    return f"{value:.2f}%"


def format_number_smart(value: float, decimals: int = 0) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:,.{decimals}f}"


# Approximate layout inspired by a US map grid
STATE_LAYOUT = [
    ["AK", None, None, None, None, None, None, None, None, None, "ME"],
    [None, None, None, None, None, None, None, None, None, "VT", "NH"],
    [None, "WA", "ID", "MT", "ND", "MN", None, "MI", None, "NY", None],
    [None, "OR", "UT", "WY", "SD", "IA", "WI", "OH", "PA", "NJ", "CT"],
    [None, "CA", "NV", "CO", "NE", "IL", "IN", "WV", "VA", "MD", "DE"],
    [None, None, "AZ", "NM", "KS", "MO", "KY", "TN", "SC", "NC", "DC"],
    ["HI", None, None, "OK", "LA", "AR", "MS", "AL", "GA", None, None],
    [None, None, None, None, "TX", None, None, None, None, "FL", None],
]

STATE_ABBREV_TO_NAME = {
    "AK": "Alaska",
    "ME": "Maine",
    "VT": "Vermont",
    "NH": "New Hampshire",
    "WA": "Washington",
    "ID": "Idaho",
    "MT": "Montana",
    "ND": "North Dakota",
    "MN": "Minnesota",
    "MI": "Michigan",
    "NY": "New York",
    "OR": "Oregon",
    "UT": "Utah",
    "WY": "Wyoming",
    "SD": "South Dakota",
    "IA": "Iowa",
    "WI": "Wisconsin",
    "OH": "Ohio",
    "PA": "Pennsylvania",
    "NJ": "New Jersey",
    "CT": "Connecticut",
    "CA": "California",
    "NV": "Nevada",
    "CO": "Colorado",
    "NE": "Nebraska",
    "IL": "Illinois",
    "IN": "Indiana",
    "WV": "West Virginia",
    "VA": "Virginia",
    "MD": "Maryland",
    "DE": "Delaware",
    "AZ": "Arizona",
    "NM": "New Mexico",
    "KS": "Kansas",
    "MO": "Missouri",
    "KY": "Kentucky",
    "TN": "Tennessee",
    "SC": "South Carolina",
    "NC": "North Carolina",
    "DC": "District of Columbia",
    "HI": "Hawaii",
    "OK": "Oklahoma",
    "LA": "Louisiana",
    "AR": "Arkansas",
    "MS": "Mississippi",
    "AL": "Alabama",
    "GA": "Georgia",
    "TX": "Texas",
    "FL": "Florida",
}


def mini_maze(state_name: str, score: float):
    seed = stable_seed(state_name)
    fig, _ = generate_maze_from_score(
        score=score,
        show_solution=False,
        seed=seed,
    )
    return fig


# -----------------------------
# Splash page
# -----------------------------
if not st.session_state.entered:
    st.markdown(
        """
        <div class="hero-section splash">
            <div class="splash-title">Navigating the Food Desert</div>
            <div class="splash-subtitle">
                Visualizing structural barriers to healthy food access as mazes
                using USDA Food Access Research Atlas data and state-level health metrics.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1, 1])
    with center:
        if st.button("Enter the project", use_container_width=True):
            st.session_state.entered = True
            st.rerun()

    st.stop()


# -----------------------------
# Main app
# -----------------------------
df = load_food_data()
state_df = aggregate_state_data(df)
state_health_df = load_state_health_data()
state_analysis_df = build_state_analysis_df(df, state_health_df)

st.markdown(
    """
    <div class="hero-section">
        <div class="main-title">Navigating the Food Desert</div>
        <div class="subtitle">Visualizing food access barriers and chronic condition burden as mazes</div>
        <div class="intro-text">
            This project transforms food access indicators into maze complexity and pairs them with
            state-level chronic condition metrics. Regions and states with greater structural barriers
            to healthy food access generate larger and more difficult mazes, creating an intuitive way
            to explore disparities in neighborhood food environments and health burden.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

view_mode = st.radio(
    "Choose a view",
    ["Single Region Explorer", "State Maze Map"],
    horizontal=True,
)

# -----------------------------
# View 1: Single Region Explorer
# -----------------------------
if view_mode == "Single Region Explorer":
    with st.sidebar:
        st.header("Controls")

        states = sorted(df["State"].dropna().unique())
        selected_state = st.selectbox("Filter by state", ["All"] + states)

        filtered_df = (
            df if selected_state == "All" else df[df["State"] == selected_state]
        )
        region_options = sorted(filtered_df["region"].unique())
        selected_region = st.selectbox("Select a region", region_options)

        show_solution = st.checkbox("Show maze solution path", value=True)

    row = df[df["region"] == selected_region].iloc[0]
    score = float(row["food_access_score"])
    difficulty = classify_score(score)
    seed = stable_seed(selected_region)

    selected_state_name = row["State"]
    state_health_row = state_health_df[state_health_df["State"] == selected_state_name]
    if not state_health_row.empty:
        state_health_row = state_health_row.iloc[0]
    else:
        state_health_row = pd.Series(dtype="object")

    controls_col, maze_col = st.columns([0.95, 1.55])

    with controls_col:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### Region Summary")
        st.write(f"**Selected region:** {selected_region}")
        if "CensusTract" in row.index and pd.notna(row.get("CensusTract")):
            st.write(f"**Census tract:** {row['CensusTract']}")
        st.metric("Food Access Score", f"{score:.3f}")
        st.metric("Barrier Level", difficulty)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### Core Indicators")

        if "Pop2010" in row.index:
            st.write(
                f"**Population (2010):** {format_number_smart(row.get('Pop2010'), 0)}"
            )

        if "PovertyRate" in row.index:
            st.write(
                f"**Poverty Rate:** {format_percent_smart(row.get('PovertyRate'))}"
            )

        if "MedianFamilyIncome" in row.index:
            income = row.get("MedianFamilyIncome")
            if pd.notna(income):
                st.write(f"**Median Family Income:** ${income:,.0f}")
            else:
                st.write("**Median Family Income:** N/A")

        if "lapop1share" in row.index:
            st.write(
                f"**Share beyond 1 mile from supermarket:** {format_percent_smart(row.get('lapop1share'))}"
            )

        if "lalowi1share" in row.index:
            st.write(
                f"**Low-income share beyond 1 mile:** {format_percent_smart(row.get('lalowi1share'))}"
            )

        if "TractHUNV" in row.index:
            st.write(
                f"**Households without a vehicle:** {format_number_smart(row.get('TractHUNV'), 0)}"
            )

        if "vehicle_barrier_rate" in row.index:
            st.write(
                f"**Vehicle Barrier Rate:** {format_percent_smart(row.get('vehicle_barrier_rate'))}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### Chronic Condition Indicators")
        st.write(f"**Shown at the state level for {selected_state_name}**")

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            metric_or_na(
                "Diabetes Admissions",
                state_health_row.get("PQI03_DBTS_AGE_LT_65"),
            )

        with metric_col2:
            metric_or_na(
                "COPD/Asthma Admissions",
                state_health_row.get("PQI05_COPD_ASTHMA_AGE_40_64"),
            )

        metric_col3, metric_col4 = st.columns(2)

        with metric_col3:
            metric_or_na(
                "Hypertension Admissions",
                state_health_row.get("PQI07_HYPRTNSN_AGE_LT_65"),
            )

        with metric_col4:
            metric_or_na(
                "Asthma Admissions (<40)",
                state_health_row.get("PQI15_ASTHMA_AGE_LT_40"),
            )

        if pd.notna(state_health_row.get("BENES_TOTAL_CNT")):
            st.write(
                f"**Total Medicare Beneficiaries (state):** {int(state_health_row['BENES_TOTAL_CNT']):,}"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        barriers = top_barriers(row)
        if barriers:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("### Strongest Score Contributors")
            for name, value in barriers:
                st.write(f"- **{name}:** {value:.3f}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### Interpretation")
        st.write(
            "Higher food access scores indicate greater structural barriers to healthy food access. "
            "These barriers are shown alongside state-level chronic condition indicators, including "
            "diabetes, hypertension, and asthma-related admissions."
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with maze_col:
        st.markdown("### Maze Visualization")
        fig, _ = generate_maze_from_score(
            score=score,
            show_solution=show_solution,
            seed=seed,
        )
        st.pyplot(fig, use_container_width=True)

        st.markdown("### What this maze means")
        st.write(
            f"In **{selected_region}**, the food access barrier score is **{score:.3f}**, "
            f"which falls in the **{difficulty.lower()}** barrier range. Regions with higher "
            "scores generate larger and denser mazes, representing the added complexity of "
            "reaching healthy food resources."
        )

    st.markdown("---")
    st.markdown("## Counties with the Hardest Food Access Mazes")

    county_scores = filtered_df.groupby(["State", "County"], as_index=False).agg(
        {"food_access_score": "mean"}
    )

    county_scores["region"] = county_scores["County"] + ", " + county_scores["State"]

    top_regions = (
        county_scores[["region", "food_access_score"]]
        .sort_values("food_access_score", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    for i, (_, r) in enumerate(top_regions.iterrows(), start=1):
        st.markdown(
            f'<div class="rank-card"><strong>{i}. {r["region"]}</strong> — {r["food_access_score"]:.3f}</div>',
            unsafe_allow_html=True,
        )

# -----------------------------
# View 2: State Maze Map
# -----------------------------
else:
    st.markdown("## State Maze Map")
    st.markdown(
        '<div class="small-note">Each state maze is based on the average county/tract-level food access score within that state.</div>',
        unsafe_allow_html=True,
    )

    state_score_lookup = dict(zip(state_df["State"], state_df["food_access_score"]))

    for row_states in STATE_LAYOUT:
        cols = st.columns(len(row_states))
        for i, abbrev in enumerate(row_states):
            with cols[i]:
                if abbrev is None:
                    st.write("")
                else:
                    state_name = STATE_ABBREV_TO_NAME.get(abbrev)
                    if state_name in state_score_lookup:
                        score = float(state_score_lookup[state_name])
                        st.markdown(
                            f"<div style='text-align:center; font-weight:700; color:#5b524a; margin-bottom:0.2rem;'>{abbrev}</div>",
                            unsafe_allow_html=True,
                        )
                        fig = mini_maze(state_name, score)
                        st.pyplot(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("## State Rankings")

    top_states = state_df.head(10).copy()
    for i, (_, r) in enumerate(top_states.iterrows(), start=1):
        st.markdown(
            f'<div class="rank-card"><strong>{i}. {r["State"]}</strong> — {r["food_access_score"]:.3f}</div>',
            unsafe_allow_html=True,
        )

# -----------------------------
# State-level analysis section
# -----------------------------
st.markdown("---")
st.markdown("## Food Access and Chronic Condition Burden")
st.markdown(
    """
    <div class="small-note">
        These visualizations compare average <strong>state-level food access scores</strong> with
        state-level Medicare chronic condition indicators.
    </div>
    """,
    unsafe_allow_html=True,
)

metric_options = {
    "Diabetes Admissions": "PQI03_DBTS_AGE_LT_65",
    "COPD/Asthma Admissions": "PQI05_COPD_ASTHMA_AGE_40_64",
    "Hypertension Admissions": "PQI07_HYPRTNSN_AGE_LT_65",
    "Asthma Admissions (<40)": "PQI15_ASTHMA_AGE_LT_40",
}

selected_metric_label = st.selectbox(
    "Choose a chronic condition metric for comparison",
    list(metric_options.keys()),
)

selected_metric_col = metric_options[selected_metric_label]

plot_df = state_analysis_df.dropna(
    subset=["food_access_score", selected_metric_col]
).copy()

analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs(
    ["Scatter + Bubble", "State Rankings", "Correlation Heatmap"]
)

with analysis_tab1:
    scatter_col, bubble_col = st.columns(2)

    with scatter_col:
        st.markdown("### Scatterplot")
        scatter = (
            alt.Chart(plot_df)
            .mark_circle(size=110, opacity=0.75, color="#8c4f7d")
            .encode(
                x=alt.X("food_access_score:Q", title="Average Food Access Score"),
                y=alt.Y(f"{selected_metric_col}:Q", title=selected_metric_label),
                tooltip=[
                    "State",
                    alt.Tooltip(
                        "food_access_score:Q", format=".3f", title="Food Access Score"
                    ),
                    alt.Tooltip(
                        f"{selected_metric_col}:Q",
                        format=".1f",
                        title=selected_metric_label,
                    ),
                    alt.Tooltip(
                        "BENES_TOTAL_CNT:Q", format=",", title="Medicare Beneficiaries"
                    ),
                ],
            )
            .properties(height=360)
            .interactive()
        )
        st.altair_chart(scatter, use_container_width=True)

    with bubble_col:
        st.markdown("### Bubble View")
        bubble = (
            alt.Chart(plot_df)
            .mark_circle(opacity=0.65, color="#d98ba6")
            .encode(
                x=alt.X("food_access_score:Q", title="Average Food Access Score"),
                y=alt.Y(f"{selected_metric_col}:Q", title=selected_metric_label),
                size=alt.Size("BENES_TOTAL_CNT:Q", title="Medicare Beneficiaries"),
                tooltip=[
                    "State",
                    alt.Tooltip(
                        "food_access_score:Q", format=".3f", title="Food Access Score"
                    ),
                    alt.Tooltip(
                        f"{selected_metric_col}:Q",
                        format=".1f",
                        title=selected_metric_label,
                    ),
                    alt.Tooltip(
                        "BENES_TOTAL_CNT:Q", format=",", title="Medicare Beneficiaries"
                    ),
                ],
            )
            .properties(height=360)
            .interactive()
        )
        st.altair_chart(bubble, use_container_width=True)

with analysis_tab2:
    st.markdown("### States Ranked by Food Access Score")

    bar_df = plot_df.sort_values("food_access_score", ascending=False).copy()

    bar = (
        alt.Chart(bar_df)
        .mark_bar(color="#7d5ba6")
        .encode(
            x=alt.X("food_access_score:Q", title="Average Food Access Score"),
            y=alt.Y("State:N", sort="-x", title="State"),
            tooltip=[
                "State",
                alt.Tooltip(
                    "food_access_score:Q", format=".3f", title="Food Access Score"
                ),
                alt.Tooltip(
                    f"{selected_metric_col}:Q",
                    format=".1f",
                    title=selected_metric_label,
                ),
            ],
        )
        .properties(height=650)
    )

    st.altair_chart(bar, use_container_width=True)

with analysis_tab3:
    st.markdown("### Correlation Heatmap")

    corr_cols = [
        "food_access_score",
        "PQI03_DBTS_AGE_LT_65",
        "PQI05_COPD_ASTHMA_AGE_40_64",
        "PQI07_HYPRTNSN_AGE_LT_65",
        "PQI15_ASTHMA_AGE_LT_40",
    ]

    corr_df = state_analysis_df[corr_cols].apply(pd.to_numeric, errors="coerce")
    corr_matrix = corr_df.corr(numeric_only=True)

    corr_long = corr_matrix.reset_index().melt(id_vars="index")
    corr_long.columns = ["Metric1", "Metric2", "Correlation"]

    heatmap = (
        alt.Chart(corr_long)
        .mark_rect()
        .encode(
            x=alt.X("Metric1:N", title=""),
            y=alt.Y("Metric2:N", title=""),
            color=alt.Color(
                "Correlation:Q",
                scale=alt.Scale(domain=[-1, 1], range=["#f4d6e2", "#7d5ba6"]),
            ),
            tooltip=[alt.Tooltip("Correlation:Q", format=".2f")],
        )
        .properties(height=320)
    )

    st.altair_chart(heatmap, use_container_width=True)
    st.dataframe(corr_matrix, use_container_width=True)

st.markdown("---")
st.caption(
    "Data sources: USDA Food Access Research Atlas and state-level Medicare health metrics. "
    "Maze visualizations are generated from a composite food access barrier score."
)
