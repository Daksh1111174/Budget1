# ===========================
# AUTO INSTALL DEPENDENCIES
# ===========================
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Auto-install required modules
for lib in ["streamlit", "pandas", "plotly"]:
    try:
        __import__(lib)
    except ImportError:
        install(lib)

# ===========================
# IMPORTS
# ===========================
import streamlit as st
import pandas as pd
import plotly.express as px

# ===========================
# LOAD DATA
# ===========================
@st.cache_data
def load_data():
    return pd.read_csv("Budget 2014-2025.csv")   # <-- your file

df = load_data()

# ===========================
# PAGE UI
# ===========================
st.set_page_config(page_title="Indian Budget Analysis", layout="wide")
st.title("📊 Indian Budget Analysis — 2014 to 2025")

# Filters
years = sorted(df["Year"].unique())
ministries = sorted(df["Ministry Name"].unique())

selected_year = st.sidebar.selectbox("Select Year", years)
selected_ministry = st.sidebar.selectbox("Select Ministry", ["All"] + ministries)

# Apply filter
filtered_df = df[df["Year"] == selected_year]

if selected_ministry != "All":
    filtered_df = filtered_df[filtered_df["Ministry Name"] == selected_ministry]

# ===========================
# DATA TABLE
# ===========================
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# ===========================
# BAR CHART
# ===========================
st.subheader(f"Budget Breakdown — {selected_year}")

fig = px.bar(
    filtered_df,
    x="Ministry Name",
    y="Total Plan & Non-Plan",
    title=f"Total Budget for {selected_year}",
    labels={"Total Plan & Non-Plan": "Total Budget"},
)
st.plotly_chart(fig, use_container_width=True)

# ===========================
# LINE CHART — trend by ministry
# ===========================
if selected_ministry != "All":
    st.subheader(f"Budget Trend for {selected_ministry}")

    ministry_trend = df[df["Ministry Name"] == selected_ministry]

    fig2 = px.line(
        ministry_trend,
        x="Year",
        y="Total Plan & Non-Plan",
        title=f"Budget Trend — {selected_ministry}",
        markers=True,
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===========================
# DOWNLOAD CSV
# ===========================
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="Budget_2014_2025.csv",
    mime="text/csv"
)
