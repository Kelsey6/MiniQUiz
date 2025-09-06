# quiz_app.py
import streamlit as st
import random
from quiz_constants import QUESTIONS

# Initialize session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.credits = 0
    st.session_state.answers = []
    st.session_state.shuffled_questions = random.sample(QUESTIONS, len(QUESTIONS))
    st.session_state.show_hint = False

st.title("🧮 Mini Math Quiz")

total_qs = len(st.session_state.shuffled_questions)

# Show progress
st.progress((st.session_state.current_q) / total_qs)
st.write(f"**Question {st.session_state.current_q + 1} of {total_qs}**")

if st.session_state.current_q < total_qs:
    q = st.session_state.shuffled_questions[st.session_state.current_q]

    # Show question
    st.subheader(q["question"])
    choice = st.radio("Choose an answer:", q["options"], index=None, key=f"q{st.session_state.current_q}")

    # Hint system
    if st.button("💡 Show Hint"):
        if st.session_state.credits > 0:
            st.session_state.credits -= 1
            st.session_state.show_hint = True
        else:
            st.warning("You need at least 1 credit to view a hint!")

    if st.session_state.show_hint:
        st.info(f"Hint: {q['hint']}")

    # Submit button
    if st.button("Submit Answer"):
        if choice:
            correct = choice == q["answer"]
            if correct:
                st.success("✅ Correct!")
                st.session_state.score += 1
                st.session_state.credits += 1
            else:
                st.error(f"❌ Incorrect! The correct answer was {q['answer']}.")

            st.session_state.answers.append({
                "question": q["question"],
                "your_answer": choice,
                "correct_answer": q["answer"],
                "is_correct": correct
            })

            # Move to next question
            st.session_state.current_q += 1
            st.session_state.show_hint = False
            st.experimental_rerun()
        else:
            st.warning("Please select an answer before submitting.")

else:
    # Final results screen
    st.header("🎉 Quiz Complete!")
    st.write(f"Your final score: **{st.session_state.score} / {total_qs}**")
    st.write(f"Credits earned: **{st.session_state.credits}**")

    # Review section
    st.subheader("Review of your answers:")
    for ans in st.session_state.answers:
        if not ans["is_correct"]:
            st.write(f"❌ {ans['question']}")
            st.write(f"Your answer: {ans['your_answer']}")
            st.write(f"Correct answer: {ans['correct_answer']}")
            st.write("---")

    if st.button("Restart Quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

