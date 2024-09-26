import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json
import openai
from docx import Document
import time

# Load Firebase credentials from Streamlit secrets
FIREBASE_KEY_JSON = st.secrets["FIREBASE_KEY"]

if FIREBASE_KEY_JSON:
    try:
        # Parse the JSON string into a dictionary
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        # Initialize Firebase only if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        # Get Firestore client
        db = firestore.client()

        # Function to read the croup document
        def read_croup_doc():
            doc = Document("croup.docx")
            content = []
            for para in doc.paragraphs:
                content.append(para.text)
            return "\n".join(content).lower()  # Convert to lower case for easier matching

        # Load the document content
        croup_info = read_croup_doc()

        # Set up OpenAI API key from Streamlit secrets
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        # Function to get response from ChatGPT
        def get_chatgpt_response(user_input):
            user_input_lower = user_input.lower()  # Normalize the user input to lower case
            
            # Define common greetings and empathetic responses
            greetings = ["how are you", "how is your child", "how do you feel"]
            empathetic_responses = ["i am sorry to hear that", "that must be tough", "i understand your concern"]
            
            if any(greet in user_input_lower for greet in greetings):
                return "I'm feeling a bit distressed; my child is having difficulty breathing."

            if any(empathetic in user_input_lower for empathetic in empathetic_responses):
                return "Thank you for your concern. It's been really stressful for me."

            # Check if the question is in the croup_info
            if user_input_lower in croup_info:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": "You are a parent whose child is experiencing croup. Answer the history questions as a parent would. You will be asked physical examination questions, please provide the findings as a doctor would."}
                    ]
                )
                return response['choices'][0]['message']['content']
            else:
                return "I don't know."

        # Function to upload data to Firebase
        def upload_to_firebase(question, response):
            entry = {'question': question, 'response': response}
            db.collection('virtual_patient_sessions').add(entry)  # Change to your collection name

        # Streamlit app layout
        st.title("Virtual Patient: Croup")

        # Instructions for the user
        st.info(
            "You will have the opportunity to perform a history and ask for important physical examination details using a virtual patient/parent. "
            "When you are ready, please start asking questions. You will be limited to 15 minutes. "
            "Alternatively, you may end the session if you click end."
        )

        # Session state to track time and session status
        if 'start_time' not in st.session_state:
            st.session_state.start_time = time.time()

        # Calculate elapsed time
        elapsed_time = (time.time() - st.session_state.start_time) / 60  # Convert to minutes

        # Display patient information
        if elapsed_time < 15:
            with st.form("question_form"):
                user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
                submit_button = st.form_submit_button("Submit")

                if submit_button and user_input:
                    virtual_patient_response = get_chatgpt_response(user_input)
                    st.write(f"Virtual Patient: {virtual_patient_response}")

                    # Upload the question and response to Firebase without announcement
                    upload_to_firebase(user_input, virtual_patient_response)

        else:
            st.warning("Session time is up. Please end the session.")
            if st.button("End Session"):
                st.session_state.start_time = None
                st.success("Session ended. You can start a new session.")

        # Option to move to a new screen
        if st.button("Go to New Screen"):
            st.session_state.start_time = None
            st.write("Redirecting to a new screen...")

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
else:
    st.error("FIREBASE_KEY environment variable not set.")



