import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ---------------- Page Setup ----------------
st.set_page_config(page_title="Gym Workout Logger 🏋", page_icon="🏋", layout="centered")

# ----------- Theme: Red UI with custom buttons -----------
RED_BG = "#A01414"         # app background
TEXT = "#FFFFFF"           # text
INPUT_BG = "#C53B3B"       # inputs
BORDER = "#FF9D9D"         # borders

st.markdown(
    f"""
    <style>
        .stApp {{
            background: {RED_BG};
            color: {TEXT};
        }}
        h1, h2, h3, h4, h5, h6, p, span, label {{
            color: {TEXT} !important;
        }}
        /* Inputs */
        .stTextInput>div>div>input,
        .stNumberInput>div>div>input,
        .stDateInput>div>div input {{
            background-color: {INPUT_BG} !important;
            color: {TEXT} !important;
            border: 1px solid {BORDER} !important;
        }}
        /* Add Entry Button */
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #28A745 !important;  /* green */
            color: #FFFFFF !important;             /* white text */
            border-radius: 10px;
            font-weight: 700;
        }}
        /* Download Button */
        .stDownloadButton>button {{
            background-color: #FFD700 !important;  /* gold/yellow */
            color: #000000 !important;             /* black text */
            border-radius: 10px;
            font-weight: 700;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Gym Workout Logger 🏋️‍♂️")
st.caption("Log exercises (sets, reps, weight) 💪 • Store history 📚 • Weekly progress 📈")

# ---------------- Data storage ----------------
CSV_FILE = "workouts.csv"

@st.cache_data
def _load_csv(path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(path, parse_dates=["date"])
        return df
    except Exception:
        return pd.DataFrame(columns=["date", "exercise", "sets", "reps", "weight", "volume"])

def _save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

if "df" not in st.session_state:
    st.session_state.df = _load_csv(CSV_FILE)

# ---------------- Add Entry Form ----------------
st.subheader("Add a Workout Entry ➕💪")
with st.form("add_entry", clear_on_submit=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        in_date = st.date_input("📅 Date", value=date.today())
        exercise = st.text_input("🏷️ Exercise", placeholder="e.g., Bench Press")
    with c2:
        sets = st.number_input("🔁 Sets", min_value=1, max_value=20, value=3, step=1)
        reps = st.number_input("🔂 Reps", min_value=1, max_value=100, value=10, step=1)
    with c3:
        weight = st.number_input("🏋️ Weight (kg)", min_value=0.0, max_value=1000.0, value=40.0, step=2.5)
    submitted = st.form_submit_button("✅ Add Entry")

if submitted:
    if exercise.strip() == "":
        st.error("Please enter an exercise name.")
    else:
        volume = sets * reps * weight
        new_row = {
            "date": pd.to_datetime(in_date),
            "exercise": exercise.strip().title(),
            "sets": int(sets),
            "reps": int(reps),
            "weight": float(weight),
            "volume": float(volume),
        }
        st.session_state.df = pd.concat(
            [st.session_state.df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        _save_csv(st.session_state.df, CSV_FILE)
        st.success("Entry added and saved ✅")

# ---------------- History + Filters ----------------
st.subheader("Workout History 📚")
df = st.session_state.df.copy()

if df.empty:
    st.info("No entries yet. Add your first workout above!")
else:
    df["date"] = pd.to_datetime(df["date"]).dt.date

    c1, c2, c3 = st.columns(3)
    with c1:
        min_d, max_d = df["date"].min(), df["date"].max()
        date_range = st.date_input("📆 Date range", value=(min_d, max_d))
    with c2:
        exercises = ["All"] + sorted(df["exercise"].dropna().unique().tolist())
        ex_filter = st.selectbox("🏷️ Exercise filter", exercises, index=0)
    with c3:
        if st.button("🗃️ Reset Filters"):
            st.experimental_rerun()

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        df = df[(df["date"] >= start_d) & (df["date"] <= end_d)]
    if ex_filter != "All":
        df = df[df["exercise"] == ex_filter]

    if df.empty:
        st.info("No entries for the selected filters.")
    else:
        st.dataframe(
            df.sort_values(by=["date", "exercise"], ascending=[False, True]).reset_index(drop=True),
            use_container_width=True
        )

        # Download filtered data
        st.download_button(
            "⬇️ Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="workout_history.csv",
            mime="text/csv"
        )

# ---------------- Weekly Progress ----------------
st.subheader("Weekly Progress 📈🔥")
df_all = st.session_state.df.copy()
if df_all.empty:
    st.info("Add entries to see weekly progress.")
else:
    df_all["date"] = pd.to_datetime(df_all["date"])
    df_all["week_start"] = df_all["date"] - pd.to_timedelta(df_all["date"].dt.weekday, unit="D")

    by_exercise = st.checkbox("Breakdown by exercise 🧩 (choose one)", value=False)

    if by_exercise:
        agg = df_all.groupby(["week_start", "exercise"], as_index=False)["volume"].sum()
        options = sorted(agg["exercise"].unique().tolist())
        chosen = st.selectbox("🎯 Choose exercise", options, index=0)
        plot_df = agg[agg["exercise"] == chosen]
        fig, ax = plt.subplots()
        ax.plot(plot_df["week_start"], plot_df["volume"], marker="o", linewidth=2)
        ax.set_title(f"Weekly Volume – {chosen}")
    else:
        agg = df_all.groupby("week_start", as_index=False)["volume"].sum()
        fig, ax = plt.subplots()
        ax.plot(agg["week_start"], agg["volume"], marker="o", linewidth=2)
        ax.set_title("Weekly Total Volume")

    ax.set_xlabel("Week starting")
    ax.set_ylabel("Total Volume (sets × reps × weight)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

# ---------------- Tips ----------------
with st.expander("Tips & Notes 💡"):
    st.markdown(
        """
        - **Volume** = `sets × reps × weight` (approx training load).
        - Use **filters** to analyze a specific period or exercise.
        - Data is saved in `workouts.csv` beside this script.
        - Use **⬇️ Download CSV** to export filtered history.
        """    )
