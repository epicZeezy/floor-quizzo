import os
import streamlit as st
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()

# Set page config
st.set_page_config(page_title="Image Trivia Flashcards", layout="centered")

# Load CSV file
@st.cache_data
def load_data():
    return pd.read_csv("brunch_floor_quiz.csv")

st.title("The Floor Quizzo")


df = load_data()

# Initialize session state
if "index" not in st.session_state:
    st.session_state.index = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "answered_question" not in st.session_state:
    st.session_state.answered_question = False

st.session_state.answer_input = ""

# Reset if index out of bounds
if st.session_state.index >= len(df):
    st.success("Game Over!")
else:
    row = df.iloc[st.session_state.index]

    # Show image and image description
    st.image(row["image_url"], use_container_width=True)
    st.markdown(f"**Trivia:** {row['image_trivia_question']}")
    answer_form = st.form(key="answer_form", clear_on_submit=True)
    answer_input = answer_form.text_input("Submit your answer here")
    submit_button = answer_form.form_submit_button(label="Submit")
    
    # TODO: Have AI read image description automatically so no clicks are needed. Cache audio description locally so you don't always call model

    if submit_button:
        # TODO: Have better way to check for answers using fuzzy matching. Add callback for submit button instead
        if answer_input.strip().lower() == row["answer"].strip().lower():
            st.success("Correct!")
            st.session_state.answered_question = True
        else:
            st.error(f"Incorrect! The correct answer is {row['answer']}. Not {answer_input}.")
            st.session_state.answered_question = True
    
    # Move to next question
    if st.session_state.answered_question:
        if st.button("Next"):
            st.session_state.index += 1
            st.session_state.answered_question = False
            st.rerun()
    
    # TODO: Print out total score
