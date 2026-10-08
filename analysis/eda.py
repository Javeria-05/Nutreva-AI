import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from models.diet_rules import fix_diet_type
from models.preprocess import load_dataset, remove_invalid_rows

OUT_DIR = Path(__file__).resolve().parent / "graphs"
OUT_DIR.mkdir(exist_ok=True)

NUMERIC_COLS = [
    "calories", "protein_g", "carbs_g", "fat_g",
    "fiber_g", "sugar_g", "sodium_mg", "health_score",
]

SCATTER_PAIRS = [
    ("calories", "health_score"),
    ("fat_g", "health_score"),
    ("calories", "protein_g"),
    ("calories", "carbs_g"),
    ("calories", "fat_g"),
    ("protein_g", "fat_g"),
    ("fiber_g", "sugar_g"),
    ("carbs_g", "fiber_g"),
    ("carbs_g", "sugar_g"),
]

DIET_LABELS = {"non-veg": "Non-Vegetarian", "veg": "Vegetarian", "vegan": "Vegan"}

GOAL_ORDER = ["Weight Loss", "Maintain Weight", "Muscle Gain", "Weight Gain"]
DIET_ORDER = ["Vegan", "Vegetarian", "Non-Vegetarian"]
MEAL_ORDER = ["Lunch", "Dessert", "Beverage"]

sns.set_theme(style="whitegrid")


def load_clean_data():
    df = load_dataset()
    df = remove_invalid_rows(df)
    df = fix_diet_type(df)
    df["diet_type"] = df["diet_type"].map(DIET_LABELS)
    return df


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT_DIR / f"{name}.png", dpi=150)
    plt.close(fig)
    print(f"Saved: {name}.png")


def label(col):
    units = {"_mg": " (mg)", "_g": " (g)"}
    for suffix, unit in units.items():
        if col.endswith(suffix):
            return col[: -len(suffix)].replace("_", " ").title() + unit
    return col.replace("_", " ").title()


def split_multi_value(df, col):
    out = df.dropna(subset=[col]).copy()
    out[col] = out[col].str.split(",")
    out = out.explode(col).reset_index(drop=True)
    out[col] = out[col].str.strip()
    return out


def correlation_heatmap(df):
    corr = df[NUMERIC_COLS].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn", center=0, ax=ax)
    ax.set_title("Correlation Between Nutritional Features")
    save(fig, "01_correlation_heatmap")


def scatter_plots(df):
    for i, (x, y) in enumerate(SCATTER_PAIRS, start=2):
        r = df[x].corr(df[y])
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.regplot(
            data=df, x=x, y=y, ax=ax,
            scatter_kws={"alpha": 0.35, "s": 18},
            line_kws={"color": "crimson"},
        )
        ax.set_xlabel(label(x))
        ax.set_ylabel(label(y))
        ax.set_title(f"{label(x)} vs {label(y)}  (r = {r:.2f})")
        save(fig, f"{i:02d}_scatter_{x}_vs_{y}")


def category_averages(df, category, cols, order, name, title):
    avg = df.groupby(category)[cols].mean().reindex(order).reset_index()
    long = avg.melt(id_vars=category, var_name="nutrient", value_name="average")
    long["nutrient"] = long["nutrient"].apply(label)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=long, x=category, y="average", hue="nutrient", ax=ax)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", fontsize=8, padding=2)
    ax.set_xlabel(label(category))
    ax.set_ylabel("Average per 100 g")
    ax.set_title(title)
    ax.legend(title="")
    save(fig, name)


def category_bar_charts(df):
    category_averages(
        df, "health_goal", ["calories", "protein_g", "carbs_g", "fat_g"],
        GOAL_ORDER, "11_health_goal_vs_nutrients",
        "Average Nutrients by Health Goal",
    )
    category_averages(
        df, "diet_type", ["calories", "protein_g", "fat_g"],
        DIET_ORDER, "12_diet_type_vs_nutrients",
        "Average Nutrients by Diet Type",
    )
    category_averages(
        df, "meal_type", ["calories", "sugar_g"],
        MEAL_ORDER, "13_meal_type_vs_nutrients",
        "Average Calories and Sugar by Meal Type",
    )


