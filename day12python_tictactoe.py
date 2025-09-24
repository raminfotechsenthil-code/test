# tic_tac_toe_tn_tournament.py
# Tic-Tac-Toe ❌⭕ — Tamil Nadu Theme + 10-Round Tournament with Final Report
# Run: streamlit run tic_tac_toe_tn_tournament.py

import random
import csv
import io
import streamlit as st

st.set_page_config(page_title="Tic-Tac-Toe — TN Tournament", page_icon="🪷", layout="centered")

# -------------------- THEME --------------------
TN_COLORS = {
    "bg_grad": "linear-gradient(135deg, #7b1e1e 0%, #ff9933 45%, #2e7d32 85%)",
    "card": "#fffaf0",
    "accent": "#d4af37",
    "maroon": "#7b1e1e",
    "saffron": "#ff9933",
    "green": "#2e7d32",
    "win": "#c8f7c5",
    "draw": "#ffe8b3",
}

st.markdown(f"""
<style>
.tn-header {{
  background: {TN_COLORS['bg_grad']};
  padding: 16px 18px; border-radius: 18px; color: #fff;
  font-weight: 800; letter-spacing: .3px;
  box-shadow: 0 8px 22px rgba(0,0,0,.12);
  border: 2px solid {TN_COLORS['accent']};
}}
.tn-card {{
  background: {TN_COLORS['card']};
  border: 2px solid {TN_COLORS['accent']};
  border-radius: 16px; padding: 12px 14px;
  box-shadow: 0 8px 20px rgba(0,0,0,.06);
}}
div.stButton > button {{
  border: 2px solid {TN_COLORS['accent']};
  background: #ffffff; color: {TN_COLORS['maroon']};
  font-weight: 800; border-radius: 12px; height: 64px; font-size: 28px;
}}
div.stButton > button:hover {{ background: #fff6e6; border-color: {TN_COLORS['saffron']}; }}
button[kind="primary"] {{ background: {TN_COLORS['green']}; color: #ffffff !important; border: 0; }}
.cellbox {{
  display:flex; align-items:center; justify-content:center;
  height:74px; font-size:40px; font-weight:900;
  border-radius:14px; border:2px solid {TN_COLORS['accent']};
  background:#ffffff;
}}
.win {{ background: {TN_COLORS['win']} !important; }}
.draw {{ background: {TN_COLORS['draw']} !important; }}
.status {{
  display:inline-block; padding:8px 12px; border-radius:999px;
  background:#fff; border:2px solid {TN_COLORS['accent']};
  font-weight:800; color:{TN_COLORS['maroon']};
}}
.kpi {{
  display:inline-block; padding:8px 14px; border-radius:12px;
  background:#fff; border:2px solid {TN_COLORS['accent']};
  font-weight:900; color:{TN_COLORS['maroon']}; margin-right:8px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="tn-header">🪷 Tic-Tac-Toe — Tamil Nadu Tournament (10 Rounds)</div>', unsafe_allow_html=True)
st.caption("Maroon • Saffron • Leaf-Green • Temple-Gold | Kolam-style accents | தமிழ் / English UI")

# -------------------- LANGUAGE --------------------
LANG = st.sidebar.radio("Language / மொழி", ["English", "தமிழ்"], index=1)
def T(en, ta): return ta if LANG == "தமிழ்" else en

# -------------------- SETTINGS --------------------
st.sidebar.subheader(T("Settings", "அமைப்புகள்"))
mode = st.sidebar.radio(
    T("Mode", "விளையாட்டு முறை"),
    [T("Two Players", "இருவர்"), T("Vs Computer (random)", "கணினி எதிர் (random)")]
)
human_plays = st.sidebar.radio(
    T("If vs Computer, you play as", "கணினி எதிரில் நீங்கள் ஆடும் அடையாளம்"),
    ["X", "O"],
    index=0,
    format_func=lambda s: ("❌ X" if s=="X" else "⭕ O")
)

# -------------------- CONSTANTS --------------------
X, O, EMPTY = "X", "O", ""
TOTAL_ROUNDS = 10

# -------------------- STATE INIT --------------------
def init_single_game():
    st.session_state.board = [EMPTY]*9
    st.session_state.turn = X
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.winning_line = []
    st.session_state.status = T("Game on!", "விளையாட்டு தொடங்கியது!")

def init_tournament():
    st.session_state.current_round = 1
    st.session_state.results = []  # list of dicts per round
    st.session_state.x_wins = 0
    st.session_state.o_wins = 0
    st.session_state.draws = 0
    init_single_game()

if "current_round" not in st.session_state:
    init_tournament()

# -------------------- GAME LOGIC --------------------
def lines():
    rows = [[(r,0),(r,1),(r,2)] for r in range(3)]
    cols = [[(0,c),(1,c),(2,c)] for c in range(3)]
    diags = [[(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]]
    return rows + cols + diags

def idx(rc): r,c = rc; return r*3+c

def check_winner(board):
    for line in lines():
        a,b,c = [board[idx(p)] for p in line]
        if a!=EMPTY and a==b==c:
            return a, line
    return None, []

def board_full(board): return all(v!=EMPTY for v in board)
def sym_to_emoji(s): return "❌" if s=="X" else ("⭕" if s=="O" else " ")

def place(i, sym):
    if st.session_state.game_over: return False
    if st.session_state.board[i]==EMPTY:
        st.session_state.board[i]=sym
        return True
    return False

def after_move():
    w, line = check_winner(st.session_state.board)
    if w:
        st.session_state.game_over=True
        st.session_state.winner=w
        st.session_state.winning_line=line
        st.session_state.status = (T("wins!", "வெற்றி!") + f" {sym_to_emoji(w)}")
        record_round_result()
        return
    if board_full(st.session_state.board):
        st.session_state.game_over=True
        st.session_state.winner=None
        st.session_state.winning_line=[]
        st.session_state.status = T("It's a draw!", "டிரா!")
        record_round_result()
        return
    st.session_state.turn = O if st.session_state.turn==X else X
    st.session_state.status = T("to move", "ஆட வேண்டியது") + f" {sym_to_emoji(st.session_state.turn)}"

def record_round_result():
    # Count moves
    move_count = sum(1 for v in st.session_state.board if v in (X,O))
    flat_board = "".join(st.session_state.board)  # snapshot
    # Update counters
    if st.session_state.winner == X:
        st.session_state.x_wins += 1
        outcome = "X"
    elif st.session_state.winner == O:
        st.session_state.o_wins += 1
        outcome = "O"
    else:
        st.session_state.draws += 1
        outcome = "Draw"

    st.session_state.results.append({
        "round": st.session_state.current_round,
        "outcome": outcome,
        "moves": move_count,
        "board": flat_board,
        "winning_line": st.session_state.winning_line
    })

# -------------------- HEADER INFO --------------------
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi">🎯 {T("Round", "சுற்று")}: {st.session_state.current_round} / {TOTAL_ROUNDS}</div>', unsafe_allow_html=True)
k2.markdown(f'<div class="kpi">❌ X: {st.session_state.x_wins}</div>', unsafe_allow_html=True)
k3.markdown(f'<div class="kpi">⭕ O: {st.session_state.o_wins}</div>', unsafe_allow_html=True)
k4.markdown(f'<div class="kpi">🤝 {T("Draws","டிரா")}: {st.session_state.draws}</div>', unsafe_allow_html=True)

# -------------------- CONTROLS --------------------
cA, cB = st.columns(2)
if cA.button(T("Reset Game (current round)", "இந்த சுற்று ரீசெட்") + " 🔄"):
    init_single_game()
    st.rerun()
if cB.button(T("Reset Tournament (all 10 rounds)", "முழு 10 சுற்று ரீசெட்") + " 🧹"):
    init_tournament()
    st.rerun()

# -------------------- STATUS --------------------
st.subheader(T("Status", "நிலை"))
st.markdown(f'<div class="status">{sym_to_emoji(st.session_state.turn)} {st.session_state.status}</div>', unsafe_allow_html=True)
st.write("")

# -------------------- GAME ACTIVE? --------------------
tournament_over = st.session_state.current_round > TOTAL_ROUNDS

# -------------------- GRID --------------------
clicked = None
if not tournament_over:
    for r in range(3):
        cols = st.columns(3, gap="small")
        for c in range(3):
            i = r*3+c
            label = sym_to_emoji(st.session_state.board[i]) if st.session_state.board[i] else " "
            disabled = st.session_state.game_over or st.session_state.board[i]!=EMPTY
            if cols[c].button(label, key=f"cell-{st.session_state.current_round}-{i}", use_container_width=True, disabled=disabled):
                clicked = i

# Handle human click
if not tournament_over and clicked is not None:
    if place(clicked, st.session_state.turn):
        after_move()
        # Computer random move if applicable
        if (mode.startswith("Vs") or mode.startswith("கணினி")) and not st.session_state.game_over:
            if st.session_state.turn != human_plays:
                empties = [i for i,v in enumerate(st.session_state.board) if v==EMPTY]
                if empties:
                    comp_i = random.choice(empties)
                    place(comp_i, st.session_state.turn)
                    after_move()

# -------------------- FINAL BOARD + NEXT ROUND --------------------
if st.session_state.game_over and not tournament_over:
    st.markdown(T("### Final Board (This Round)", "### இந்த சுற்றின் இறுதி பலகை"))
    win_cells = set(idx(p) for p in st.session_state.winning_line)

    css_class = "draw" if st.session_state.winner is None else ""
    for r in range(3):
        cols = st.columns(3, gap="small")
        for c in range(3):
            i = r*3+c
            val = sym_to_emoji(st.session_state.board[i]) if st.session_state.board[i] else " "
            klass = "cellbox win" if i in win_cells else f"cellbox {css_class}"
            cols[c].markdown(f'<div class="{klass}">{val}</div>', unsafe_allow_html=True)

    # Next Round button
    def next_round():
        st.session_state.current_round += 1
        init_single_game()
    st.button(T("Next Round ▶️", "அடுத்த சுற்று ▶️"), type="primary", on_click=next_round)

# -------------------- TOURNAMENT OVER? SHOW REPORT --------------------
if tournament_over:
    st.markdown("## 🏁 " + T("Tournament Finished — Final Report", "டூர்ணமெண்ட் முடிந்தது — இறுதி அறிக்கை"))

    x, o, d = st.session_state.x_wins, st.session_state.o_wins, st.session_state.draws
    total = x + o + d if (x+o+d)>0 else 1
    champ = T("Draw (Tie)", "டிரா (சமநிலை)")
    if x > o: champ = "❌ X"
    elif o > x: champ = "⭕ O"

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="kpi">❌ X Wins: {x} ({x*100//total}%)</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi">⭕ O Wins: {o} ({o*100//total}%)</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi">🤝 {T("Draws","டிரா")}: {d} ({d*100//total}%)</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi">🏆 {T("Champion","சாம்பியன்")}: {champ}</div>', unsafe_allow_html=True)

    # Round-wise table
    st.markdown("### " + T("Round-wise Results", "சுற்று வாரியான முடிவுகள்"))
    # Build a small readable table
    def board_pretty(b):  # b is "XXO...O"
        return " | ".join([b[i] or "-" for i in range(9)])
    rows = []
    for r in st.session_state.results:
        wl = ",".join([f"({a},{b})" for (a,b) in r["winning_line"]]) if r["winning_line"] else "-"
        rows.append({
            T("Round","சுற்று"): r["round"],
            T("Outcome","முடிவு"): r["outcome"],
            T("Moves","நடவடிக்கை"): r["moves"],
            T("Winning Line","வெற்றி வரி"): wl,
            T("Board (r1-3,c1-3)","பலகை"): board_pretty(r["board"])
        })
    st.dataframe(rows, use_container_width=True)

    # CSV download
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(["round","outcome","moves","winning_line","board"])
    for r in st.session_state.results:
        wl = ";".join([f"{a}-{b}" for (a,b) in r["winning_line"]]) if r["winning_line"] else ""
        writer.writerow([r["round"], r["outcome"], r["moves"], wl, r["board"]])
    st.download_button(
        label=T("Download Final Report (CSV)", "இறுதி அறிக்கை பதிவிறக்கு (CSV)"),
        data=csv_buf.getvalue().encode("utf-8"),
        file_name="tictactoe_tournament_report.csv",
        mime="text/csv",
        use_container_width=True
    )

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(T(
    "Tip: Switch தமிழ் / English from the sidebar. Reset just this round or the whole tournament anytime.",
    "குறிப்பு: பக்கப்பட்டியில் தமிழ் / English மாற்றலாம். இந்த சுற்றை மட்டும் அல்லது முழு 10 சுற்றையும் ரீசெட் செய்யலாம்."
))
