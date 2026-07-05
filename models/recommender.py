import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from models.preprocess import (
    load_dataset,
    preprocess_dataset
)


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

    text_columns = [

        "food_name",

        "description",

        "cuisine",

        "meal_type",

        "diet_type",

        "health_goal",

        "ingredients",

        "recommendation_tags"

    ]

    for column in text_columns:

        df[column] = df[column].astype(str)

    df["combined_features"] = (

        df["food_name"]

        + " "

        + df["description"]

        + " "

        + df["cuisine"]

        + " "

        + df["meal_type"]

        + " "

        + df["diet_type"]

        + " "

        + df["health_goal"]

        + " "

        + df["ingredients"]

        + " "

        + df["recommendation_tags"]

    )

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

    vectorizer = TfidfVectorizer(

        stop_words="english"

    )

    tfidf_matrix = vectorizer.fit_transform(

        df["combined_features"]

    )

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

    similarity_matrix = cosine_similarity(

        tfidf_matrix

    )

    print("✅ Similarity Matrix Created")

    print(

        f"📊 Matrix Shape : {similarity_matrix.shape}"

    )

    return similarity_matrix
# ==========================================================
# Food-to-Food Recommendation
# ==========================================================

def recommend_food(food_name, df, similarity_matrix, top_n=5):
    """
    Recommend similar foods based on food name.
    """

    matches = df[
        df["food_name"].str.lower() == food_name.lower()
    ]

    if matches.empty:
        return pd.DataFrame()

    index = matches.index[0]

    similarity_scores = list(
        enumerate(similarity_matrix[index])
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

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

    query = (
        f"{goal} "
        f"{meal_type} "
        f"{diet_type} "
        f"{cuisine}"
    ).lower()

    query_vector = vectorizer.transform([query])

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    recommendation_df = df.copy()

    recommendation_df["match_score"] = (
        similarity_scores * 100
    )

    recommendation_df = recommendation_df.sort_values(
        by="match_score",
        ascending=False
    )

    return recommendation_df.head(top_n).reset_index(drop=True)
# ==========================================================
# Smart Profile Recommendation
# ==========================================================

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

    # ----------------------------
    # Goal Filter
    # ----------------------------
    if goal:

        temp = filtered[
            filtered["health_goal"].str.lower()
            == goal.lower()
        ]

        if not temp.empty:
            filtered = temp

    # ----------------------------
    # Diet Filter
    # ----------------------------
    if diet_type:

        temp = filtered[
            filtered["diet_type"].str.lower()
            == diet_type.lower()
        ]

        if not temp.empty:
            filtered = temp

    # ----------------------------
    # Meal Filter
    # ----------------------------
    if meal_type:

        temp = filtered[
            filtered["meal_type"].str.lower()
            == meal_type.lower()
        ]

        if not temp.empty:
            filtered = temp

    # ----------------------------
    # Cuisine Filter
    # ----------------------------
    if cuisine:

        temp = filtered[
            filtered["cuisine"].str.lower()
            == cuisine.lower()
        ]

        if not temp.empty:
            filtered = temp

    # ----------------------------
    # Fallback
    # ----------------------------
    if filtered.empty:

        filtered = df.copy()

    # ----------------------------
    # Create Features
    # ----------------------------
    filtered = create_combined_features(
        filtered.copy()
    )

    vectorizer, tfidf_matrix = create_tfidf_matrix(
        filtered
    )

    # ----------------------------
    # User Query
    # ----------------------------
    query = (
        f"{goal} "
        f"{meal_type} "
        f"{diet_type} "
        f"{cuisine}"
    ).lower()

    query_vector = vectorizer.transform(
        [query]
    )

    similarity_scores = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    # ----------------------------
    # Final Ranking
    # ----------------------------
    result = filtered.copy()

    result["match_score"] = (
        similarity_scores * 100
    )

    # Nutrition Bonus
    if "health_score" in result.columns:

        result["ai_score"] = (

            result["match_score"] * 0.70 +

            result["health_score"] * 0.30

        )

    else:

        result["ai_score"] = result["match_score"]

    result = result.sort_values(

        by="ai_score",

        ascending=False

    )

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

    similarity_matrix = create_similarity_matrix(
        tfidf_matrix
    )

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

    # -----------------------------------
    # Build AI Engine
    # -----------------------------------

    (
        df,
        vectorizer,
        tfidf_matrix,
        similarity_matrix
    ) = build_ai_engine()

    print(f"\n🍽 Total Foods : {len(df)}")

    # -----------------------------------
    # Food-to-Food Recommendation
    # -----------------------------------

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

            print(
                f"{i}. {row['food_name']} "
                f"({row['match_score']:.1f}%)"
            )

    # -----------------------------------
    # User Profile Recommendation
    # -----------------------------------

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

        print(
            f"{i}. {row['food_name']} | "
            f"AI Match: {row['match_score']:.1f}%"
        )

    # -----------------------------------
    # Smart Recommendation
    # -----------------------------------

    print("\n" + "=" * 70)
    print("🤖 SMART AI RECOMMENDATION")
    print("=" * 70)

    smart_results = smart_recommend_by_profile(
        goal="Weight Loss",
        meal_type="Lunch",
        diet_type="Veg",
        cuisine="Pakistani",
        df=df,
        top_n=5
    )

    print(smart_results[
        [
            "food_name",
            "match_score",
            "ai_score",
            "health_score",
            "calories",
            "protein_g"
        ]
    ])

    print("\n" + "=" * 70)
    print("✅ Nutreva AI Engine Ready for Streamlit")
    print("=" * 70)