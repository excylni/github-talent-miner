import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from connection import query

# 1. Page Configuration
st.set_page_config(page_title="Tech Stack Insights", layout="wide")

# 2. Sidebar Controls
st.sidebar.header("Dashboard Controls")
top_n = st.sidebar.slider("Show top N languages", min_value=5, max_value=30, value=15)

# 3. Data Processing
df = query("SELECT * FROM mart_languages ORDER BY DEVELOPER_COUNT DESC")
df.columns = [c.lower() for c in df.columns]

# Calculate absolute market share BEFORE filtering so the metrics remain mathematically accurate
total_devs = df["developer_count"].sum()
df["market_share"] = (df["developer_count"] / total_devs) * 100

df_filtered = df.head(top_n)

# 4. Header Section
st.title("💻 European Language Dominance")
st.markdown("Analyzing developer volume and ecosystem influence across the European tech scene.")
st.markdown("---")

# 5. Core Layout: Volume vs. Influence Side-by-Side
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Ecosystem Volume")
    
    # We use 'text' to put the market share directly on the bars, removing the need for a pie chart
    fig_vol = px.bar(
        df_filtered,
        x="developer_count",
        y="primary_language",
        orientation="h",
        text="market_share",
        labels={"developer_count": "Engineers", "primary_language": "Language"},
    )
    
    fig_vol.update_traces(
        marker_color="#d9383a",  # Unified crimson red theme
        texttemplate="%{text:.1f}%",  # Formats the bar text labels as "X.X%"
        textposition="outside",
        cliponaxis=False
    )
    
    fig_vol.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="", yaxis_title="",
        margin=dict(l=10, r=40, t=10, b=10),
        height=150 + (top_n * 25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    fig_vol.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig_vol.update_yaxes(showgrid=False)
    
    st.plotly_chart(fig_vol, use_container_width=True, config={"displayModeBar": False})

with col2:
    st.markdown("### Engineer Influence")
    
    # Vertical ranking for seniority/influence proxy
    fig_inf = px.bar(
        df_filtered.sort_values("avg_followers", ascending=False),
        x="primary_language",
        y="avg_followers",
        text="avg_followers",
        labels={"avg_followers": "Avg Followers", "primary_language": "Language"},
    )
    
    fig_inf.update_traces(
        marker_color="#e07a5f",  # Secondary muted orange/coral that complements the red
        texttemplate="%{text:.0f}",
        textposition="outside",
        cliponaxis=False
    )
    
    fig_inf.update_layout(
        xaxis={"categoryorder": "total descending"},
        xaxis_title="", yaxis_title="",
        margin=dict(l=10, r=10, t=10, b=10),
        height=150 + (top_n * 25),  # Keep heights identical for symmetry
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    fig_inf.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig_inf.update_xaxes(showgrid=False)
    
    st.plotly_chart(fig_inf, use_container_width=True, config={"displayModeBar": False})

# 6. Raw Data Table
st.markdown("---")
with st.expander("🔍 Inspect Complete Metrics"):
    # Format columns nicely for presentation
    df_display = df_filtered.copy()
    df_display["market_share"] = df_display["market_share"].map("{:.2f}%".format)
    df_display["developer_count"] = df_display["developer_count"].map("{:,}".format)
    df_display["avg_followers"] = df_display["avg_followers"].map("{:.1f}".format)
    
    st.dataframe(
        df_display[["primary_language", "developer_count", "market_share", "avg_followers"]],
        use_container_width=True,
        hide_index=True
    )