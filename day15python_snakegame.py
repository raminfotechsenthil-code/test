# snake_streamlit.py
import random
import time
from typing import List, Tuple

import numpy as np
import streamlit as st

st.set_page_config(page_title="Snake 🐍 – Streamlit", page_icon="🐍", layout="wide")

Cell = Tuple[int, int]

# -------------------- State --------------------
def init_state():
    g = 22  # grid size
    st.session_state.grid = g
    st.session_state.cell_px = 24
    # 3-long snake centered, facing right
    st.session_state.snake = [(g//2 + i, g//2) for i in range(0, -3, -1)]
    st.session_state.dir = (1, 0)
    st.session_state.pending_dir = (1, 0)
    st.session_state.food = spawn_food()
    st.session_state.score = 0
    st.session_state.speed = 0.20      # slower default so it’s playable
    st.session_state.is_running = False  # start paused; press Start
    st.session_state.game_over = False
    st.session_state.keybox = ""
    st.session_state.countdown = 0      # 3..2..1 Start

def spawn_food() -> Cell:
    g = st.session_state.grid
    snake = set(st.session_state.snake)
    while True:
        p = (random.randint(0, g-1), random.randint(0, g-1))
        if p not in snake:
            return p

def valid_turn(new_dir: Cell) -> bool:
    cx, cy = st.session_state.dir
    nx, ny = new_dir
    return (nx, ny) != (-cx, -cy)

def turn(new_dir: Cell):
    if valid_turn(new_dir):
        st.session_state.pending_dir = new_dir

def restart():
    init_state()

def start_with_countdown():
    if st.session_state.game_over:
        restart()
    st.session_state.countdown = 3
    st.session_state.is_running = False

if "grid" not in st.session_state:
    init_state()

# -------------------- Game step (with correct tail rule) --------------------
def step():
    if st.session_state.game_over or not st.session_state.is_running:
        return

    g = st.session_state.grid
    snake: List[Cell] = st.session_state.snake

    # apply direction chosen by user this tick
    st.session_state.dir = st.session_state.pending_dir
    dx, dy = st.session_state.dir
    hx, hy = snake[0]
    new_head = (hx + dx, hy + dy)

    # wall collision
    if not (0 <= new_head[0] < g and 0 <= new_head[1] < g):
        st.session_state.game_over = True
        st.session_state.is_running = False
        return

    will_grow = (new_head == st.session_state.food)

    # self collision (allow stepping onto tail if it will move this tick)
    body_to_check = snake if will_grow else snake[:-1]
    if new_head in body_to_check:
        st.session_state.game_over = True
        st.session_state.is_running = False
        return

    # move snake
    snake.insert(0, new_head)
    if will_grow:
        st.session_state.score += 1
        st.session_state.food = spawn_food()
    else:
        snake.pop()

# -------------------- Drawing --------------------
def draw_board() -> np.ndarray:
    g, c = st.session_state.grid, st.session_state.cell_px
    H, W = g*c, g*c
    img = np.zeros((H, W, 3), dtype=np.uint8)

    # colorful checkerboard
    base1, base2 = np.array([28, 26, 68]), np.array([32, 30, 84])
    for y in range(g):
        for x in range(g):
            img[y*c:(y+1)*c, x*c:(x+1)*c] = base1 if (x+y) % 2 == 0 else base2
    img[::c, :, :] = 50
    img[:, ::c, :] = 50

    # food
    fx, fy = st.session_state.food
    img[fy*c:(fy+1)*c, fx*c:(fx+1)*c] = [235, 64, 90]

    # snake
    for i, (sx, sy) in enumerate(st.session_state.snake):
        color = np.array([34, 200, 160]) if i > 0 else np.array([80, 255, 180])
        block = img[sy*c:(sy+1)*c, sx*c:(sx+1)*c]
        block[...] = color
        inner = block[4:-4, 4:-4]
        if inner.size > 0:
            inner[...] = np.clip(color + 20, 0, 255)
    return img

# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## 🎮 Controls & Settings")
    st.write("Use buttons **or** type **W/A/S/D** or **up/down/left/right** here and press **Enter**.")
    st.session_state.keybox = st.text_input(
        "Keyboard (focus here)", value=st.session_state.keybox, key="kb",
        placeholder="w a s d / up down left right"
    )
    key = st.session_state.keybox.strip().lower()
    if key:
        mapping = {"w": (0, -1), "up": (0, -1), "s": (0, 1), "down": (0, 1),
                   "a": (-1, 0), "left": (-1, 0), "d": (1, 0), "right": (1, 0)}
        if key in mapping:
            turn(mapping[key])
        st.session_state.keybox = ""
        st.session_state.kb = ""

    st.slider("Speed (lower = faster)", 0.05, 0.40, st.session_state.speed, 0.01, key="speed")
    st.button("🔄 Restart", use_container_width=True, on_click=restart)

# -------------------- Header --------------------
st.markdown(
    """
    <style>
    .badge{display:inline-block;padding:6px 12px;border-radius:999px;color:#fff;
           font-weight:700;letter-spacing:.3px;margin-right:8px;}
    .score{background:linear-gradient(90deg,#ff6aa2,#7b5cff);}
    .state{background:linear-gradient(90deg,#00d2ff,#3a7bd5);}
    .start{background:linear-gradient(90deg,#00c853,#64dd17);}
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🐍 Snake — Streamlit Edition")
state_text = ("Game Over" if st.session_state.game_over
              else ("Running" if st.session_state.is_running else "Paused"))
st.markdown(
    f"<span class='badge score'>Score: {st.session_state.score}</span>"
    f"<span class='badge state'>{state_text}</span>",
    unsafe_allow_html=True,
)

# Start / Pause / Resume controls
ctrl = st.columns([1,1,1])
with ctrl[0]:
    st.button("🚀 Start", use_container_width=True, on_click=start_with_countdown,
              disabled=st.session_state.is_running and not st.session_state.game_over)
with ctrl[1]:
    if not st.session_state.game_over:
        if st.session_state.is_running:
            st.button("⏸ Pause", use_container_width=True,
                      on_click=lambda: st.session_state.update(is_running=False))
        else:
            st.button("▶ Resume", use_container_width=True,
                      on_click=lambda: st.session_state.update(is_running=True))

# -------------------- D-Pad Buttons --------------------
top = st.columns([1,1,1,2,1,1,1])
with top[1]:
    st.button("⬆️ Up", use_container_width=True, on_click=turn, args=((0, -1),))
row = st.columns([1,1,1,2,1,1,1])
with row[0]:
    st.button("⬅️ Left", use_container_width=True, on_click=turn, args=((-1, 0),))
with row[2]:
    st.button("➡️ Right", use_container_width=True, on_click=turn, args=((1, 0),))
with row[4]:
    st.button("⬇️ Down", use_container_width=True, on_click=turn, args=((0, 1),))

# -------------------- Countdown / Tick / Render --------------------
# Countdown overlay
if st.session_state.countdown > 0:
    board = draw_board()
    st.image(board, width=st.session_state.grid * st.session_state.cell_px)
    st.warning(f"Starting in {st.session_state.countdown}…")
    time.sleep(0.6)
    st.session_state.countdown -= 1
    if st.session_state.countdown == 0:
        st.session_state.is_running = True
    st.rerun()

# Advance one tick
if st.session_state.is_running and not st.session_state.game_over:
    step()

# Render board
board = draw_board()
st.image(board, width=st.session_state.grid * st.session_state.cell_px)

# Game over or keep running
if st.session_state.game_over:
    st.error("💥 **Game Over!** Press **Restart** or **Start** to play again.")
else:
    time.sleep(st.session_state.speed)
    st.rerun()
