import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.helper import load_data

st.set_page_config(page_title="City Insights", page_icon="📊", layout="wide")
sns.set_theme(style="whitegrid")

st.title("📊 City Insights")
st.markdown("Explore house price trends across Canadian cities.")
st.divider()

# ── Load data ─────────────────────────────────────────────
try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Could not load data: {e}")
    st.stop()

# Ensure Price column exists
if "Price" not in df.columns:
    if "Log_Price" in df.columns:
        df["Price"] = np.expm1(df["Log_Price"])
    else:
        st.error("❌ Price column not found in dataset.")
        st.stop()

# Ensure Province column exists
if "Province" not in df.columns:
    st.warning("⚠️ Province column not found — skipping province chart.")
    has_province = False
else:
    has_province = True

# ── Section 1: City Price Comparison ─────────────────────
st.subheader("🏙️ Median Price by City")
try:
    city_median = df.groupby("City")["Price"].median().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(14, 6))
    colors  = ["#1f4e79" if i < 5 else "#2e75b6" if i < 15 else "#9dc3e6"
               for i in range(len(city_median))]
    ax.bar(city_median.index, city_median.values, color=colors)
    ax.set_title("Median House Price by City", fontsize=14, fontweight="bold")
    ax.set_xlabel("City")
    ax.set_ylabel("Median Price ($)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
except Exception as e:
    st.error(f"❌ Could not render city chart: {e}")

# ── Section 2: Filter by City ─────────────────────────────
st.divider()
st.subheader("🔍 Explore a Specific City")

try:
    cities   = sorted(df["City"].unique().tolist())
    sel_city = st.selectbox("Select City", cities)
    city_df  = df[df["City"] == sel_city]

    if len(city_df) == 0:
        st.warning(f"No data found for {sel_city}")
    else:
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Listings", f"{len(city_df):,}")
        c2.metric("Min Price",      f"${city_df['Price'].min():,.0f}")
        c3.metric("Median Price",   f"${city_df['Price'].median():,.0f}")
        c4.metric("Avg Price",      f"${city_df['Price'].mean():,.0f}")
        c5.metric("Max Price",      f"${city_df['Price'].max():,.0f}")

        fig2, axes = plt.subplots(1, 2, figsize=(14, 4))
        sns.histplot(city_df["Price"], kde=True, ax=axes[0], color="#1f4e79", bins=40)
        axes[0].set_title(f"Price Distribution — {sel_city}")
        axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

        if "Number_Beds" in city_df.columns:
            sns.boxplot(x="Number_Beds", y="Price", data=city_df,
                        ax=axes[1], palette="Blues")
            axes[1].set_title(f"Price by Bedrooms — {sel_city}")
            axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
except Exception as e:
    st.error(f"❌ City explorer error: {e}")

# ── Section 3: Province Comparison ───────────────────────
if has_province:
    st.divider()
    st.subheader("🗺️ Price by Province")
    try:
        fig3, ax3 = plt.subplots(figsize=(12, 5))
        order = df.groupby("Province")["Price"].median().sort_values(ascending=False).index
        sns.boxplot(x="Province", y="Price", data=df,
                    order=order, palette="Blues", ax=ax3)
        ax3.set_title("House Price by Province")
        ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
    except Exception as e:
        st.error(f"❌ Province chart error: {e}")

# ── Section 4: Beds & Baths vs Price ─────────────────────
st.divider()
st.subheader("🛏 Bedrooms & Bathrooms vs Price")
try:
    fig4, axes4 = plt.subplots(1, 2, figsize=(14, 5))

    if "Number_Beds" in df.columns:
        sns.boxplot(x="Number_Beds", y="Price", data=df, ax=axes4[0], palette="Blues")
        axes4[0].set_title("Price by Bedrooms")
        axes4[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    if "Number_Baths" in df.columns:
        sns.boxplot(x="Number_Baths", y="Price", data=df, ax=axes4[1], palette="Set2")
        axes4[1].set_title("Price by Bathrooms")
        axes4[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))

    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)
except Exception as e:
    st.error(f"❌ Beds/Baths chart error: {e}")