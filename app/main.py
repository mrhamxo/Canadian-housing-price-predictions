import streamlit as st
import sys, os
sys.path.append(os.path.dirname(__file__))
from utils.helper import load_data, get_cities

# ── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="🏠 Canadian House Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #1f4e79;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .card {
        background: linear-gradient(135deg, #f0f4ff, #ffffff);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1rem;
    }
    .card-icon  { font-size: 2.5rem; }
    .card-title { font-size: 1.2rem; font-weight: 700; color: #1f4e79; margin-top: 0.5rem; }
    .card-desc  { font-size: 0.95rem; color: #666; }
    .stat-box   {
        background: #1f4e79;
        color: white;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 800; }
    .stat-label  { font-size: 0.9rem; opacity: 0.85; }
    </style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────
st.markdown('<div class="main-title">🏠 Canadian House Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Predict house prices across 45 Canadian cities using Machine Learning</div>', unsafe_allow_html=True)
st.divider()

# ── Stats ─────────────────────────────────────────────────
try:
    df     = load_data()
    n_rows = len(df)
    n_city = df["City"].nunique()
except Exception:
    n_rows = 27000
    n_city = 45

c1, c2, c3, c4 = st.columns(4)
for col, number, label in zip(
    [c1, c2, c3, c4],
    [n_city, f"{n_rows:,}", "67%", "~30%"],
    ["Canadian Cities", "Houses Trained", "CV Accuracy (R²)", "Avg Error (MAPE)"],
):
    col.markdown(f"""
        <div class="stat-box">
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Feature Cards ─────────────────────────────────────────
st.subheader("What can you do?")
col1, col2, col3 = st.columns(3)
for col, icon, title, desc in zip(
    [col1, col2, col3],
    ["🔮", "📊", "ℹ️"],
    ["Predict Price", "City Insights", "About"],
    [
        "Enter city, bedrooms, bathrooms and income to get an instant price estimate",
        "Explore price trends, distributions and comparisons across Canadian cities",
        "Learn about the model, dataset, features and how predictions are made",
    ],
):
    col.markdown(f"""
        <div class="card">
            <div class="card-icon">{icon}</div>
            <div class="card-title">{title}</div>
            <div class="card-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 Use the **sidebar** to navigate between pages")