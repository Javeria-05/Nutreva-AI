DISPLAY_NAMES = {
    "health_goal": {
        "weight loss": "🔻 Weight Loss",
        "maintain weight": "⚖️ Maintain Weight",
        "muscle gain": "💪 Muscle Gain",
        "weight gain": "🔺 Weight Gain",
    },
    "meal_type": {
        "lunch": "🍛 Main Course",
        "dessert": "🍰 Dessert",
        "beverage": "🥤 Beverage",
    },
    "diet_type": {
        "non-veg": "🍗 Non-Vegetarian",
        "veg": "🥛 Vegetarian",
        "vegan": "🌱 Vegan",
    },
}

DESCRIPTIONS = {
    "health_goal": {
        "weight loss": "Low-calorie, light foods.",
        "maintain weight": "Balanced foods to keep your current weight.",
        "muscle gain": "High-protein foods to build muscle.",
        "weight gain": "High-calorie, energy-rich foods.",
    },
    "meal_type": {
        "lunch": "Lunch or dinner dishes.",
        "dessert": "Sweets and desserts.",
        "beverage": "Juices, tea, coffee and other drinks.",
    },
    "diet_type": {
        "non-veg": "Includes meat, chicken, fish and eggs.",
        "veg": "No meat, fish or eggs. Milk, cheese, yogurt and butter are allowed.",
        "vegan": "Nothing from animals. No meat, eggs, milk, cheese or honey. Only vegetables, fruits, grains, lentils and nuts.",
    },
}


def display_name(column, value):
    """
    Return a user-friendly name for a dataset value.
    """

    key = str(value).lower()

    return DISPLAY_NAMES.get(column, {}).get(key, str(value).title())


def describe(column, value):
    """
    Return a short explanation of a dataset value for the UI.
    """

    return DESCRIPTIONS.get(column, {}).get(str(value).lower(), "")


def ordered_options(df, column):
    """
    Return the column's values in a logical order for dropdowns.
    """

    available = set(df[column].dropna().str.lower().unique())

    preferred = [v for v in DISPLAY_NAMES.get(column, {}) if v in available]
    remaining = sorted(available - set(preferred))

    return preferred + remaining