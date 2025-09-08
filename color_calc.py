# simple_calc.py
import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")
st.title("🧮 Simple Calculator")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("First number", value=0.0, format="%.10g")
with col2:
    b = st.number_input("Second number", value=0.0, format="%.10g")

op = st.selectbox("Operation", ["+", "-", "×", "÷", "%", "^"], index=0)

if st.button("Calculate"):
    try:
        if op == "+":      res = a + b
        elif op == "-":    res = a - b
        elif op == "×":    res = a * b
        elif op == "÷":
            if b == 0: raise ZeroDivisionError("Cannot divide by zero")
            res = a / b
        elif op == "%":
            if b == 0: raise ZeroDivisionError("Cannot modulo by zero")
            res = a % b
        elif op == "^":    res = a ** b

        st.success(f"Result: {res}")
    except ZeroDivisionError as e:
        st.error(str(e))
