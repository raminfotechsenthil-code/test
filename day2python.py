import streamlit as st

# Set page style
st.set_page_config(page_title="Expense Splitter", layout="centered")
st.markdown(
    """
    <style>
    body {
        background-color: skyblue;
        color: black;
    }
    .stTextInput label, .stNumberInput label, .stMarkdown, .stButton button {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💸 Friends Expense Splitter")

st.markdown("Easily split dinner/trip expenses among friends!")

# Input: total and number of people
total_amount = st.number_input("Enter Total Amount (₹):", min_value=0.0, step=100.0)
num_people = st.number_input("Enter Number of People:", min_value=1, step=1)

# Optionally enter names & contributions
names = []
contributions = []

st.subheader("Optional: Add each person's contribution")
for i in range(int(num_people)):
    col1, col2 = st.columns([2, 1])
    with col1:
        name = st.text_input(f"Person {i+1} Name", key=f"name_{i}")
    with col2:
        contrib = st.number_input(f"Contribution (₹)", min_value=0.0, step=50.0, key=f"contrib_{i}")
    names.append(name if name else f"Person {i+1}")
    contributions.append(contrib)

if st.button("Calculate Split"):
    if total_amount > 0 and num_people > 0:
        equal_share = total_amount / num_people
        st.markdown(f"### Each person should ideally pay: **₹{equal_share:.2f}**")

        if sum(contributions) > 0:
            st.subheader("Settlement Details")
            for i in range(num_people):
                balance = contributions[i] - equal_share
                if balance > 0:
                    st.write(f"✅ {names[i]} should **get back ₹{balance:.2f}**")
                elif balance < 0:
                    st.write(f"❌ {names[i]} should **pay ₹{-balance:.2f}**")
                else:
                    st.write(f"✔️ {names[i]} is **settled**")
    else:
        st.warning("Please enter valid total amount and number of people.")
