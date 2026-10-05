<div align="center">

# 🥗 Nutreva AI
### AI-Powered Nutrition Recommendation System

An intelligent **Content-Based Food Recommendation System** built using **Python**, **Machine Learning**, **TF-IDF**, **Cosine Similarity**, and **Streamlit**.

---

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-TF--IDF-success)
![EDA](https://img.shields.io/badge/EDA-23%20Visualizations-orange)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

</div>

---

## 🔗 Live Demo

**[Try Nutreva AI live →](https://nutreva-ai-q5x6uoynp3s72buwdk4jps.streamlit.app/)**

---

# 📌 Project Overview

Nutreva AI is an intelligent nutrition recommendation system that suggests healthy foods based on user preferences.

Instead of using collaborative filtering, Nutreva uses a **Content-Based Recommendation Engine** powered by **TF-IDF** and **Cosine Similarity** to recommend foods that best match a user's profile.

Users can select:

- 🎯 Health Goal
- 🍽 Meal Type
- 🥦 Diet Type
- 🌍 Cuisine

The AI engine analyzes these preferences and recommends the most relevant foods from the dataset.

---

# ✨ Features

- 🤖 AI Powered Recommendation Engine
- 🥗 Content-Based Filtering
- 📊 TF-IDF Vectorization
- 📈 Cosine Similarity Matching
- 🎯 Smart Profile-Based Recommendations
- 🌍 Cuisine Filtering
- 🥦 Diet Type Filtering
- 🍽 Meal Type Filtering
- ❤️ Health Goal Matching
- 📊 Nutrition Dashboard
- 📉 Interactive Charts
- 🔍 Exploratory Data Analysis with 23 visualizations
- 🌙 Professional Streamlit UI

---

# 🧠 AI Workflow

```text
User Preferences
        │
        ▼
Data Preprocessing
        │
        ▼
Combined Features
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Cosine Similarity
        │
        ▼
Smart Filtering
        │
        ▼
Top AI Recommendations
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Pandas | Data Processing |
| Scikit-Learn | Machine Learning |
| TF-IDF | Feature Extraction |
| Cosine Similarity | Recommendation Engine |
| Streamlit | Web Application |
| Plotly | Interactive Charts |
| Matplotlib & Seaborn | Exploratory Data Analysis |

---

# 📂 Project Structure

```text
Nutreva
│
├── app.py
├── README.md
├── requirements.txt
│
├── dataset
│   └── Nutreva.csv
│
├── analysis
│   ├── eda.py
│   └── graphs/          # 23 generated visualizations
│
├── models
│   ├── preprocess.py
│   ├── recommender.py
│   └── similarity.py
│
├── utils
│   ├── styles.py
│   ├── cards.py
│   ├── charts.py
│   └── helper.py
│
├── pages
│   ├── About.py
│   ├── Home.py
│   └── Recommendation.py
│
└── assets
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Javeria-05/Nutreva-AI.git
```

Move into project folder

```bash
cd Nutreva-AI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Streamlit

```bash
python -m streamlit run app.py
```

---

# 🚀 How It Works

1. Load Dataset
2. Clean & Preprocess Data
3. Create Combined Features
4. TF-IDF Vectorization
5. Cosine Similarity Calculation
6. Smart User Profile Filtering
7. AI Recommendation Generation
8. Display Results in Streamlit Dashboard

---

# 📊 Dataset Information

- 🍽 Foods: **2396**
- 📋 Features: **20**
- 🤖 Recommendation Type: **Content-Based Filtering**
- 📈 AI Model: **TF-IDF + Cosine Similarity**

---

# 🔍 Exploratory Data Analysis

A full EDA was performed on the dataset to understand the relationships between nutritional values, health goals, diet types and recommendation tags.

**Data cleaning:** 74 invalid rows were removed before analysis (foods above 900 kcal per 100 g, which is physically impossible, and one corrupted row), leaving **2322 foods**.

Generate all 23 graphs:

```bash
python analysis/eda.py
```

### Correlation Between Nutritional Features
<img src="analysis/graphs/01_correlation_heatmap.png" width="600" />

### Calories vs Health Score
<img src="analysis/graphs/02_scatter_calories_vs_health_score.png" width="600" />

### Average Nutrients by Health Goal
<img src="analysis/graphs/11_health_goal_vs_nutrients.png" width="700" />

### Diet Type Share within Each Health Goal
<img src="analysis/graphs/15_health_goal_x_diet_type.png" width="700" />

### Recommendation Tags Frequency
<img src="analysis/graphs/21_tags_frequency.png" width="600" />

### Calories Distribution
<img src="analysis/graphs/23_calories_distribution.png" width="700" />

### Key Findings

- **Calories and Health Score** have a strong negative correlation (r = −0.60): higher-calorie foods receive lower health scores.
- **Fat** is the second biggest factor lowering the health score (r = −0.51).
- **Protein and Fat** are strongly linked (r = 0.69), mainly driven by meat-based foods.
- **Weight Gain** foods have the highest average calories, protein and fat, while **Weight Loss** foods are the lowest across all macronutrients.
- The calories distribution is **right-skewed**: most foods are low-calorie, while a small number of high-calorie foods pull the mean above the median.
- **Weight Loss** foods make up the largest share of the dataset, and **Heart Healthy** is the most common recommendation tag.

All 23 graphs are available in [`analysis/graphs`](analysis/graphs).

---

# 📸 Screenshots
<img width="1365" height="601" alt="image" src="https://github.com/user-attachments/assets/dc54bab3-a62e-4d79-a071-c432492305ea" />
<img width="1365" height="597" alt="image" src="https://github.com/user-attachments/assets/60c7ffc9-0161-4c45-a970-968e210bc3ab" />
<img width="1365" height="602" alt="image" src="https://github.com/user-attachments/assets/f86cf3a2-d28d-4cb4-ac91-a1be031cb590" />
<img width="1365" height="599" alt="image" src="https://github.com/user-attachments/assets/4b0f7ca8-3285-48d3-9951-5e0b0ef99457" />
<img width="1365" height="600" alt="image" src="https://github.com/user-attachments/assets/b1e4abb2-caac-4c82-9edf-cd662afaf1bf" />
<img width="1365" height="599" alt="image" src="https://github.com/user-attachments/assets/75d43c31-50cf-46be-a38f-c8bf8e064578" />
<img width="1365" height="598" alt="image" src="https://github.com/user-attachments/assets/b5284091-05b7-4065-ac20-2e6b2987f7c0" />

---

# 🚀 Future Improvements

- Food Images
- Nutrition Tracking
- User Login
- Meal Planner
- Favorite Foods
- AI Chatbot
- Barcode Scanner
- Mobile App Version

---

# 👩‍💻 Developer

**Javeria**

Software Engineering Student

AI & Machine Learning Enthusiast

---

# ⭐ Support

If you like this project, don't forget to ⭐ star this repository.