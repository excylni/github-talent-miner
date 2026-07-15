import streamlit as st

st.set_page_config(
    page_title="GitHub Talent Miner",
    page_icon="⛏️",
    layout="wide"
)

st.title("⛏️ GitHub Talent Miner")
st.subheader("Exploring the European tech industry through public GitHub data")

st.markdown("""
This dashboard visualizes public GitHub profile data scraped from developers
from German cities.

### What's inside
- **Companies** — which companies have the most visible engineers on GitHub
- **Languages** — which programming languages dominate across the ecosystem

### How it was built
- **Extraction** — GitHub REST API (search + profile + repo endpoints)
- **Validation** — Pydantic data models
- **Storage** — Snowflake data warehouse
- **Transformation** — dbt (staging → marts)
- **Visualization** — Streamlit + Plotly

Use the sidebar to navigate between pages.
""")