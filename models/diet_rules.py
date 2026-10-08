import re

NON_VEG_WORDS = [
    "chicken", "beef", "pork", "turkey", "veal", "lamb", "mutton", "goat", "ham", "bacon",
    "meat", "meatball", "meatballs", "sausage", "sausages", "salami", "pepperoni", "pastrami",
    "prosciutto", "chorizo", "bologna", "frankfurter", "hotdog", "jerky", "steak", "ribs",
    "tenderloin", "sirloin", "brisket", "burger", "hamburger", "cheeseburger", "nuggets",
    "wings", "drumstick", "duck", "goose", "ostrich", "emu", "quail", "pheasant", "rabbit",
    "venison", "bison", "buffalo", "elk", "liver", "heart", "kidney", "tongue", "tripe",
    "gizzard", "spleen", "splean", "pancreas", "brain", "lard", "tallow", "suet", "gelatin",
    "fish", "salmon", "tuna", "cod", "halibut", "pollock", "tilefish", "trout", "mackerel",
    "herring", "tilapia", "catfish", "haddock", "snapper", "sardine", "sardines", "anchovy",
    "anchovies", "roe", "caviar", "shrimp", "prawn", "prawns", "crab", "lobster", "oyster",
    "oysters", "clam", "clams", "mussel", "mussels", "scallop", "scallops", "squid", "octopus",
    "surimi", "egg", "eggs", "omelet", "omelette", "carne", "cerdo", "chuck", "caribou",
    "moose", "reindeer", "boar", "sucker", "pike", "burbot", "carp", "whiting", "shad",
    "mullet", "lingcod", "ling", "cisco", "pompano", "seatrout", "flounder", "drum",
    "croaker", "scup", "sheepshead", "bass", "pout", "turbot", "sturgeon", "cusk", "eel",
    "yellowtail", "grouper", "swordfish", "sole", "hake", "abalone", "whelk", "conch",
    "big mac", "quarter pounder", "big n tasty", "cold cuts",
]

DAIRY_WORDS = [
    "cheese", "milk", "yogurt", "yoghurt", "cream", "butter", "buttermilk", "ghee", "paneer",
    "curd", "whey", "kefir", "custard", "pudding", "icecream", "latte", "cappuccino",
    "requeijao", "ricotta", "mozzarella", "parmesan", "cheddar", "feta", "honey", "queso",
    "gratin", "lasagna", "proteiinirahka",
]

PLANT_EXCEPTIONS = [
    "peanut butter", "almond butter", "cashew butter", "nut butter", "apple butter",
    "cocoa butter", "seed butter", "cream of tartar", "coconut milk", "almond milk",
    "soy milk", "soymilk", "oat milk", "rice milk", "coconut cream", "butternut",
]


def _contains_any(text, words):
    pattern = r"\b(" + "|".join(re.escape(w) for w in words) + r")\b"
    return bool(re.search(pattern, text))


def classify_diet(name, ingredients, allergens, original=""):
    """
    Decide the diet type of a food from its name, ingredients and allergens.
    """

    if str(original).lower() == "non-veg":
        return "non-veg"

    text = f"{name} {ingredients}".lower()

    for phrase in PLANT_EXCEPTIONS:
        text = text.replace(phrase, " ")

    allergens = str(allergens).lower()

    if _contains_any(text, NON_VEG_WORDS) or "eggs" in allergens or "seafood" in allergens:
        return "non-veg"

    if _contains_any(text, DAIRY_WORDS) or "milk" in allergens:
        return "veg"

    return "vegan"


def fix_diet_type(df):
    """
    Relabel the diet_type column using keyword rules.
    """

    old = df["diet_type"].str.lower()

    df["diet_type"] = [
        classify_diet(name, ingredients, allergens, original)
        for name, ingredients, allergens, original in zip(
            df["food_name"].fillna(""),
            df["ingredients"].fillna(""),
            df["allergens"].fillna(""),
            df["diet_type"].fillna(""),
        )
    ]

    changed = (old != df["diet_type"]).sum()

    print(f"✅ Diet type corrected for {changed} foods")

    return df