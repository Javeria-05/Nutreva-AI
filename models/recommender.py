import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.preprocess import (
    load_dataset,
    preprocess_dataset
)


# ==========================================================
# Goal-Based Scoring
# ==========================================================

GOAL_WEIGHTS = {
    "weight loss": {"match_score": 0.70, "health_score": 0.30},
    "maintain weight": {"match_score": 0.70, "health_score": 0.30},
    "muscle gain": {"match_score": 0.60, "health_score": 0.10, "protein_g": 0.30},
    "weight gain": {"match_score": 0.60, "health_score": 0.10, "calories": 0.20, "protein_g": 0.10},
}

DEFAULT_WEIGHTS = {"match_score": 0.70, "health_score": 0.30}

TEXT_COLUMNS = [
    "food_name",
    "description",
    "cuisine",
    "meal_type",
    "diet_type",
    "health_goal",
    "ingredients",
    "recommendation_tags"
]


# ==========================================================
# Load & Prepare Dataset
# ==========================================================

def prepare_dataset():
    """
    Load and preprocess the Nutreva dataset.
    """

    df = load_dataset()
    df = preprocess_dataset(df)
    df = create_combined_features(df)

    return df


# ==========================================================
# Create Combined Features
# ==========================================================

def create_combined_features(df):
    """
    Combine important text columns into a single feature.
    """

    print("\n" + "=" * 60)
    print("🧠 CREATING COMBINED FEATURES")
    print("=" * 60)

    df = df.fillna("")

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype(str)

    df["combined_features"] = df[TEXT_COLUMNS].agg(" ".join, axis=1)

    print("✅ Combined Features Created")

    return df


# ==========================================================
# TF-IDF
# ==========================================================

def create_tfidf_matrix(df):
    """
    Create TF-IDF matrix.
    """

    print("\n" + "=" * 60)
    print("🤖 TF-IDF VECTORIZATION")
    print("=" * 60)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(df["combined_features"])

    print("✅ TF-IDF Matrix Created")
    print(f"📊 Matrix Shape : {tfidf_matrix.shape}")

    return vectorizer, tfidf_matrix


# ==========================================================
# Cosine Similarity
# ==========================================================

def create_similarity_matrix(tfidf_matrix):
    """
    Create cosine similarity matrix.
    """

    print("\n" + "=" * 60)
    print("🤖 CREATING COSINE SIMILARITY MATRIX")
    print("=" * 60)

    similarity_matrix = cosine_similarity(tfidf_matrix)

    print("✅ Similarity Matrix Created")
    print(f"📊 Matrix Shape : {similarity_matrix.shape}")

    return similarity_matrix


# ==========================================================
# Goal-Based AI Score
# ==========================================================

def compute_ai_score(df, goal):
    """
    Combine similarity and nutrition into one score based on the user's goal.
    """

    weights = GOAL_WEIGHTS.get(str(goal).lower(), DEFAULT_WEIGHTS)

    ai_score = pd.Series(0.0, index=df.index)

    for column, weight in weights.items():

        if column not in df.columns:
            continue

        if column in ("match_score", "health_score"):
            values = df[column]
        else:
            values = df[column].rank(pct=True) * 100

        ai_score += values * weight

    return ai_score


# ==========================================================
# Food-to-Food Recommendation
# ==========================================================

