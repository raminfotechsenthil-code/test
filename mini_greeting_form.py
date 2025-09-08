# greet_form.py
import streamlit as st  # Use only streamlit

st.set_page_config(page_title="Mini Greeting Form", page_icon="👋", layout="centered")
st.title("👋 Mini Greeting Form")

with st.form("greet_form"):
    name = st.text_input("Your name")
    age = st.slider("Your age", min_value=1, max_value=100, value=25)
    submitted = st.form_submit_button("Say hello")

if submitted:
    if name.strip():
        st.success(f"Hello {name}! You are {age} years young 🎉")
    else:
        st.warning("Please enter your name.")
