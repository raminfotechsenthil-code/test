# funny_python_quiz_extra_fixed.py
# Super Funny Python Quiz 🐍🤣 with jokes + colorful UI (uses st.rerun)

import streamlit as st
from random import shuffle

st.set_page_config(page_title="Super Funny Python Quiz 🐍🤣", page_icon="🐍", layout="centered")

# ===== CSS for colorful theme =====
st.markdown("""
<style>
  .stApp {
    background: linear-gradient(135deg, #ff9a9e, #fad0c4, #fbc2eb, #a1c4fd) fixed;
  }
  .quiz-card {
    background: rgba(255,255,255,0.9);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
  }
  .stButton button {
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
  }
  div[role="radiogroup"] label {
    background: rgba(255,255,255,0.82);
    border-radius: 12px;
    padding: 8px 10px;
    margin: 4px 0;
    border: 1px solid rgba(0,0,0,0.06);
  }
</style>
""", unsafe_allow_html=True)

st.title("🐍🤣 Super Funny Python Quiz 🎉🎭")
st.caption("Answer these silly Python questions. Warning: jokes included 🙈")

# ===== Questions =====
QUESTIONS = [
    {
        "q": "Why is Python called Python?",
        "options": [
            "Because the creator loved snakes 🐍",
            "Because Monty Python made him laugh 🤡",
            "Because it sounded cooler than 'BananaLang' 🍌",
            "Because Java was already taken ☕"
        ],
        "answer": "Because Monty Python made him laugh 🤡",
        "gag": "✅ Correct! Imagine if it was called BananaLang 🍌🤣",
        "oops": "❌ Nope! Snakes don’t code (yet). 🐍💻",
    },
    {
        "q": "What happens if you type `import this` in Python?",
        "options": [
            "It prints Zen of Python ✨",
            "It imports happiness 😍",
            "It deletes Windows system32 😱",
            "It summons a real snake 🐍"
        ],
        "answer": "It prints Zen of Python ✨",
        "gag": "✅ Correct! Simple is better than complex… except pizza 🍕",
        "oops": "❌ Nope! Your PC is safe (for now) 😅",
    },
    {
        "q": "Which of these is NOT a Python data type?",
        "options": ["list", "dict", "tuple", "TikTokDance 💃"],
        "answer": "TikTokDance 💃",
        "gag": "✅ Correct! TikTokDance is only supported in JavaScript 😂",
        "oops": "❌ Oops! No dancing in Python, only indentation 🪄",
    },
    {
        "q": "What does `print('hello' * 3)` output?",
        "options": ["hellohellohello", "333", "Error 💥", "It calls your mom ☎️"],
        "answer": "hellohellohello",
        "gag": "✅ Correct! Python multiplies words better than a parrot 🦜",
        "oops": "❌ Wrong! But don’t worry, your mom still loves you ❤️",
    },
    {
        "q": "Which keyword defines a function in Python?",
        "options": ["func", "define", "def", "abracadabra ✨"],
        "answer": "def",
        "gag": "✅ Correct! But admit it, `abracadabra` would be cooler 🪄",
        "oops": "❌ Wrong! Python isn’t that magical 🧙‍♂️",
    },
]

N = len(QUESTIONS)

# ===== State =====
def init_state():
    st.session_state.q_index = 0
    st.session_state.answers = [None] * N
    st.session_state.locked = [False] * N
    st.session_state.finished = False
    st.session_state.shuffled = []
    for q in QUESTIONS:
        opts = q["options"][:]
        shuffle(opts)
        st.session_state.shuffled.append(opts)

if "answers" not in st.session_state:
    init_state()

q_idx = st.session_state.q_index

def compute_score():
    return sum(1 for i, a in enumerate(st.session_state.answers) if a == QUESTIONS[i]["answer"])

def lock_answer(choice):
    st.session_state.answers[q_idx] = choice
    st.session_state.locked[q_idx] = True

# ===== Quiz =====
if not st.session_state.finished:
    st.progress(q_idx / N)
    q = QUESTIONS[q_idx]
    st.markdown(f"<div class='quiz-card'><h3>Q{q_idx+1}: {q['q']}</h3></div>", unsafe_allow_html=True)

    options = st.session_state.shuffled[q_idx]

    # maintain previous selection if any
    if st.session_state.answers[q_idx] in options:
        default_index = options.index(st.session_state.answers[q_idx])
    else:
        default_index = 0

    choice_ans = st.radio(
        "Pick one:",
        options,
        index=default_index,
        disabled=st.session_state.locked[q_idx],
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Back", disabled=(q_idx == 0)):
            st.session_state.q_index -= 1
            st.rerun()
    with col2:
        if st.button("🔒 Lock", disabled=st.session_state.locked[q_idx]):
            lock_answer(choice_ans)
            if choice_ans == q["answer"]:
                st.success(q["gag"])
            else:
                st.error(q["oops"])
    with col3:
        if q_idx < N - 1:
            if st.button("➡️ Next", disabled=not st.session_state.locked[q_idx]):
                st.session_state.q_index += 1
                st.rerun()
        else:
            if st.button("🏁 Submit", disabled=not st.session_state.locked[q_idx]):
                st.session_state.finished = True
                st.rerun()

else:
    score = compute_score()
    st.balloons()
    st.header("🎊 Quiz Finished 🎊")
    st.success(f"Your score: **{score}/{N}**")

    if score == N:
        st.write("🐍 You’re a Python Rockstar! import fame ⭐")
    elif score >= N // 2:
        st.write("👍 Nice job! Not perfect, but you can still `pip install coffee` ☕")
    else:
        st.write("😅 That was… something. Go hug a Python book 📖🐍")

    st.subheader("Review 📋")
    for i, q in enumerate(QUESTIONS):
        user = st.session_state.answers[i]
        correct = q["answer"]
        ok = (user == correct)
        st.markdown(f"**Q{i+1}. {q['q']}**  {'✅' if ok else '❌'}")
        st.write(f"Your answer: **{user if user else '—'}**")
        st.write(f"Correct: **{correct}**")
        st.write("")

    if st.button("🔄 Restart"):
        init_state()
        st.rerun()
