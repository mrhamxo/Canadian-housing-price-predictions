import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data

st.set_page_config(page_title="About", page_icon="ℹ️", layout="centered")

st.title("ℹ️ About This App")
st.divider()

# ── Project Overview ──────────────────────────────────────
st.subheader("📌 Project Overview")
st.markdown("""
This app predicts **Canadian house prices** using a Machine Learning model
trained on real listing data from **45 Canadian cities**.

Simply enter a city, number of bedrooms, bathrooms, and median family income —
and the app will give you an **instant price estimate**.
""")

# ── Dataset Info ──────────────────────────────────────────
st.divider()
st.subheader("📁 Dataset")

try:
    df     = load_data()
    n_rows = len(df)
    n_city = df["City"].nunique()
    n_cols = df.shape[1]
except Exception:
    n_rows, n_city, n_cols = "N/A", "N/A", "N/A"

c1, c2, c3 = st.columns(3)
c1.metric("Total Rows",    f"{n_rows:,}" if isinstance(n_rows, int) else n_rows)
c2.metric("Total Cities",  n_city)
c3.metric("Total Columns", n_cols)

st.markdown("""
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
| `Median_Family_Income` | Median income in the city |
""")

# ── Model Info ────────────────────────────────────────────
st.divider()
st.subheader("🤖 Model")
st.markdown("""
| Detail | Value |
|---|---|
| **Algorithm** | Gradient Boosting Regressor |
| **Target** | Log Price → converted back to $ |
| **CV R²** | ~0.67 |
| **MAPE** | ~30% |
| **Train / Test Split** | 80% / 20% |
| **Total Features** | 11 |
""")

# ── Features ──────────────────────────────────────────────
st.divider()
st.subheader("⚙️ Features Used in Model")
st.markdown("""
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
""")

# ── How it works ──────────────────────────────────────────
st.divider()
st.subheader("⚡ How Prediction Works")
st.markdown("""
1. User enters **City, Beds, Baths, Income**
2. App auto-fills **Lat, Lon, Population, Province** from city lookup
3. App calculates **engineered features** behind the scenes
4. **Model predicts** Log Price
5. Log Price converted back to **real dollars** using `expm1()`
6. A **±10% range** is shown as low / high estimate
""")

# ── Disclaimer ────────────────────────────────────────────
st.divider()
st.warning("""
⚠️ **Disclaimer:** Predictions are based on historical listing data and are
estimates only. Actual house prices depend on many additional factors such as
property condition, exact location, market trends, and more.
""")