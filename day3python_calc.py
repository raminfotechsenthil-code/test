import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Simple Calculator",
    page_icon="🧮",
    layout="centered"
)

# Main title
st.title("Simple Calculator ➕➖✖➗")

# Create columns for better layout
col1, col2 = st.columns(2)

# Input fields for numbers
with col1:
    num1 = st.number_input("Enter first number:", value=0.0, format="%.6f")

with col2:
    num2 = st.number_input("Enter second number:", value=0.0, format="%.6f")

# Operation selection
operation = st.selectbox(
    "Choose operation:",
    ["Addition ➕", "Subtraction ➖", "Multiplication ✖", "Division ➗"]
)

# Calculate button
if st.button("Calculate", type="primary"):
    try:
        if operation == "Addition ➕":
            result = num1 + num2
            st.success(f"**Result:** {num1} + {num2} = {result}")
            
        elif operation == "Subtraction ➖":
            result = num1 - num2
            st.success(f"**Result:** {num1} - {num2} = {result}")
            
        elif operation == "Multiplication ✖":
            result = num1 * num2
            st.success(f"**Result:** {num1} × {num2} = {result}")
            
        elif operation == "Division ➗":
            if num2 != 0:
                result = num1 / num2
                st.success(f"**Result:** {num1} ÷ {num2} = {result}")
            else:
                st.error("Error: Division by zero is not allowed!")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Add some styling and information
st.markdown("---")
st.markdown("### How to use:")
st.markdown("""
1. Enter two numbers in the input fields
2. Select the desired operation
3. Click the 'Calculate' button to get the result
""")

# Footer
st.markdown("---")
st.markdown("<center>Made with Streamlit 🚀</center>", unsafe_allow_html=True)