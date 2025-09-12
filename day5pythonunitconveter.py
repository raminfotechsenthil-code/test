import streamlit as st

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Unit Converter 🔄", page_icon="🔄", layout="centered")

# ---------------------------
# Dark Theme Styling
# ---------------------------
st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #f1f1f1;
    }
    .stApp {
        background-color: #121212;
    }
    .title {
        font-size: 2rem; font-weight: 800; margin-bottom: 0.25rem;
        color: #FFD700;
    }
    .subtitle {
        color: #bbb; margin-bottom: 1.5rem;
    }
    .box {
        padding: 1rem 1.25rem; border: 1px solid #333; border-radius: 12px;
        background: #1e1e1e;
    }
    .hint {
        font-size:0.9rem; color:#aaa;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔄 Unit Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">💵 Currency | 🌡️ Temperature | 📏 Length | ⚖️ Weight</div>', unsafe_allow_html=True)

# ---------------------------
# Helper functions
# ---------------------------
RATES_TO_USD = {"USD": 1.0, "INR": 0.012, "EUR": 1.09, "GBP": 1.28, "AED": 0.2723, "JPY": 0.0069}

def convert_currency(amount, from_ccy, to_ccy):
    if from_ccy == to_ccy:
        return amount
    usd = amount * RATES_TO_USD[from_ccy]
    return usd / RATES_TO_USD[to_ccy]

def convert_temperature(value, from_u, to_u):
    if from_u == "°C": c = value
    elif from_u == "°F": c = (value - 32) * 5/9
    elif from_u == "K": c = value - 273.15
    if to_u == "°C": return c
    elif to_u == "°F": return c * 9/5 + 32
    elif to_u == "K": return c + 273.15

LENGTH_TO_M = {"mm": 0.001,"cm": 0.01,"m": 1.0,"km": 1000.0,"inch": 0.0254,"foot": 0.3048,"yard": 0.9144,"mile": 1609.344}
def convert_length(value, from_u, to_u): return (value * LENGTH_TO_M[from_u]) / LENGTH_TO_M[to_u]

WEIGHT_TO_G = {"mg": 0.001,"g": 1.0,"kg": 1000.0,"tonne": 1_000_000.0,"oz": 28.35,"lb": 453.59}
def convert_weight(value, from_u, to_u): return (value * WEIGHT_TO_G[from_u]) / WEIGHT_TO_G[to_u]

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3, tab4 = st.tabs(["💵 Currency", "🌡️ Temp", "📏 Length", "⚖️ Weight"])

with tab1:
    st.markdown("## 💵 Currency Converter")
    with st.container():
        amount = st.number_input("Enter Amount", value=100.0, step=1.0)
        c1, c2 = st.columns(2)
        from_ccy = c1.selectbox("From", list(RATES_TO_USD.keys()))
        to_ccy = c2.selectbox("To", list(RATES_TO_USD.keys()), index=1)
        result = convert_currency(amount, from_ccy, to_ccy)
        st.metric(label=f"{amount} {from_ccy} = ", value=f"💰 {result:.2f} {to_ccy}")

with tab2:
    st.markdown("## 🌡️ Temperature Converter")
    value = st.number_input("Enter Temperature", value=25.0, step=0.1)
    c1, c2 = st.columns(2)
    from_u = c1.selectbox("From", ["°C","°F","K"])
    to_u = c2.selectbox("To", ["°C","°F","K"], index=1)
    st.metric(label=f"{value} {from_u} = ", value=f"🔥 {convert_temperature(value, from_u, to_u):.2f} {to_u}")

with tab3:
    st.markdown("## 📏 Length Converter")
    value = st.number_input("Enter Length", value=1.0, step=0.1)
    c1, c2 = st.columns(2)
    from_u = c1.selectbox("From", list(LENGTH_TO_M.keys()))
    to_u = c2.selectbox("To", list(LENGTH_TO_M.keys()), index=3)
    st.metric(label=f"{value} {from_u} = ", value=f"📐 {convert_length(value, from_u, to_u):.4f} {to_u}")

with tab4:
    st.markdown("## ⚖️ Weight Converter")
    value = st.number_input("Enter Weight", value=1.0, step=0.1)
    c1, c2 = st.columns(2)
    from_u = c1.selectbox("From", list(WEIGHT_TO_G.keys()), index=2)
    to_u = c2.selectbox("To", list(WEIGHT_TO_G.keys()), index=5)
    st.metric(label=f"{value} {from_u} = ", value=f"🥗 {convert_weight(value, from_u, to_u):.4f} {to_u}")

st.markdown("<div class='hint'>✨ Emojis make it fun! Add more units or APIs anytime.</div>", unsafe_allow_html=True)
