import streamlit as st
import random
from quiz_constants import QUESTIONS

def initialize_session_state():
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = QUESTIONS.copy()
        random.shuffle(st.session_state.questions)
    if 'show_next' not in st.session_state:
        st.session_state.show_next = False
    if 'wrong_questions' not in st.session_state:
        st.session_state.wrong_questions = []

def check_answer():
    selected_answer = st.session_state.user_answer
    current_q = st.session_state.questions[st.session_state.current_question]
    
    if selected_answer == current_q['correct_answer']:
        st.success('Correct! 🎉')
        st.session_state.score += 1
    else:
        st.error(f'Sorry, that\'s incorrect. The correct answer was: {current_q["correct_answer"]}')
        st.session_state.wrong_questions.append({
            'question': current_q['question'],
            'your_answer': selected_answer,
            'correct_answer': current_q['correct_answer']
        })
    
    st.session_state.show_next = True

def next_question():
    st.session_state.current_question += 1
    st.session_state.show_next = False

def main():
    st.title('Math Quiz App')
    initialize_session_state()
    
    total_questions = len(st.session_state.questions)
    current_q_num = st.session_state.current_question + 1
    
    # --- Check if quiz is complete first ---
    if st.session_state.current_question >= total_questions:
        st.progress(1.0)  # show full bar
        st.success(f'Quiz Complete! You scored {st.session_state.score} out of {total_questions}!')
        
        if st.session_state.wrong_questions:
            st.write('Questions you got wrong:')
            for q in st.session_state.wrong_questions:
                with st.expander(q['question']):
                    st.write(f'Your answer: {q["your_answer"]}')
                    st.write(f'Correct answer: {q["correct_answer"]}')
        
        if st.button('Restart Quiz'):
            st.session_state.clear()
            st.experimental_rerun()
        return
    
    # --- Show progress bar only during quiz ---
    progress = st.session_state.current_question / total_questions
    st.progress(progress)
    st.write(f'Question {current_q_num} of {total_questions}')
    
    # Display current question
    current_q = st.session_state.questions[st.session_state.current_question]
    st.write('### ' + current_q['question'])
    
    # Show hint button
    if 'hint' in current_q:
        if st.button('Show Hint'):
            st.info(current_q['hint'])
    
    # Answer selection
    st.radio(
        'Choose your answer:',
        options=current_q['choices'],
        key='user_answer'
    )
    
    # Submit answer button
    if not st.session_state.show_next:
        st.button('Submit Answer', on_click=check_answer)
    else:
        st.button('Next Question', on_click=next_question)

if __name__ == '__main__':
    main()
