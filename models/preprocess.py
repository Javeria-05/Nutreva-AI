import pandas as pd


# ==========================================================
# Load Dataset
# ==========================================================
def load_dataset():
    """
    Load the Nutreva dataset.
    """
    df = pd.read_csv("dataset/Nutreva.csv")
    return df


# ==========================================================
# Dataset Validation
# ==========================================================
def validate_dataset(df):
    """
    Perform basic validation checks.
    """

    print("\n" + "=" * 60)
    print("📋 DATASET VALIDATION REPORT")
    print("=" * 60)

    # Missing Values
    print("\n🔍 Missing Values:")
    print(df.isnull().sum())

    # Duplicate Rows
    print(f"\n🗂 Duplicate Rows: {df.duplicated().sum()}")

    # Dataset Shape
    print("\n📊 Dataset Shape:")
    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    # Data Types
    print("\n📝 Data Types:")
    print(df.dtypes)

    # Statistics
    print("\n📈 Numerical Summary:")
    print(df.describe())


# ==========================================================
# AI Preprocessing
# ==========================================================
def preprocess_dataset(df):
    """
    Clean and prepare dataset for AI recommendation.
    """

    print("\n" + "=" * 60)
    print("🤖 AI PREPROCESSING")
    print("=" * 60)

    # Columns required for AI
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

    # Fill Missing Values
    for column in text_columns:
        df[column] = df[column].fillna("")

    # Convert to lowercase
    for column in text_columns:
        df[column] = df[column].astype(str).str.lower()

    # Remove extra spaces
    for column in text_columns:
        df[column] = (
            df[column]
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    print("✅ Missing values handled")
    print("✅ Converted text to lowercase")
    print("✅ Removed extra spaces")

    return df


# ==========================================================
# Main Function
# ==========================================================
if __name__ == "__main__":

    # Load Dataset
    df = load_dataset()

    print("✅ Dataset Loaded Successfully!")

    # Basic Information
    print(f"\n📊 Total Rows    : {df.shape[0]}")
    print(f"📋 Total Columns : {df.shape[1]}")

    # Column Names
    print("\n📌 Columns:")
    print(df.columns.tolist())

    # First Five Rows
    print("\n🍽 First 5 Rows:")
    print(df.head())

    # Validation
    validate_dataset(df)

    # AI Preprocessing
    df = preprocess_dataset(df)

    # Show Result
    print("\n🍽 Preprocessed Dataset:")
    print(df.head())