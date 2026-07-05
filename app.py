import streamlit as st
import pandas as pd

# ===========================
# Custom Modules
# ===========================

from utils.styles import load_css
from utils.cards import (
    recommendation_card,
    nutrition_metrics,
    health_progress,
    ai_explanation
)

from utils.charts import (
    calories_chart,
    protein_chart,
    health_score_chart,
    nutrition_pie,
    health_gauge
)

from models.recommender import (
    build_ai_engine,
    smart_recommend_by_profile
)

# ===========================
# Page Config
# ===========================

st.set_page_config(

    page_title="Nutreva",

    page_icon="🥗",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ===========================
# Load CSS
# ===========================

load_css()

# ===========================
# Load AI Engine
# ===========================

@st.cache_resource
def load_ai():

    return build_ai_engine()

df, vectorizer, tfidf_matrix, similarity_matrix = load_ai()

# ===========================
# Header
# ===========================

st.markdown("""

<div class="hero">

<h1>🥗 Nutreva</h1>

<p>

AI Powered Nutrition Recommendation Platform

</p>

</div>

""", unsafe_allow_html=True)

# ===========================
# Metrics
# ===========================

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown("""

<div class="metric-card">

<div class="metric-title">

Foods

</div>

<div class="metric-value">

2396

</div>

</div>

""",unsafe_allow_html=True)

with c2:

    st.markdown("""

<div class="metric-card">

<div class="metric-title">

Features

</div>

<div class="metric-value">

20

</div>

</div>

""",unsafe_allow_html=True)

with c3:

    st.markdown("""

<div class="metric-card">

<div class="metric-title">

AI Model

</div>

<div class="metric-value">

TF-IDF

</div>

</div>

""",unsafe_allow_html=True)

with c4:

    st.markdown("""

<div class="metric-card">

<div class="metric-title">

Engine

</div>

<div class="metric-value">

Ready

</div>

</div>

""",unsafe_allow_html=True)

st.divider()
# ==========================================================
# Sidebar
# ==========================================================

st.sidebar.title("⚙ AI Preferences")

goal = st.sidebar.selectbox(
    "🎯 Health Goal",
    sorted(df["health_goal"].dropna().unique())
)

meal_type = st.sidebar.selectbox(
    "🍽 Meal Type",
    sorted(df["meal_type"].dropna().unique())
)

diet_type = st.sidebar.selectbox(
    "🥦 Diet Type",
    sorted(df["diet_type"].dropna().unique())
)

cuisine = st.sidebar.selectbox(
    "🌍 Cuisine",
    sorted(df["cuisine"].dropna().unique())
)

top_n = st.sidebar.slider(
    "📌 Number of Recommendations",
    min_value=3,
    max_value=10,
    value=5
)

recommend_btn = st.sidebar.button(
    "🚀 Get AI Recommendations",
    use_container_width=True
)

# ==========================================================
# Main Layout
# ==========================================================

left_col, right_col = st.columns([2.2, 1])

if not recommend_btn:

    with left_col:
        st.info(
            "👈 Select your preferences from the sidebar and click **Get AI Recommendations**."
        )

    with right_col:
        st.success("✅ AI Engine Ready")
        st.write(f"🍽 Foods : **{len(df)}**")
        st.write("🤖 Model : **TF-IDF + Cosine Similarity**")
        st.write("❤️ Ranking : **AI Score**")

else:

    results = smart_recommend_by_profile(
        goal=goal,
        meal_type=meal_type,
        diet_type=diet_type,
        cuisine=cuisine,
        df=df,
        top_n=top_n
    )
# ==========================================================
# Show AI Recommendations
# ==========================================================

if recommend_btn and not results.empty:

    st.divider()

    st.header("🥗 Recommended Foods")

    for _, row in results.iterrows():

        recommendation_card(row)

        with st.expander("📊 View Nutrition Details"):

            nutrition_metrics(row)

            health_progress(row["health_score"])

            ai_explanation(row)

        st.markdown("---")
# ==========================================================
# Charts
# ==========================================================

    if recommend_btn and not results.empty:

        st.header("📈 Nutrition Dashboard")

        c1, c2 = st.columns(2)

    with c1:
        st.plotly_chart(
            calories_chart(results),
            use_container_width=True
        )

    with c2:
        st.plotly_chart(
            protein_chart(results),
            use_container_width=True
        )

    c3, c4 = st.columns(2)

    with c3:
        st.plotly_chart(
            health_score_chart(results),
            use_container_width=True
        )

    with c4:
        st.plotly_chart(
            nutrition_pie(results.iloc[0]),
            use_container_width=True
        )

    st.plotly_chart(
        health_gauge(results.iloc[0]["health_score"]),
        use_container_width=True
    )