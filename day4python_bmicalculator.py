import streamlit as st

# ---------------- Page Setup ----------------
st.set_page_config(page_title="BMI Calculator", page_icon="🧮", layout="centered")

# --- Fun, colorful theme via CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8ffd7 0%, #d7f3ff 50%, #ffe3f1 100%);
        background-attachment: fixed;
    }
    .glass {
        background: rgba(255,255,255,0.65);
        border: 1px solid rgba(255,255,255,0.35);
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        backdrop-filter: blur(6px);
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 1rem;
    }
    [data-testid="stMetric"] {
        border-radius: 16px;
        padding: 10px 12px;
        background: linear-gradient(135deg, #fff 0%, #f6faff 100%);
        border: 1px solid rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Header ----------------
st.title("🧮🎈 BMI Calculator — Colorful Edition")
st.caption("⚖️ Weight in **kg** • 📏 Height in **feet & inches** • 📊 Metrics with **delta** • 💡 With Fitness Tips")

# ---------------- Helpers ----------------
def bmi_from_metric_kg_and_feet_inches(weight_kg: float, height_ft: float, height_in: float) -> float:
    total_inches = height_ft * 12.0 + height_in
    meters = total_inches * 0.0254
    return weight_kg / (meters ** 2)

def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight 😕"
    elif bmi < 25:
        return "Normal 🙂"
    elif bmi < 30:
        return "Overweight 😐"
    else:
        return "Obese 😟"

def healthy_weight_range_for_height_ft_in(height_ft: float, height_in: float):
    total_inches = height_ft * 12.0 + height_in
    meters = total_inches * 0.0254
    lo_kg = 18.5 * (meters ** 2)
    hi_kg = 24.9 * (meters ** 2)
    return (lo_kg, hi_kg)

def fitness_tips(bmi: float) -> str:
    if bmi < 18.5:
        return "🍽️ Eat more nutrient-rich foods, 🏋️ Strength training, and 🛌 Adequate rest."
    elif bmi < 25:
        return "🥗 Maintain a balanced diet, 🚶‍♂️ Regular activity (30 min/day), and 💧 Stay hydrated."
    elif bmi < 30:
        return "🥦 Cut down on junk food, 🏃 Do cardio + strength training, and ⏰ Monitor calories."
    else:
        return "🥗 Follow a low-calorie balanced diet, 🚴‍♀️ Increase physical activity, and 👩‍⚕️ Consult a doctor/nutritionist."

# ---------------- Inputs ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    weight_kg = st.number_input("⚖️ Weight (kg)", min_value=0.0, value=70.0, step=0.1)
with c2:
    st.markdown("📏 **Height** (feet + inches)")
    hcol1, hcol2 = st.columns(2)
    with hcol1:
        height_ft = st.number_input("Feet 🦶", min_value=0.0, value=5.0, step=1.0)
    with hcol2:
        height_in = st.number_input("Inches 📐", min_value=0.0, value=7.0, step=0.5)

st.caption("💡 Tip: Flip the toggle to calculate/update. Try changing values and watch the **delta** in the BMI metric!")

calculate = st.toggle("🔄 Calculate BMI", value=False)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Session state ----------------
if "last_bmi" not in st.session_state:
    st.session_state.last_bmi = None

# ---------------- Compute & Display ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

if calculate:
    if (height_ft == 0 and height_in == 0) or weight_kg <= 0:
        st.error("🚫 Please enter valid weight and height.")
    else:
        bmi = bmi_from_metric_kg_and_feet_inches(weight_kg, height_ft, height_in)
        cat = bmi_category(bmi)
        lo_kg, hi_kg = healthy_weight_range_for_height_ft_in(height_ft, height_in)

        delta = None if st.session_state.last_bmi is None else round(bmi - st.session_state.last_bmi, 2)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("🧮 BMI", value=f"{bmi:.2f}", delta=(f"{delta:+.2f}" if delta is not None else None))
        with m2:
            st.metric("🏷️ Category", value=cat)
        with m3:
            st.metric("🎯 Healthy Range", value=f"{lo_kg:.1f}–{hi_kg:.1f} kg")

        st.session_state.last_bmi = bmi

        # Fitness Tips Section
        st.subheader("💪 Fitness Tips for You")
        st.success(fitness_tips(bmi))

else:
    st.info("⌛ Toggle **Calculate BMI** to see results.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown(
    """
---  
📝 **Notes**  
- BMI is a screening tool, not a diagnosis.  
- Fitness tips here are **general**. For personalized advice, consult a healthcare professional.  
"""
)
