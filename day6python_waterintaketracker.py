# app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import altair as alt

# ---------- Page setup ----------
st.set_page_config(page_title="Water Intake Tracker 💧", page_icon="💧", layout="centered")

# ---------- Safe Theme (blue bg + readable text) ----------
st.markdown("""
<style>
/* Background */
.stApp { background-color:#0A3A66; }  /* deep blue */

/* Headings (gold) */
h1, h2, h3, h4, h5, h6 { color:#FFD700 !important; }

/* Body text (light gray) */
.stMarkdown, .stText, .stCaption, p, span, label { color:#F0F0F0 !important; }

/* Progress bar track & fill */
[data-testid="stProgress"] > div > div { background-color:#e6eef5 !important; }
[data-testid="stProgress"] > div > div > div { background-color:#00CED1 !important; }

/* Metric value (percentage) + delta */
[data-testid="stMetricValue"] { color:#FFD700 !important; font-weight:700 !important; }
[data-testid="stMetricDelta"] { color:#00FFFF !important; font-weight:700 !important; }

/* Buttons */
div.stButton > button {
  background-color:#1463A0; color:white !important; border-radius:10px; border:1px solid #FFD700;
}
div.stButton > button:hover { background-color:#1E78C8; color:#FFD700 !important; }

/* Inputs keep dark text inside white boxes for readability */
.stNumberInput input, .stDateInput input { color:#0A3A66 !important; }
</style>
""", unsafe_allow_html=True)

# ---------- State & helpers ----------
def init_state():
    if "log" not in st.session_state:
        st.session_state.log = pd.DataFrame(columns=["date", "ml"]).astype({"ml":"int"})
    if "goal_l" not in st.session_state:
        st.session_state.goal_l = 3.0

def add_intake(d: date, ml: int):
    log = st.session_state.log
    if not log.empty and d in set(pd.to_datetime(log["date"]).dt.date):
        idx = pd.to_datetime(log["date"]).dt.date.eq(d)
        st.session_state.log.loc[idx, "ml"] += int(ml)
    else:
        st.session_state.log = pd.concat(
            [log, pd.DataFrame([{"date": pd.to_datetime(d), "ml": int(ml)}])],
            ignore_index=True
        )
    st.session_state.log["date"] = pd.to_datetime(st.session_state.log["date"])
    cutoff = date.today() - timedelta(days=60)
    st.session_state.log = st.session_state.log[st.session_state.log["date"].dt.date >= cutoff].reset_index(drop=True)

def today_total_ml() -> int:
    if st.session_state.log.empty: return 0
    t = date.today()
    return int(st.session_state.log[st.session_state.log["date"].dt.date.eq(t)]["ml"].sum())

def last7_df() -> pd.DataFrame:
    t = date.today()
    days = pd.date_range(t - timedelta(days=6), t, freq="D")
    base = pd.DataFrame({"date": days})
    if st.session_state.log.empty:
        base["ml"] = 0
    else:
        daily = st.session_state.log.groupby(st.session_state.log["date"].dt.date)["ml"].sum()
        base["ml"] = [int(daily.get(d.date(), 0)) for d in days]
    base["liters"] = base["ml"] / 1000.0
    base["label"] = base["date"].dt.strftime("%a %d")
    return base

# ---------- App content (always renders some text) ----------
init_state()
st.title("💧 Water Intake Tracker")
st.write("This app helps you log water, track progress to your daily goal, and view a 7-day chart.")

with st.sidebar:
    st.header("Settings")
    st.session_state.goal_l = st.number_input("Daily goal (L)", 0.5, 10.0, float(st.session_state.goal_l), 0.5)
    if st.button("Reset today's total"):
        if not st.session_state.log.empty:
            st.session_state.log = st.session_state.log[st.session_state.log["date"].dt.date != date.today()].reset_index(drop=True)
        st.success("Cleared today's total.")
    if st.button("Clear all data"):
        st.session_state.log = pd.DataFrame(columns=["date","ml"]).astype({"ml":"int"})
        st.success("Cleared all logs.")

# Add intake
st.subheader("➕ Add Intake")
c1, c2, c3 = st.columns([1,1,1.2])
with c1:
    entry_date = st.date_input("📅 Date", value=date.today(), max_value=date.today())
with c2:
    ml = st.number_input("🥤 Amount (ml)", min_value=50, max_value=2000, value=250, step=50)
with c3:
    st.markdown("**Quick add**")
    q1, q2, q3, q4 = st.columns(4)
    if q1.button("200 ml"): add_intake(entry_date, 200); st.toast("Added 200 ml")
    if q2.button("250 ml"): add_intake(entry_date, 250); st.toast("Added 250 ml")
    if q3.button("300 ml"): add_intake(entry_date, 300); st.toast("Added 300 ml")
    if q4.button("500 ml"): add_intake(entry_date, 500); st.toast("Added 500 ml")

if st.button("Log Water 💦"):
    add_intake(entry_date, int(ml))
    st.success(f"✅ Added {int(ml)} ml for {entry_date.isoformat()}")

st.divider()

# Today progress
goal_ml = int(st.session_state.goal_l * 1000)
today_ml = today_total_ml()
pct = 0.0 if goal_ml <= 0 else min(1.0, today_ml / goal_ml)

st.subheader("📊 Today's Progress")
st.progress(pct)
st.metric("Progress", f"{round(pct*100)}%", f"{today_ml} ml / {goal_ml} ml")

# Weekly chart
st.subheader("📅 Weekly Hydration Chart")
week_df = last7_df()
chart = (
    alt.Chart(week_df)
    .mark_bar(color="#FFD700")  # gold bars
    .encode(
        x=alt.X("label:N", title="Day"),
        y=alt.Y("liters:Q", title="Liters"),
        tooltip=[alt.Tooltip("date:T", title="Date"), alt.Tooltip("ml:Q", title="ml"), alt.Tooltip("liters:Q", title="L")]
    )
    .properties(height=260)
    .configure_axis(labelColor="#F0F0F0", titleColor="#FFD700")
)
st.altair_chart(chart, use_container_width=True)

# Stats & export
st.subheader("🧾 Stats & Data")
w_total = float(week_df["liters"].sum()); w_avg = float(week_df["liters"].mean())
days_hit = int((week_df["liters"] >= st.session_state.goal_l - 1e-9).sum())
s1, s2, s3 = st.columns(3)
s1.metric("7-day total", f"{w_total:.1f} L")
s2.metric("Daily avg", f"{w_avg:.2f} L")
s3.metric("Goal reached", f"{days_hit}/7 days")

with st.expander("View / download raw log"):
    if st.session_state.log.empty:
        st.write("No entries yet.")
    else:
        show_df = st.session_state.log.copy()
        show_df["date"] = show_df["date"].dt.date
        st.dataframe(show_df.sort_values("date", ascending=False), use_container_width=True)
        csv_df = st.session_state.log.copy()
        csv_df["date"] = csv_df["date"].dt.strftime("%Y-%m-%d")
        st.download_button("⬇️ Download CSV", csv_df.to_csv(index=False).encode("utf-8"),
                           file_name="water_log.csv", mime="text/csv")

st.caption("💙 Blue background • 🟡 Gold headings • ⚪ Light text • 🟦 Cyan progress")
