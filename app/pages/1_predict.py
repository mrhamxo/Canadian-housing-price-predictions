import streamlit as st
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import predict_price, get_cities, get_city_stats

st.set_page_config(
    page_title="Predict Price",
    page_icon="🔮",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────
st.markdown("""
    <style>
    .result-box {
        background: linear-gradient(135deg, #1f4e79, #2e75b6);
        color: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .result-price { font-size: 3rem; font-weight: 800; margin: 0.5rem 0; }
    .result-label { font-size: 1rem; opacity: 0.85; }
    .range-box    { background: #f0f4ff; border-radius: 12px; padding: 1rem; text-align: center; }
    .range-value  { font-size: 1.4rem; font-weight: 700; color: #1f4e79; }
    .range-label  { font-size: 0.85rem; color: #666; }
    </style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────
st.title("🔮 Predict House Price")
st.markdown("Fill in the details below to get an instant price estimate.")
st.divider()

# ── Load cities ───────────────────────────────────────────
try:
    cities = get_cities()
except Exception as e:
    st.error(f"❌ Could not load cities: {e}")
    st.stop()

# ── Input Form ────────────────────────────────────────────
with st.form("predict_form"):
    st.subheader("📍 Location")
    city = st.selectbox("City", cities)

    st.subheader("🏡 Property Details")
    col1, col2 = st.columns(2)
    beds  = col1.slider("🛏 Bedrooms",  min_value=0, max_value=10, value=3)
    baths = col2.slider("🚿 Bathrooms", min_value=1, max_value=8,  value=2)

    st.subheader("💵 Financial Info")
    income = st.number_input(
        "Median Family Income ($)",
        min_value=20_000, max_value=500_000,
        value=97_000, step=1_000,
    )

    submitted = st.form_submit_button(
        "💰 Predict Price",
        use_container_width=True,
        type="primary",
    )

# ── Result ────────────────────────────────────────────────
if submitted:
    try:
        with st.spinner("Calculating price..."):
            price = predict_price(city, beds, baths, income)
            low   = price * 0.90
            high  = price * 1.10

        # Validate result
        if price <= 0 or np.isnan(price) or np.isinf(price):
            st.error("❌ Prediction failed — invalid result. Please try different inputs.")
            st.stop()

        # Main result
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Estimated House Price</div>
                <div class="result-price">${price:,.0f}</div>
                <div class="result-label">
                    📍 {city} &nbsp;|&nbsp; 🛏 {beds} bed &nbsp;|&nbsp;
                    🚿 {baths} bath &nbsp;|&nbsp; 💵 ${income:,}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Range
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"""
                <div class="range-box">
                    <div class="range-label">Low Estimate (−10%)</div>
                    <div class="range-value">${low:,.0f}</div>
                </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
                <div class="range-box">
                    <div class="range-label">High Estimate (+10%)</div>
                    <div class="range-value">${high:,.0f}</div>
                </div>""", unsafe_allow_html=True)

        # City stats
        st.markdown("<br>", unsafe_allow_html=True)
        try:
            stats = get_city_stats(city)
            if stats:
                st.subheader(f"📊 {city} Market Stats")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Min Price",    f"${stats['min']:,.0f}")
                c2.metric("Median Price", f"${stats['median']:,.0f}")
                c3.metric("Avg Price",    f"${stats['mean']:,.0f}")
                c4.metric("Max Price",    f"${stats['max']:,.0f}")
        except Exception:
            pass  # stats are optional — don't crash if they fail

        st.caption("⚠️ Predictions are estimates based on historical data. Actual prices may vary.")

    except Exception as e:
        st.error(f"❌ Prediction error: {e}")