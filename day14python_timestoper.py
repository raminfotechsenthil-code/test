# stopwatch_app.py
import time
import math
import streamlit as st

st.set_page_config(page_title="Stopwatch ⏱️", page_icon="⏱️", layout="centered")

# ---------------- State ----------------
def _init_state():
    for k, v in {
        "running": False,         # currently running?
        "start_perf": 0.0,        # perf_counter() at last start/resume
        "accumulated": 0.0,       # time saved while paused (sec)
        "laps": [],               # list of lap stamps (sec)
    }.items():
        if k not in st.session_state:
            st.session_state[k] = v
_init_state()

# ---------------- Helpers ----------------
def now_elapsed() -> float:
    if st.session_state.running:
        return st.session_state.accumulated + (time.perf_counter() - st.session_state.start_perf)
    return st.session_state.accumulated

def fmt(t: float) -> str:
    t = max(0.0, float(t))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t - math.floor(t)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:03d}"

def start():
    if not st.session_state.running:
        st.session_state.start_perf = time.perf_counter()
        st.session_state.running = True

def stop():
    if st.session_state.running:
        st.session_state.accumulated += time.perf_counter() - st.session_state.start_perf
        st.session_state.running = False

def reset():
    st.session_state.running = False
    st.session_state.start_perf = 0.0
    st.session_state.accumulated = 0.0
    st.session_state.laps = []

def lap():
    st.session_state.laps.append(now_elapsed())

# ---------------- Styles ----------------
st.markdown(
    """
    <style>
    .timer-box{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
        font-weight: 800;
        font-size: clamp(42px, 9vw, 92px);
        padding: 24px 20px;
        text-align:center;
        border-radius: 18px;
        color: #E9F2FF;
        background: radial-gradient(120% 120% at 50% 0%, rgba(255,255,255,0.14), rgba(0,0,0,0.12)), #0F1116;
        box-shadow: inset 0 10px 28px rgba(0,0,0,0.4), 0 12px 24px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.08);
        letter-spacing: 1px;
        user-select: none;
        text-shadow: 0 0 14px rgba(90,220,255,.25);
    }
    .pill{
        display:inline-block; margin-right:8px; padding:6px 12px; border-radius:999px;
        font-size:12px; font-weight:600; letter-spacing:.3px;
        border:1px solid rgba(255,255,255,.12); background:rgba(255,255,255,.06);
    }
    .lap-row{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("⏱️ Stopwatch")

# ---------------- Display ----------------
elapsed = now_elapsed()

# Blink the last ":" (between MM and SS) every 0.5s when running
display_txt = fmt(elapsed)
if st.session_state.running and (int((elapsed * 2) % 2) == 0):
    display_txt = display_txt[:5] + " " + display_txt[6:]  # HH:MM SS.mmm

# Status pills
p1, p2, _ = st.columns([1,1,3])
with p1:
    st.markdown(f'<span class="pill">Status: {"Running" if st.session_state.running else "Stopped"}</span>', unsafe_allow_html=True)
with p2:
    st.markdown(f'<span class="pill">Laps: {len(st.session_state.laps)}</span>', unsafe_allow_html=True)

st.markdown(f'<div class="timer-box">{display_txt}</div>', unsafe_allow_html=True)
st.caption("Accurate timing via `time.perf_counter()`; tab switching won’t skew the clock.")

# ---------------- Controls ----------------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.button("▶️ Start / Resume", type="primary", use_container_width=True, on_click=start)
with c2:
    st.button("⏸️ Stop", use_container_width=True, on_click=stop)
with c3:
    st.button("🔁 Reset", use_container_width=True, on_click=reset)
with c4:
    st.button("🏷️ Lap", use_container_width=True, on_click=lap,
              disabled=not (st.session_state.running or elapsed > 0))

# ---------------- Laps ----------------
if st.session_state.laps:
    st.subheader("Lap Times")
    h1, h2, h3 = st.columns([1,2,2])
    h1.markdown("**#**"); h2.markdown("**Lap**"); h3.markdown("**Δ from previous**")

    for i, t in enumerate(st.session_state.laps, start=1):
        delta = t - (st.session_state.laps[i-2] if i > 1 else 0.0)
        a, b, c = st.columns([1,2,2])
        a.markdown(f"<div class='lap-row'>{i}</div>", unsafe_allow_html=True)
        b.markdown(f"<div class='lap-row'>{fmt(t)}</div>", unsafe_allow_html=True)
        c.markdown(f"<div class='lap-row'>{fmt(delta)}</div>", unsafe_allow_html=True)

# ---------------- Auto-refresh ----------------
if st.session_state.running:
    time.sleep(0.1)  # ~10 fps
    st.rerun()       # ✅ modern Streamlit
