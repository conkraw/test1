import streamlit as st
import json
import openai
from docx import Document
import time
import random
from utils.session_management import collect_session_data  #######NEED THIS
from utils.firebase_operations import upload_to_firebase  

def read_croup_doc():
    doc = Document("croup.docx")
    croup_info = {}
    for para in doc.paragraphs:
        # Assuming each paragraph contains a question and an answer separated by a colon
        if ':' in para.text:
            question, answer = para.text.split(':', 1)
            croup_info[question.strip().lower()] = answer.strip().lower()
    return croup_info

# Load the document content
croup_info = read_croup_doc()

def get_chatgpt_response(user_input):
    user_input_lower = user_input.lower()
    
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

        
def run_virtual_patient(db):
    st.title("Virtual Patient: Case #1")

    st.info(
        "You will have the opportunity to perform a history and ask for important physical examination details. "
        "You will be limited to 15 minutes. Alternatively, you may end the session."
    )

    # Initialize start_time only if it's not already set
    if 'start_time' not in st.session_state or st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # Initialize session data for storing questions
    if 'session_data' not in st.session_state:
        st.session_state.session_data = {
            'questions_asked': []
        }

    # Calculate elapsed time
    elapsed_time = (time.time() - st.session_state.start_time) / 60

    # Display patient information
    if elapsed_time < 15:
        with st.form("question_form"):
            user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
            submit_button = st.form_submit_button("Submit")

            if submit_button and user_input:
                # Store the user question in the session data
                st.session_state.session_data['questions_asked'].append(user_input)

                # Get the virtual patient's response
                virtual_patient_response = get_chatgpt_response(user_input)
                st.write(f"Virtual Patient: {virtual_patient_response}")

                # Display the questions asked so far
                st.write("Questions asked so far:")
                for question in st.session_state.session_data['questions_asked']:
                    st.write(f"- {question}")

                # Collect session data and upload to Firebase upon submission
                session_data = collect_session_data()  # Collect session data
                session_data['questions_asked'] = st.session_state.session_data['questions_asked']
                upload_message = upload_to_firebase(db, session_data)  # Upload to Firebase
                st.success("Your questions have been saved successfully.")

    else:
        st.warning("Session time is up. Please end the session.")

    # End session button
    if st.button("End Session"):
        # Collect session data and upload to Firebase upon ending session
        session_data = collect_session_data()  # Collect session data
        session_data['questions_asked'] = st.session_state.session_data['questions_asked']
        upload_message = upload_to_firebase(db, session_data)  # Upload to Firebase
        st.success("Your questions have been saved successfully.")

        st.session_state.start_time = None  # Reset start_time
        st.session_state.page = "Focused Physical Examination"
        st.write("Session ended. You can start a new session.")
        st.rerun()

