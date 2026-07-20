import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Amazon Sales Dashboard")

st.markdown("""
Welcome to the Amazon Product Analysis Dashboard.

This dashboard provides insights into product ratings,
discounts, prices and categories.
""")

# Load Dataset
df = pd.read_csv("amazon.csv")

# Cleaning
df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
)

df["discount_percentage"] = pd.to_numeric(
    df["discount_percentage"],
    errors="coerce"
)

# ======================
# Sidebar Filter
# ======================

st.sidebar.header("🔍 Filters")

categories = sorted(
    df["category"]
    .dropna()
    .unique()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(categories)
)

if selected_category != "All":
    filtered_df = df[
        df["category"] == selected_category
    ]
else:
    filtered_df = df

# ======================
# KPI Section
# ======================

st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Products",
    len(filtered_df)
)

col2.metric(
    "Average Rating",
    round(filtered_df["rating"].mean(), 2)
)

col3.metric(
    "Average Discount %",
    round(
        filtered_df["discount_percentage"].mean(),
        2
    )
)

st.divider()

# ======================
# Dataset Preview
# ======================

st.subheader("📄 Dataset Preview")

st.dataframe(filtered_df.head())

# ======================
# Top Categories Chart
# ======================

st.subheader("📊 Top Product Categories")

top_categories = (
    filtered_df["category"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=top_categories.values,
    y=top_categories.index,
    orientation="h",
    title="Top 10 Product Categories"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================
# Rating Distribution
# ======================

st.subheader("⭐ Rating Distribution")

fig2 = px.histogram(
    filtered_df,
    x="rating",
    nbins=20,
    title="Distribution of Product Ratings"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ======================
# Discount Analysis
# ======================

st.subheader("🎯 Top Categories by Average Discount")

discount_df = (
    filtered_df
    .groupby("category")["discount_percentage"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig3 = px.bar(
    x=discount_df.values,
    y=discount_df.index,
    orientation="h",
    title="Average Discount by Category",
    color=discount_df.values,
    color_continuous_scale="Viridis"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.divider()

st.markdown("""
### 📊 Amazon Sales Dashboard

Created using:
- Pandas
- Plotly
- Streamlit

Project by VenuSree
""")