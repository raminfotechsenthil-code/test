# funny_quiz.py
import random
import streamlit as st

st.set_page_config(page_title="😂 Funny Quiz App", page_icon="🎉", layout="centered")
st.title("😂 Funny Quiz App")

# ---- compatibility: rerun for all versions ----
def do_rerun():
    # Prefer new API; fall back if running an older Streamlit
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()  # type: ignore[attr-defined]

# -------------------- Questions --------------------
def get_questions():
    return [
        {"q": "What does CPU stand for?",
         "options": ["Central Pizza Unit","Central Processing Unit","Computer Power Utility","Chief Ping Utility"],
         "answer": "Central Processing Unit",
         "lol": "Sadly, it does not bake pizzas. 🍕",
         "hint": "It's the brain of the computer."},
        {"q": "Which animal is famous on the internet for being grumpy?",
         "options": ["Happy Hippo","Grumpy Cat","Moody Moose","Angry Ant"],
         "answer": "Grumpy Cat",
         "lol": "RIP legend. 😾",
         "hint": "Feline and famous."},
        {"q": "In Python, what does print('😎') do?",
         "options": ["Prints a receipt","Prints 😎 to the screen","Orders sunglasses","Turns on dark mode"],
         "answer": "Prints 😎 to the screen",
         "lol": "No free sunglasses included. 🕶️",
         "hint": "Output goes to the terminal."},
        {"q": "Which key closes a dialog most often?",
         "options": ["Enter","Escape","Space","Caps Lock"],
         "answer": "Escape",
         "lol": "Also useful for awkward chats. 🏃‍♂️",
         "hint": "Think: run away!"},
        {"q": "Which of these is NOT a programming language?",
         "options": ["Python","Java","HTML","BananaScript"],
         "answer": "BananaScript",
         "lol": "Though I'd love to import smoothie. 🍌",
         "hint": "One is very… fruity."},
        {"q": "What does RAM stand for?",
         "options": ["Random Access Memory","Rapid Access Module","Really Awesome Machine","Read And Mail"],
         "answer": "Random Access Memory",
         "lol": "Short-term memory of your PC. 🧠",
         "hint": "It forgets on restart."},
        {"q": "What’s the best way to debug?",
         "options": ["Rubber duck talk","Guessing wildly","Turning monitor off","Changing font size"],
         "answer": "Rubber duck talk",
         "lol": "Explain it to a duck. 🦆",
         "hint": "Quacky technique."},
    ]

# -------------------- State --------------------
ss = st.session_state
if "order" not in ss:
    qs = get_questions()
    ss.order = list(range(len(qs)))
    random.shuffle(ss.order)
    ss.i = 0
    ss.score = 0
    ss.finished = False
    ss.opts = {}  # per-question shuffled options stored once

PLACEHOLDER = "— Select an answer —"

def get_q_and_opts(i):
    qs = get_questions()
    q = qs[ss.order[i]]
    if i not in ss.opts:
        opts = q["options"][:]
        random.shuffle(opts)
        ss.opts[i] = opts
    return q, ss.opts[i]

# -------------------- UI --------------------
if ss.finished:
    st.success(f"Done! You scored **{ss.score} / {len(ss.order)}** 🎯")
    if st.button("Play again 🔁"):
        ss.clear()
        do_rerun()
else:
    q, opts = get_q_and_opts(ss.i)
    st.subheader(f"Q{ss.i+1}. {q['q']}")
    st.progress(ss.i / len(ss.order))

    choice = st.radio(
        "Choose one:",
        [PLACEHOLDER] + opts,
        index=0,
        key=f"choice_{ss.i}",
    )

    c1, c2, c3 = st.columns(3)
    if c1.button("Hint 💡"):
        st.info(q["hint"])

    if c2.button("Submit ✅"):
        if choice == PLACEHOLDER:
            st.warning("Please select an option first.")
        else:
            if choice == q["answer"]:
                ss.score += 1
                st.success("Correct! 🎉 " + q["lol"])
            else:
                st.error(f"Oops! The answer is **{q['answer']}**. {q['lol']}")
            ss.i += 1
            if ss.i >= len(ss.order):
                ss.finished = True
            do_rerun()

    if c3.button("Skip ⏭️"):
        ss.i += 1
        if ss.i >= len(ss.order):
            ss.finished = True
        do_rerun()

st.caption("If you prefer, you can simply replace all calls to experimental_rerun() with rerun().")
