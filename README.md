# 🏠 Canadian House Price Predictor

A Machine Learning web application that predicts house prices across **45 Canadian cities** using real listing data. Built with Python, Scikit-learn, and Streamlit.

---

## 📸 App Preview

| Home | Predict | Insights |
|---|---|---|
| Stats & Overview | City, Beds, Baths, Income | Price trends & charts |

---

## 📁 Project Structure

```
Canadian-house-price-predictions/
│
├── data/
│   ├── raw/
│   │   └── HouseListings-Top45Cities.csv   ← original dataset
│   ├── cleaned/
│   │   └── Housing_cleaned.csv   ← after cleaning
│   └── processed/              
│   |   ├── housing_featured.csv                 ← after feature engineering
│   |   ├── province_map.csv                     ← province encoding map
│   └── train_test/              
│       ├── X_train.csv                          ← train features
│       ├── y_train.csv                          ← province train target
│       ├── X_test.csv                           ← test features
│       └── y_test.csv                           ← test target
│
├── models/
│   ├── model_features.pkl                       ← feature list
│   ├── province_map.pkl                         ← province encoding
│   └── model_comparison.csv                     ← all models comparison
│
├── notebooks/
│   ├── 1_cleaning.ipynb                         ← data cleaning
│   ├── 2_eda.ipynb                              ← exploratory data analysis
│   ├── 3_feature_engineering.ipynb              ← feature engineering
│   └── 4_train_model.ipynb                      ← training, comparison & testing
│   └── 4_test_model.ipynb                       ← testing model
│
├── plots/                                       ← all saved plots
│
├── app/
│   ├── main.py                                  ← home page
│   ├── pages/
│   │   ├── 1_predict.py                         ← prediction page
│   │   ├── 2_insights.py                        ← city insights page
│   │   └── 3_about.py                           ← about page
│   └── utils/
│       └── helper.py                            ← shared functions
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📊 Dataset

- **Source:** Canadian House Listings — Top 45 Cities
- **Total rows:** ~27,000 listings
- **Cities:** 45 Canadian cities
- **Provinces:** Alberta, British Columbia, Ontario, Quebec, and more

| Column | Description |
|---|---|
| `City` | Canadian city name |
| `Province` | Canadian province |
| `Price` | House listing price ($) |
| `Number_Beds` | Number of bedrooms |
| `Number_Baths` | Number of bathrooms |
| `Latitude` | Geographic latitude |
| `Longitude` | Geographic longitude |
| `Population` | City population |
| `Median_Family_Income` | Median family income in city |

---

## ⚙️ Features Used in Model

| Feature | Type | Description |
|---|---|---|
| `Number_Beds` | Raw | Number of bedrooms |
| `Number_Baths` | Raw | Number of bathrooms |
| `Latitude` | Raw | City latitude |
| `Longitude` | Raw | City longitude |
| `Bath_Bed_Ratio` | Engineered | Baths / (Beds + 1) |
| `Log_Income` | Engineered | log1p(Median Income) |
| `Log_Population` | Engineered | log1p(Population) |
| `Province_Code` | Encoded | Province → number |
| `City_Encoded` | Encoded | City → median log price |
| `City_Price_Std` | Encoded | City price volatility |
| `City_Price_Rank` | Encoded | Price rank within city |

---

## 🤖 Models Trained & Compared

| Model | CV R² |
|---|---|
| Gradient Boosting | 0.6696 ✅ Best |
| Random Forest | 0.6598 |
| XGBoost | 0.6633 |
| Decision Tree | 0.6494 |
| AdaBoost | 0.5855 |
| Ridge Regression | 0.6146 |
| Lasso Regression | 0.4423 |
| Linear Regression | 0.6156 |

---

## 🏆 Best Model

| Detail | Value |
|---|---|
| **Algorithm** | Gradient Boosting Regressor |
| **Target** | Log Price → converted back to $ |
| **CV R²** | ~0.67 |
| **MAPE** | ~30% |
| **Train / Test Split** | 80% / 20% |
| **Format** | ONNX (cross-platform) |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/mrhamxo/Canadian-house-price-predictions.git
cd Canadian-house-price-predictions
```

### 2. Create virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```cmd
pip install -r requirements.txt
```

### 4. Launch Streamlit app

```cmd
streamlit run app/main.py
```

---

## 📦 Requirements

Install all dependencies:
```cmd
pip install -r requirements.txt
```

---

## 🖥️ App Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Overview, stats, navigation |
| 🔮 **Predict** | Enter city, beds, baths, income → get price estimate |
| 📊 **Insights** | Price trends, city explorer, province comparison |
| ℹ️ **About** | Model info, features, how prediction works |

---

## 📈 How Prediction Works

```
User enters → City, Beds, Baths, Income
                      ↓
App auto-fills → Lat, Lon, Population, Province from city
                      ↓
App calculates → Bath_Bed_Ratio, Log_Income, City_Encoded...
                      ↓
Model predicts → Log Price
                      ↓
App converts → Real Price using expm1()
                      ↓
Result shown → Predicted Price ± 10% range
```

---

## ⚠️ Disclaimer

Predictions are based on historical listing data and are estimates only.
Actual house prices depend on many additional factors such as property
condition, exact location, market trends, and more.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@hamza](https://github.com/mrhamxo)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/muhammad-hamza-khattak)