import streamlit as st
import json
import os
import random
import time

# Questions
questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Mumbai", "Delhi", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which language is used for AI?",
        "options": ["Python", "HTML", "CSS", "C"],
        "answer": "Python"
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    }
]

# Shuffle questions
random.shuffle(questions)

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)

# UI Improvements
st.title("🧠 Ultimate Quiz Challenge")
st.markdown("### Test your knowledge and climb the leaderboard 🚀")

name = st.text_input("Enter your name:")

# Timer start
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Store answers
if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)

# Show questions (NO PRESELECTED OPTION)
for i, q in enumerate(questions):
    st.session_state.answers[i] = st.radio(
        q["question"],
        ["-- Select an option --"] + q["options"],  # placeholder
        key=f"q{i}"
    )

if st.button("Submit"):
    if not name:
        st.warning("Please enter your name!")
    else:
        score = 0

        for i, q in enumerate(questions):
            if st.session_state.answers[i] == q["answer"]:
                score += 1

        # Timer end
        end_time = time.time()
        time_taken = int(end_time - st.session_state.start_time)

        st.success(f"Your Score: {score}/{len(questions)}")
        st.info(f"⏱️ Time taken: {time_taken} seconds")

        # Show correct answers
        st.subheader("📘 Review Answers")
        for i, q in enumerate(questions):
            if st.session_state.answers[i] == q["answer"]:
                st.write(f"✅ {q['question']} → {q['answer']}")
            else:
                st.write(f"❌ {q['question']}")
                st.write(f"Correct Answer: {q['answer']}")

        # Save leaderboard
        leaderboard = load_leaderboard()
        leaderboard.append({"name": name, "score": score})

        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)
        save_leaderboard(leaderboard)

# Leaderboard
st.subheader("🏆 Leaderboard")
leaderboard = load_leaderboard()

if leaderboard:
    st.success(f"👑 Top Player: {leaderboard[0]['name']}")

for i, entry in enumerate(leaderboard[:5]):
    st.write(f"{i+1}. {entry['name']} - {entry['score']}")