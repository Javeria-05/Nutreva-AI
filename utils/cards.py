import streamlit as st


# ==========================================================
# Recommendation Card
# ==========================================================

def recommendation_card(food):

    # ---------- Safe Defaults ----------
    food_name = food.get("food_name", "Unknown Food")
    cuisine = food.get("cuisine", "-")
    meal = food.get("meal_type", "-")
    diet = food.get("diet_type", "-")
    goal = food.get("health_goal", "-")

    calories = food.get("calories", 0)
    protein = food.get("protein_g", 0)
    carbs = food.get("carbs_g", 0)
    fat = food.get("fat_g", 0)
    fiber = food.get("fiber_g", 0)

    score = food.get("health_score", 0)

    ai_match = food.get("match_score", 0)

    # ---------- Badge ----------
    if ai_match >= 90:
        badge = "🟢 Excellent Match"
    elif ai_match >= 75:
        badge = "🟡 Very Good Match"
    elif ai_match >= 60:
        badge = "🟠 Good Match"
    else:
        badge = "🔴 Average Match"

    # ---------- Card ----------
    st.markdown(
        f"""
<div class="food-card">

<div class="food-title">
🥗 {food_name.title()}
</div>

<div class="food-info">

<b>🤖 AI Match</b> : {ai_match:.1f}%<br>

<b>🎯 Goal</b> : {goal.title()}<br>

<b>🌍 Cuisine</b> : {cuisine.title()}<br>

<b>🍽 Meal</b> : {meal.title()}<br>

<b>🥦 Diet</b> : {diet.title()}<br>

<hr>

🔥 Calories : {calories} kcal<br>

💪 Protein : {protein} g<br>

🍚 Carbs : {carbs} g<br>

🥑 Fat : {fat} g<br>

🌾 Fiber : {fiber} g<br>

❤️ Health Score : {score}/100

<hr>

<h4>{badge}</h4>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Nutrition Metrics
# ==========================================================

def nutrition_metrics(food):

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🔥 Calories",
        f"{food.get('calories',0)} kcal"
    )

    c2.metric(
        "💪 Protein",
        f"{food.get('protein_g',0)} g"
    )

    c3.metric(
        "🍚 Carbs",
        f"{food.get('carbs_g',0)} g"
    )

    c4.metric(
        "🥑 Fat",
        f"{food.get('fat_g',0)} g"
    )


# ==========================================================
# Health Score Progress
# ==========================================================

def health_progress(score):

    st.write("### ❤️ Health Score")

    progress = max(0, min(score, 100)) / 100

    st.progress(progress)

    if score >= 90:
        st.success(f"Excellent ({score}/100)")
    elif score >= 75:
        st.info(f"Very Good ({score}/100)")
    elif score >= 60:
        st.warning(f"Average ({score}/100)")
    else:
        st.error(f"Needs Improvement ({score}/100)")


# ==========================================================
# AI Explanation
# ==========================================================

def ai_explanation(food):

    st.write("### 🤖 Why AI Recommended This")

    reasons = []

    if food.get("protein_g", 0) >= 20:
        reasons.append("💪 High Protein")

    if food.get("fiber_g", 0) >= 5:
        reasons.append("🌾 Rich in Fiber")

    if food.get("health_score", 0) >= 90:
        reasons.append("❤️ Excellent Health Score")

    if food.get("calories", 0) <= 250:
        reasons.append("🔥 Low Calories")

    if food.get("diet_type", "").lower() == "veg":
        reasons.append("🥦 Vegetarian Friendly")

    if not reasons:
        reasons.append("🤖 Best overall similarity match")

    for reason in reasons:
        st.success(reason)