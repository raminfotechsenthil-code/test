# dog_show_registration_app.py
# Streamlit: Dog Show Event Registration 🎉🐶

import streamlit as st
import pandas as pd
import io
import re
from datetime import datetime
import base64

st.set_page_config(page_title="Dog Show Registration 🐶🎉", page_icon="🐶", layout="centered")

# ------------------ Event Info Banner ------------------
st.markdown(
    """
    <div style='
        background: linear-gradient(90deg, #ff9a9e, #fad0c4, #fbc2eb, #a1c4fd);
        padding: 20px; border-radius: 15px; text-align: center; color: black;
        box-shadow: 0px 6px 18px rgba(0,0,0,0.25);'>
        <h1 style='margin-bottom:5px;'>🐾 Dog Show Event 2025 🎉</h1>
        <h3 style='margin-top:0;'>📅 Date: <b>18-09-2025</b> &nbsp;&nbsp; 🕓 Time: <b>4.30 PM – 6.30 PM</b></h3>
        <h3>📍 Venue: <b>Vadapalani</b></h3>
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

st.caption("Register your champion dog! Organizers can export registrations as CSV.")

# ------------------ Storage ------------------
if "registrations" not in st.session_state:
    st.session_state.registrations = []

EVENT_CLASSES = [
    "Puppy Class (under 1 year)",
    "Junior Class (1–2 years)",
    "Adult Class (2–7 years)",
    "Senior Class (7+ years)",
    "Best Costume 👗",
    "Best Trick 🎩",
    "Agility Run 🏃‍♂️",
    "Obedience Round 🐾",
]

AGE_CATEGORIES = ["Puppy (<1y)", "Junior (1–2y)", "Adult (2–7y)", "Senior (7+y)"]

# ------------------ Helpers ------------------
def valid_email(email: str) -> bool:
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or "") is not None

def make_registration_id(email: str, dog_name: str) -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    base = f"{email.lower()}-{dog_name.lower()}-{ts}"
    return "DOG-" + base.replace(" ", "")[:28].upper()

def is_duplicate(email: str, dog_name: str) -> bool:
    for r in st.session_state.registrations:
        if r["Email"].lower() == email.lower() and r["Dog Name"].lower() == dog_name.lower():
            return True
    return False

def image_to_b64(file) -> str | None:
    if not file:
        return None
    raw = file.read()
    return "data:" + file.type + ";base64," + base64.b64encode(raw).decode("utf-8")

# ------------------ Registration Form ------------------
st.subheader("📝 Register Your Dog")

with st.form("dog_show_form", clear_on_submit=True):
    colA, colB = st.columns(2)
    with colA:
        owner_name = st.text_input("Owner Name")
        email = st.text_input("Email")
        dog_name = st.text_input("Dog Name")
        breed = st.text_input("Breed")
    with colB:
        age_cat = st.selectbox("Age Category", AGE_CATEGORIES, index=2)
        event_class = st.selectbox("Event Class", EVENT_CLASSES, index=2)
        vaccinated = st.checkbox("I confirm vaccinations are up to date ✅")
        photo = st.file_uploader("Upload Dog Photo (optional)", type=["png", "jpg", "jpeg"])

    notes = st.text_area("Notes (diet, temperament, special requests)", placeholder="Anything we should know?")
    agree = st.checkbox("I agree to the event rules & handling terms.")

    submitted = st.form_submit_button("✅ Submit Registration")

    if submitted:
        if not owner_name.strip() or not email.strip() or not dog_name.strip() or not breed.strip():
            st.error("Please fill all required fields (Owner, Email, Dog Name, Breed).")
        elif not valid_email(email):
            st.error("Please enter a valid email address.")
        elif not vaccinated:
            st.error("Vaccination confirmation is required for participation.")
        elif not agree:
            st.error("You must agree to the event rules.")
        elif is_duplicate(email, dog_name):
            st.warning(f"Duplicate found: {dog_name} is already registered with {email}.")
        else:
            reg_id = make_registration_id(email, dog_name)
            photo_b64 = image_to_b64(photo)
            st.session_state.registrations.append({
                "Registration ID": reg_id,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Owner Name": owner_name.strip(),
                "Email": email.strip(),
                "Dog Name": dog_name.strip(),
                "Breed": breed.strip(),
                "Age Category": age_cat,
                "Event Class": event_class,
                "Vaccinated": "Yes" if vaccinated else "No",
                "Notes": notes.strip(),
                "PhotoB64": photo_b64,
            })
            st.success(f"🎉 Thanks {owner_name}! **{dog_name}** is registered for **{event_class}**.")
            st.info(f"Your Registration ID: **{reg_id}** (save this for check-in)")

# ------------------ Live Stats ------------------
st.subheader("📊 Live Registrations")
total = len(st.session_state.registrations)
st.metric("Total Registrations", total)

if total > 0:
    df = pd.DataFrame(st.session_state.registrations)
    show_cols = [c for c in df.columns if c != "PhotoB64"]
    st.dataframe(df[show_cols], hide_index=True, use_container_width=True)

    st.caption("Registrations per Event Class")
    per_class = df["Event Class"].value_counts().rename_axis("Event Class").reset_index(name="Count")
    st.bar_chart(per_class.set_index("Event Class"))

    csv_buf = io.StringIO()
    df[show_cols].to_csv(csv_buf, index=False)
    st.download_button(
        "📥 Download CSV (Organizer View)",
        data=csv_buf.getvalue(),
        file_name="dog_show_registrations.csv",
        mime="text/csv",
    )
else:
    st.info("No registrations yet. First paw on the floor wins! 🐾")

with st.expander("🛠️ Organizer Tools (clear data)"):
    if st.button("🧹 Clear ALL registrations"):
        st.session_state.registrations = []
        st.success("Cleared! (Session only)")
