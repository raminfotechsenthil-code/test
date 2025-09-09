import streamlit as st

# Page Config
st.set_page_config(page_title="Expense Splitter", layout="centered")

# Custom CSS for colorful theme
st.markdown(
    """
    <style>
    body {
       background: linear-gradient(135deg, #89f7fe, #66a6ff);
       color: #111;
        font-family: 'Arial';
    }
    .stTextInput label, .stNumberInput label, .stMarkdown, .stButton button {
        color: black !important;
        font-weight: bold;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff9966, #ff5e62);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.5em 1em;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
    }
    .result-card {
        background: #ffffffcc;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌈 Friends Expense Splitter")
st.markdown("Split dinner/trip expenses fairly with friends in a colorful way 🎉")

# Input fields
total_amount = st.number_input("💰 Enter Total Amount (₹):", min_value=0.0, step=100.0)
num_people = st.number_input("👥 Enter Number of People:", min_value=1, step=1)

# Person contributions
names = []
contributions = []

st.subheader("✏️ Add each person's contribution (optional)")
for i in range(int(num_people)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}")
    with col2:
        contrib = st.number_input(f"Paid (₹)", min_value=0.0, step=50.0, key=f"contrib_{i}")
    names.append(name if name else f"Person {i+1}")
    contributions.append(contrib)

# Calculate
if st.button("🚀 Calculate Split"):
    if total_amount > 0 and num_people > 0:
        equal_share = total_amount / num_people
        st.markdown(
            f"<div class='result-card'><h3>Each person should ideally pay: ₹{equal_share:.2f}</h3></div>",
            unsafe_allow_html=True,
        )

        if sum(contributions) > 0:
            st.subheader("📊 Settlement Details")
            for i in range(num_people):
                balance = contributions[i] - equal_share
                if balance > 0:
                    st.markdown(
                        f"<div class='result-card'>✅ {names[i]} should <b>get back ₹{balance:.2f}</b></div>",
                        unsafe_allow_html=True,
                    )
                elif balance < 0:
                    st.markdown(
                        f"<div class='result-card'>❌ {names[i]} should <b>pay ₹{-balance:.2f}</b></div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div class='result-card'>✔️ {names[i]} is <b>settled</b></div>",
                        unsafe_allow_html=True,
                    )
    else:
        st.warning("⚠️ Please enter valid total amount and number of people.")
