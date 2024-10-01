# utils/history_with_ai.py

import streamlit as st
import json
import openai
from docx import Document
import time
import random

def read_croup_doc():
    doc = Document("croup.docx")
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return "\n".join(content).lower()

# Load the document content
croup_info = read_croup_doc()

# Set up OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_chatgpt_response(user_input):
    user_input_lower = user_input.lower()
    
    # Example croup_info dictionary
    # croup_info = {'what are symptoms': 'respiratory distress'}
    
    # List of alternative responses
    alternative_responses = [
        "I'm not sure about that.",
        "I don't have that information.",
        "That's a good question, but I don't know.",
        "I'm not certain.",
    ]

    if user_input_lower in croup_info:
        answer = croup_info[user_input_lower]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": f"The answer is: {answer}"}
            ]
        )
        return response['choices'][0]['message']['content']
    else:
        return random.choice(alternative_responses)  # Random response from the list


def run_virtual_patient():
    st.title("Virtual Patient: Case #1")

    st.info(
        "You will have the opportunity to perform a history and ask for important physical examination details. "
        "You will be limited to 15 minutes. Alternatively, you may end the session."
    )

    # Initialize start_time only if it's not already set
    if 'start_time' not in st.session_state or st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # Calculate elapsed time
    elapsed_time = (time.time() - st.session_state.start_time) / 60

    # Display patient information
    if elapsed_time < 15:
        with st.form("question_form"):
            user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
            submit_button = st.form_submit_button("Submit")

            if submit_button and user_input:
                virtual_patient_response = get_chatgpt_response(user_input)
                st.write(f"Virtual Patient: {virtual_patient_response}")
    else:
        st.warning("Session time is up. Please end the session.")
        if st.button("End Session"):
            st.session_state.start_time = None  # Reset start_time only when ending session
            st.session_state.page = "Focused Physical Examination"
            st.success("Session ended. You can start a new session.")

    # Option to move to a new screen
    if st.button("End Session"):
        st.session_state.start_time = None
        st.session_state.page = "Focused Physical Examination"
        st.rerun()
        st.write("Redirecting to a new screen...")


