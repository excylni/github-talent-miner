import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import query

# 1. Page Configuration
st.set_page_config(page_title="Company Insights", layout="wide")

# 2. Sidebar Filters
st.sidebar.header("Dashboard Controls")
top_n = st.sidebar.slider("Show top N companies", min_value=5, max_value=100, value=20)

# 3. Data Loading & Cleaning
df = query("SELECT * FROM mart_companies ORDER BY DEVELOPER_COUNT DESC")
df.columns = [c.lower() for c in df.columns]
df_filtered = df.head(top_n)

# 4. Header Section
st.title("Corporate GitHub Footprint")
st.markdown("An analysis of which companies employ the highest number of public GitHub engineers.")
st.markdown("---")

# 5. Key Metrics (Moved to the top for immediate context)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Tracked Companies", value=f"{len(df):,}")
with col2:
    st.metric(label="Market Leader", value=df.iloc[0]["company"])
with col3:
    # Formatted with commas for readability (e.g., 10,000 instead of 10000)
    max_devs = int(df.iloc[0]["developer_count"])
    st.metric(label="Peak Developer Count", value=f"{max_devs:,}")

st.markdown("### Ranking Overview")

# 6. Optimized Main Chart
# We use a clean sequence of colors instead of a continuous scale color-bar to reduce visual noise.
fig = px.bar(
    df_filtered,
    x="developer_count",
    y="company",
    orientation="h",
    text="developer_count", # Adds data labels directly on the bars
    labels={"developer_count": "Engineers", "company": "Company"},
)

# Professional Plotly Styling adjustments
fig.update_traces(
    marker_color="#2b5c8f",  # Solid, professional brand color
    textposition="outside",   # Places numbers outside the bars so they are readable
    cliponaxis=False          # Prevents the text numbers from getting cut off at the edge
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="", 
    yaxis_title="",
    margin=dict(l=20, r=20, t=10, b=10), # Tight margins to remove dead space
    height=200 + (top_n * 20),           # Dynamic height so the chart stretches cleanly if N changes
    paper_bgcolor="rgba(0,0,0,0)",       # Transparent background to blend with Streamlit theme
    plot_bgcolor="rgba(0,0,0,0)",
)

# Hide distracting background grid lines
fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
fig.update_yaxes(showgrid=False)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# 7. Raw Data Inspection
with st.expander("🔍 Inspect Raw Data Table"):
    st.dataframe(
        df_filtered[["company", "developer_count"]], 
        use_container_width=True,
        hide_index=True
    )