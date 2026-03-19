import joblib
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import os

# ── Paths — relative to project root ─────────────────────
BASE_DIR      = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MODEL_PATH    = os.path.join(BASE_DIR, "models", "house_price_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "models", "model_features.pkl")
DATA_PATH     = os.path.join(BASE_DIR, "dataset", "processed", "housing_featured.csv")

# ── Load model ────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ Model file not found: {MODEL_PATH}")
        st.stop()
    if not os.path.exists(FEATURES_PATH):
        st.error(f"❌ Features file not found: {FEATURES_PATH}")
        st.stop()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    features = joblib.load(FEATURES_PATH)
    return model, features

# ── Load dataset ──────────────────────────────────────────
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ Data file not found: {DATA_PATH}")
        st.stop()
    df = pd.read_csv(DATA_PATH)

    # Make sure Price column exists in real dollars
    if "Price" not in df.columns and "Log_Price" in df.columns:
        df["Price"] = np.expm1(df["Log_Price"])

    return df

# ── Build city lookup maps ────────────────────────────────
@st.cache_data
def build_city_maps():
    df = load_data()
    return {
        "lat":          df.groupby("City")["Latitude"].first().to_dict(),
        "lon":          df.groupby("City")["Longitude"].first().to_dict(),
        "log_pop":      df.groupby("City")["Log_Population"].first().to_dict(),
        "province":     df.groupby("City")["Province_Code"].first().to_dict(),
        "price_median": df.groupby("City")["Log_Price"].median().to_dict(),
        "price_std":    df.groupby("City")["Log_Price"].std().to_dict(),
    }

# ── Get available cities ──────────────────────────────────
@st.cache_data
def get_cities():
    df = load_data()
    return sorted(df["City"].unique().tolist())

# ── Get city stats ────────────────────────────────────────
@st.cache_data
def get_city_stats(city):
    df = load_data()
    if "Price" not in df.columns:
        return {}
    subset = df[df["City"] == city]["Price"]
    if len(subset) == 0:
        return {}
    return {
        "min":    subset.min(),
        "max":    subset.max(),
        "median": subset.median(),
        "mean":   subset.mean(),
        "count":  len(subset),
    }

# ── Predict price ─────────────────────────────────────────
def predict_price(city, number_beds, number_baths, income):
    model, features = load_model()
    maps            = build_city_maps()

    # Validate city exists
    if city not in maps["lat"]:
        st.error(f"❌ City '{city}' not found in dataset.")
        st.stop()

    # Build features
    log_income      = np.log1p(income)
    log_pop         = maps["log_pop"].get(city, 0)
    latitude        = maps["lat"].get(city, 0)
    longitude       = maps["lon"].get(city, 0)
    province_code   = maps["province"].get(city, 0)
    bath_bed_ratio  = number_baths / (number_beds + 1)

    fallback_median = float(np.mean(list(maps["price_median"].values())))
    fallback_std    = float(np.mean(list(maps["price_std"].values())))

    city_encoded    = maps["price_median"].get(city, fallback_median)
    city_price_std  = maps["price_std"].get(city,    fallback_std)
    city_price_rank = 0.75

    input_dict = {
        "Number_Beds":     number_beds,
        "Number_Baths":    number_baths,
        "Latitude":        latitude,
        "Longitude":       longitude,
        "Bath_Bed_Ratio":  bath_bed_ratio,
        "Log_Income":      log_income,
        "Log_Population":  log_pop,
        "Province_Code":   province_code,
        "City_Encoded":    city_encoded,
        "City_Price_Std":  city_price_std,
        "City_Price_Rank": city_price_rank,
    }

    # Only keep features the model expects
    input_data = pd.DataFrame([input_dict])[features]

    log_pred = model.predict(input_data)[0]
    price    = float(np.expm1(log_pred))
    return price