def health_score_boxplot(df):
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.boxplot(
        data=df, x="health_goal", y="health_score",
        order=GOAL_ORDER, hue="health_goal", palette="Set2", legend=False, ax=ax,
    )
    ax.set_xlabel("Health Goal")
    ax.set_ylabel("Health Score")
    ax.set_title("Health Score Distribution by Health Goal")
    save(fig, "14_health_goal_vs_health_score")


def stacked_percent(df, row, col, name, title, row_order=None, col_order=None):
    table = pd.crosstab(df[row], df[col], normalize="index") * 100
    if row_order:
        table = table.reindex(row_order)
    if col_order:
        table = table.reindex(columns=col_order)

    counts = df[row].value_counts()
    table.index = [f"{idx}\n(n={counts.get(idx, 0)})" for idx in table.index]

    fig, ax = plt.subplots(figsize=(10, 6))
    table.plot(kind="bar", stacked=True, colormap="Set2", ax=ax, width=0.7)
    for container in ax.containers:
        labels = [f"{v:.0f}%" if v >= 5 else "" for v in container.datavalues]
        ax.bar_label(container, labels=labels, label_type="center", fontsize=8)
    ax.set_xlabel(label(row))
    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 100)
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=0)
    ax.legend(title=label(col), bbox_to_anchor=(1.02, 1), loc="upper left")
    save(fig, name)


def category_cross_charts(df):
    stacked_percent(
        df, "health_goal", "diet_type", "15_health_goal_x_diet_type",
        "Diet Type Share within Each Health Goal",
        row_order=GOAL_ORDER, col_order=DIET_ORDER,
    )
    stacked_percent(
        df, "meal_type", "health_goal", "16_meal_type_x_health_goal",
        "Health Goal Share within Each Meal Type",
        row_order=MEAL_ORDER, col_order=GOAL_ORDER,
    )

    allergens = split_multi_value(df, "allergens")
    stacked_percent(
        allergens, "allergens", "diet_type", "17_allergens_x_diet_type",
        "Diet Type Share within Each Allergen",
        col_order=DIET_ORDER,
    )

    tags = split_multi_value(df, "recommendation_tags")
    stacked_percent(
        tags, "recommendation_tags", "health_goal", "18_tags_x_health_goal",
        "Health Goal Share within Each Recommendation Tag",
        col_order=GOAL_ORDER,
    )


def pie_chart(df, col, order, name, title):
    counts = df[col].value_counts().reindex(order)
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        counts, labels=[f"{k}\n({v})" for k, v in counts.items()],
        autopct="%1.1f%%", startangle=90,
        colors=sns.color_palette("Set2", len(counts)),
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    ax.set_title(title)
    save(fig, name)


def frequency_bar(df, col, name, title):
    counts = split_multi_value(df, col)[col].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(counts.index, counts.values, color=sns.color_palette("Set2", len(counts)))
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_xlabel("Number of Foods")
    ax.set_title(title)
    save(fig, name)


def calories_histogram(df):
    mean, median = df["calories"].mean(), df["calories"].median()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df["calories"], bins=40, kde=True, color="teal", ax=ax)
    ax.axvline(mean, color="crimson", linestyle="--", label=f"Mean = {mean:.0f}")
    ax.axvline(median, color="orange", linestyle="--", label=f"Median = {median:.0f}")
    ax.set_xlabel("Calories per 100 g")
    ax.set_ylabel("Number of Foods")
    ax.set_title("Calories Distribution")
    ax.legend()
    save(fig, "23_calories_distribution")


def distribution_charts(df):
    pie_chart(df, "health_goal", GOAL_ORDER, "19_health_goal_distribution",
              "Foods by Health Goal")
    pie_chart(df, "diet_type", DIET_ORDER, "20_diet_type_distribution",
              "Foods by Diet Type")
    frequency_bar(df, "recommendation_tags", "21_tags_frequency",
                  "Recommendation Tags Frequency")
    frequency_bar(df, "allergens", "22_allergens_frequency",
                  "Allergens Frequency")
    calories_histogram(df)


if __name__ == "__main__":
    data = load_clean_data()
    correlation_heatmap(data)
    scatter_plots(data)
    category_bar_charts(data)
    health_score_boxplot(data)
    category_cross_charts(data)
    distribution_charts(data)