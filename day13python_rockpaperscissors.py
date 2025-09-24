# rps_tournament.py
# Rock, Paper, Scissors ✊✋✌️ — Tournament (Dark theme, white text, dropdown options black)
# Run: streamlit run rps_tournament.py

import random
import streamlit as st

st.set_page_config(page_title="Rock, Paper, Scissors", page_icon="✊", layout="centered")

# ---------- DARK THEME + SELECTBOX FIX ----------
st.markdown("""
<style>
/* App backgrounds */
:root, body { background-color: #0d1117; }
[data-testid="stAppViewContainer"] { background-color: #0d1117; }
[data-testid="stHeader"] { background-color: #0d1117; }
[data-testid="stSidebar"] { background-color: #161b22; }

/* Make ALL text white by default */
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"],
h1, h2, h3, h4, h5, h6, p, span, div, label, small, code, pre,
[data-testid="stMarkdownContainer"], .stText, .stNumberInput, .stSelectbox, .stDataFrame, .stTable {
  color: #ffffff !important;
}

/* Inputs & selectbox field text */
select, option, input, textarea { color: #ffffff; background-color: #0f1720; border-color: #2a3340; }

/* Streamlit Selectbox container (BaseWeb Select) */
[data-baseweb="select"] {
  color: #ffffff !important;
}

/* Dropdown menu list: options = black text on white background */
ul[role="listbox"] {
  background-color: #ffffff !important;
  border: 1px solid #e5e7eb !important;
}
ul[role="listbox"] li {
  background-color: #ffffff !important;
  color: #000000 !important;
}
ul[role="listbox"] li:hover {
  background-color: #fde047 !important; /* yellow highlight on hover */
  color: #000000 !important;
}

/* Selected option (rendered chip/text inside the closed select) → white */
[data-baseweb="select"] span {
  color: #ffffff !important;
}

/* Metric styles (numbers bright yellow) */
[data-testid="stMetricValue"] {
  color: #facc15 !important;
  font-weight: 900;
}
[data-testid="stMetricLabel"] {
  color: #ffffff !important;
  font-weight: 700;
}

/* Buttons */
div.stButton > button {
  background-color: #facc15;
  color: #0d1117 !important;
  font-weight: 800;
  border-radius: 10px;
  border: none;
  height: 60px;
  font-size: 22px;
}
div.stButton > button:hover {
  background-color: #fde047;
  color: #000000 !important;
}

/* Tables */
[data-testid="stTable"] *, [data-testid="stDataFrame"] * {
  color: #ffffff !important;
}

/* Links and captions */
a, a:visited { color: #fde047 !important; }
</style>
""", unsafe_allow_html=True)

# ---------- Game constants ----------
CHOICES = {"Rock": "✊", "Paper": "✋", "Scissors": "✌️"}

# ---------- Initialize state ----------
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
    st.session_state.comp_score = 0
    st.session_state.rounds = []           # list of dicts with results
    st.session_state.round_number = 1
    st.session_state.last_result = "Start the game!"
    st.session_state.tournament_over = False

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Tournament Settings")
max_rounds = st.sidebar.selectbox("Select total rounds:", [5, 7, 10], index=2)  # default 10

def reset_tournament():
    st.session_state.user_score = 0
    st.session_state.comp_score = 0
    st.session_state.rounds = []
    st.session_state.round_number = 1
    st.session_state.last_result = "Game reset. Start again!"
    st.session_state.tournament_over = False

if st.sidebar.button("🔄 Reset Tournament"):
    reset_tournament()
    st.rerun()

# ---------- Helpers ----------
def play(user_choice: str):
    """Play one round if tournament not over."""
    if st.session_state.tournament_over:
        return

    comp_choice = random.choice(list(CHOICES.keys()))

    if user_choice == comp_choice:
        result_text = "Draw 🤝"
    elif (user_choice == "Rock" and comp_choice == "Scissors") \
         or (user_choice == "Paper" and comp_choice == "Rock") \
         or (user_choice == "Scissors" and comp_choice == "Paper"):
        result_text = "You Win 🎉"
        st.session_state.user_score += 1
    else:
        result_text = "Computer Wins 💻"
        st.session_state.comp_score += 1

    st.session_state.rounds.append({
        "Round": st.session_state.round_number,
        "You": f"{CHOICES[user_choice]} {user_choice}",
        "Computer": f"{CHOICES[comp_choice]} {comp_choice}",
        "Result": result_text
    })
    st.session_state.last_result = (
        f"You: {CHOICES[user_choice]}  |  Computer: {CHOICES[comp_choice]}  →  **{result_text}**"
    )
    st.session_state.round_number += 1

    # End tournament after max rounds are played
    if st.session_state.round_number > max_rounds:
        st.session_state.tournament_over = True

def reset_game_only():
    """Reset scores and rounds but keep settings."""
    reset_tournament()

# ---------- UI ----------
st.title("✊✋✌️ Rock – Paper – Scissors")
st.caption("Dark theme • All text white • Yellow buttons • Tournament mode")

# Scoreboard
c1, c2, c3 = st.columns(3)
c1.metric("👤 You", st.session_state.user_score)
c2.metric("💻 Computer", st.session_state.comp_score)
c3.metric("🎯 Round", f"{st.session_state.round_number-1}/{max_rounds}")

# Make a move
st.subheader("Make your move:")
bcols = st.columns(3)
if bcols[0].button("✊ Rock"):
    play("Rock")
if bcols[1].button("✋ Paper"):
    play("Paper")
if bcols[2].button("✌️ Scissors"):
    play("Scissors")

# Last result
st.markdown("### 🎯 Last Result")
st.write(st.session_state.last_result)

# Round history
if st.session_state.rounds:
    st.markdown("### 📜 Round History")
    st.table(st.session_state.rounds[::-1])  # latest first

# Tournament over summary
if st.session_state.tournament_over:
    st.markdown("## 🏆 Tournament Over")
    if st.session_state.user_score > st.session_state.comp_score:
        champ = "🎉 You are the Champion!"
    elif st.session_state.comp_score > st.session_state.user_score:
        champ = "💻 Computer is the Champion!"
    else:
        champ = "🤝 It's a Draw!"
    st.success(champ)

    st.button("🔄 Play Again", on_click=reset_game_only)
