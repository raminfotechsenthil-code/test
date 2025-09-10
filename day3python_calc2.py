import streamlit as st

# Page config
st.set_page_config(page_title="Simple Calculator", page_icon="➕")

# Custom CSS for theme
st.markdown(
    """
    <style>
        /* Background */
        .stApp {
            background-color: #87CEEB; /* Sky Blue */
            color: black;
        }

        /* Titles */
        h1 {
            color: #000000;
            text-align: center;
        }

        /* Buttons */
        div.stButton > button {
            background-color: #1E90FF;
            color: white;
            border-radius: 10px;
            font-size: 18px;
            height: 3em;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #104E8B;
            color: white;
        }

        /* Select box text */
        .stSelectbox label, .stNumberInput label {
            font-weight: bold;
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Simple Calculator ➕➖✖➗")

# Input numbers
num1 = st.number_input("Enter first number", step=1.0, format="%.2f")
num2 = st.number_input("Enter second number", step=1.0, format="%.2f")

# Select operation
operation = st.selectbox("Choose operation", ["Addition (+)", "Subtraction (-)", "Multiplication (×)", "Division (÷)"])

# Calculate
if st.button("Calculate"):
    if operation == "Addition (+)":
        result = num1 + num2
        st.success(f"Result: {num1} + {num2} = {result}")
    elif operation == "Subtraction (-)":
        result = num1 - num2
        st.success(f"Result: {num1} - {num2} = {result}")
    elif operation == "Multiplication (×)":
        result = num1 * num2
        st.success(f"Result: {num1} × {num2} = {result}")
    elif operation == "Division (÷)":
        if num2 != 0:
            result = num1 / num2
            st.success(f"Result: {num1} ÷ {num2} = {result}")
        else:
            st.error("❌ Error: Division by zero is not allowed!")
