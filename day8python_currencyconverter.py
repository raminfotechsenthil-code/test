# currency_converter_yellow_black.py
# Streamlit app: Currency Converter 💱 with yellow/black theme + emoji

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Currency Converter 💱", page_icon="💱", layout="centered")

# ---- Custom CSS for Yellow & Black Theme ----
st.markdown("""
    <style>
        body, .stApp {
            background-color: black;
            color: yellow;
        }
        .stButton button {
            background-color: yellow;
            color: black;
            font-weight: bold;
            border-radius: 8px;
        }
        .stMetric {
            background: #222;
            border: 2px solid yellow;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown("<h1 style='text-align:center; color:yellow;'>💱 Currency Converter 💱</h1>", unsafe_allow_html=True)
st.caption("⚡ Static rates (editable in code). Simple dropdown + number input.")

# ---- Static exchange rates (INR per 1 unit of the currency) ----
RATES_INR_PER_UNIT = {
    "INR": 1.00,   # base
    "USD": 84.00,
    "EUR": 90.00,
    "GBP": 105.00,
    "AED": 22.90,
    "JPY": 0.56,
    "AUD": 56.00,
    "CAD": 62.00,
    "SGD": 62.50,
}

currencies = list(RATES_INR_PER_UNIT.keys())

# ---- Sidebar: rates table ----
with st.sidebar:
    st.subheader("📋 Static Rates (₹ per 1 unit)")
    df_rates = pd.DataFrame(
        {"Currency": currencies, "💰 INR per Unit": [RATES_INR_PER_UNIT[c] for c in currencies]}
    )
    # Show only 2 decimal places in table
    df_rates["💰 INR per Unit"] = df_rates["💰 INR per Unit"].map(lambda x: f"{x:.2f}")
    st.dataframe(df_rates, hide_index=True, use_container_width=True)
    st.caption("✍️ Edit the numbers in code to update rates.")

# ---- Converter UI ----
col1, col2 = st.columns(2)
with col1:
    from_cur = st.selectbox("🔽 From", currencies, index=currencies.index("INR"))
with col2:
    to_cur = st.selectbox("🔼 To", currencies, index=currencies.index("USD"))

amount = st.number_input("💵 Enter Amount", min_value=0.0, value=100.0, step=1.0, format="%.2f")

# Conversion logic (INR as the bridge)
def convert(amount: float, from_c: str, to_c: str) -> float:
    if from_c == to_c:
        return amount
    in_inr = amount * RATES_INR_PER_UNIT[from_c]
    out_amt = in_inr / RATES_INR_PER_UNIT[to_c]
    return out_amt

# Show conversion instantly
result = convert(amount, from_cur, to_cur)
st.success(f"✨ {amount:,.2f} {from_cur} = {result:,.2f} {to_cur} ✨")

# ---- Metric preview ----
st.metric(label="🔎 Live Preview", value=f"{result:,.2f} {to_cur}")

st.caption("⚠️ Disclaimer: Demo uses static example rates, not real-time forex.")
