import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ==========================================================
# Calories Chart
# ==========================================================

def calories_chart(df):

    fig = px.bar(
        df,
        x="food_name",
        y="calories",
        color="calories",
        color_continuous_scale="Greens",
        title="🔥 Calories Comparison"
    )

    fig.update_layout(
        height=400,
        xaxis_title="Food",
        yaxis_title="Calories",
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


# ==========================================================
# Protein Chart
# ==========================================================

def protein_chart(df):

    fig = px.bar(
        df,
        x="food_name",
        y="protein_g",
        color="protein_g",
        color_continuous_scale="Blues",
        title="💪 Protein Comparison"
    )

    fig.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


# ==========================================================
# Health Score Chart
# ==========================================================

def health_score_chart(df):

    fig = px.bar(
        df,
        x="food_name",
        y="health_score",
        color="health_score",
        color_continuous_scale="Viridis",
        title="❤️ Health Score"
    )

    fig.update_layout(
        height=400,
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


# ==========================================================
# Macronutrients Pie Chart
# ==========================================================

def nutrition_pie(food):

    labels = [
        "Protein",
        "Carbs",
        "Fat"
    ]

    values = [
        food["protein_g"],
        food["carbs_g"],
        food["fat_g"]
    ]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55
            )
        ]
    )

    fig.update_layout(
        title="🥗 Macronutrient Distribution",
        template="plotly_dark",
        height=420
    )

    return fig


# ==========================================================
# Health Gauge
# ==========================================================

def health_gauge(score):

    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=score,

            title={"text": "Health Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#22C55E"},

                "steps": [

                    {"range": [0, 40], "color": "#EF4444"},

                    {"range": [40, 70], "color": "#FACC15"},

                    {"range": [70, 100], "color": "#22C55E"}

                ]

            }

        )

    )

    fig.update_layout(

        template="plotly_dark",

        height=350

    )

    return fig


# ==========================================================
# Dashboard Charts
# ==========================================================

def dashboard(df):

    return {

        "calories": calories_chart(df),

        "protein": protein_chart(df),

        "health": health_score_chart(df)

    }