def recommend_food(food_name, df, similarity_matrix, top_n=5):
    """
    Recommend similar foods based on food name.
    """

    matches = df[df["food_name"].str.lower() == food_name.lower()]

    if matches.empty:
        return pd.DataFrame()

    index = matches.index[0]

    similarity_scores = list(enumerate(similarity_matrix[index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for food_index, score in similarity_scores[1:top_n + 1]:
        row = df.iloc[food_index].copy()
        row["match_score"] = round(score * 100, 2)
        recommendations.append(row)

    return pd.DataFrame(recommendations)


# ==========================================================
# User Profile Recommendation
# ==========================================================

def recommend_by_profile(
    goal,
    meal_type,
    diet_type,
    cuisine,
    df,
    vectorizer,
    tfidf_matrix,
    top_n=5
):
    """
    Recommend foods based on user profile.
    """

    query = f"{goal} {meal_type} {diet_type} {cuisine}".lower()

    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    recommendation_df = df.copy()
    recommendation_df["match_score"] = similarity_scores * 100

    recommendation_df = recommendation_df.sort_values(by="match_score", ascending=False)

    return recommendation_df.head(top_n).reset_index(drop=True)


# ==========================================================
# Smart Profile Recommendation
# ==========================================================

def apply_filter(df, column, value):
    """
    Filter by a column value, keep the previous data if nothing matches.
    """

    if not value:
        return df

    filtered = df[df[column].str.lower() == value.lower()]

    return filtered if not filtered.empty else df


def smart_recommend_by_profile(
    goal,
    meal_type,
    diet_type,
    cuisine,
    df,
    top_n=5
):
    """
    Smart AI recommendation with filtering.
    Returns a DataFrame for Streamlit.
    """

    filtered = df.copy()

    filtered = apply_filter(filtered, "health_goal", goal)
    filtered = apply_filter(filtered, "diet_type", diet_type)
    filtered = apply_filter(filtered, "meal_type", meal_type)
    filtered = apply_filter(filtered, "cuisine", cuisine)

    if filtered.empty:
        filtered = df.copy()

    filtered = create_combined_features(filtered.copy())

    vectorizer, tfidf_matrix = create_tfidf_matrix(filtered)

    query = f"{goal} {meal_type} {diet_type} {cuisine}".lower()

    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    result = filtered.copy()
    result["match_score"] = similarity_scores * 100
    result["ai_score"] = compute_ai_score(result, goal)

    result = result.sort_values(by="ai_score", ascending=False)

    return result.head(top_n).reset_index(drop=True)


# ==========================================================
# Helper Function
# ==========================================================

def build_ai_engine():
    """
    Prepare everything once.
    """

    df = prepare_dataset()

    vectorizer, tfidf_matrix = create_tfidf_matrix(df)

    similarity_matrix = create_similarity_matrix(tfidf_matrix)

    return (
        df,
        vectorizer,
        tfidf_matrix,
        similarity_matrix
    )


# ==========================================================
# Main (Testing)
# ==========================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("🥗 NUTREVA AI RECOMMENDATION ENGINE")
    print("=" * 70)

    df, vectorizer, tfidf_matrix, similarity_matrix = build_ai_engine()

    print(f"\n🍽 Total Foods : {len(df)}")

    print("\n" + "=" * 70)
    print("🍔 FOOD TO FOOD RECOMMENDATION")
    print("=" * 70)

    food_results = recommend_food(
        food_name="cream cheese",
        df=df,
        similarity_matrix=similarity_matrix,
        top_n=5
    )

    if not food_results.empty:
        for i, (_, row) in enumerate(food_results.iterrows(), start=1):
            print(f"{i}. {row['food_name']} ({row['match_score']:.1f}%)")

    print("\n" + "=" * 70)
    print("🥗 USER PROFILE RECOMMENDATION")
    print("=" * 70)

    profile_results = recommend_by_profile(
        goal="Weight Loss",
        meal_type="Lunch",
        diet_type="Veg",
        cuisine="Pakistani",
        df=df,
        vectorizer=vectorizer,
        tfidf_matrix=tfidf_matrix,
        top_n=5
    )

    for i, (_, row) in enumerate(profile_results.iterrows(), start=1):
        print(f"{i}. {row['food_name']} | AI Match: {row['match_score']:.1f}%")

    print("\n" + "=" * 70)
    print("🤖 SMART AI RECOMMENDATION (GOAL-BASED)")
    print("=" * 70)

    for test_goal in ["Weight Loss", "Muscle Gain", "Weight Gain"]:

        smart_results = smart_recommend_by_profile(
            goal=test_goal,
            meal_type="Lunch",
            diet_type="Non-Veg",
            cuisine="Continental",
            df=df,
            top_n=5
        )

        print(f"\n🎯 {test_goal}")
        print(smart_results[
            ["food_name", "ai_score", "health_score", "calories", "protein_g"]
        ].round(1).to_string(index=False))

    print("\n" + "=" * 70)
    print("✅ Nutreva AI Engine Ready for Streamlit")
    print("=" * 70)