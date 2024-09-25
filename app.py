import streamlit as st
import pandas as pd
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials from environment variable
FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

if FIREBASE_KEY_JSON is None:
    st.error("FIREBASE_KEY environment variable not set.")
else:
    try:
        # Parse the JSON string into a dictionary
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        # Initialize Firebase only if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        # Get Firestore client
        db = firestore.client()

        # Function to load questions from a CSV file
        def load_questions(doc_path):
            df = pd.read_csv(doc_path)
            return df['prompt'].tolist()  # Return the list of prompts

        # Main Streamlit App
        def main():
            st.title("Questionnaire Application")

            # Load questions from a CSV file
            questions = load_questions("questions.csv")  # Ensure this file is in the same directory

            # Initialize session state for answers and question index
            if 'answers' not in st.session_state:
                st.session_state.answers = []
            if 'question_index' not in st.session_state:
                st.session_state.question_index = 0

            current_index = st.session_state.question_index

            # Display the current question
            if current_index < len(questions):
                question = questions[current_index]
                answer = st.text_input(question, key=f"answer_{current_index}")

                # Submit button
                if st.button("Submit"):
                    if answer:  # Check if an answer is provided
                        st.session_state.answers.append(answer)
                        st.session_state.question_index += 1  # Move to the next question
                    else:
                        st.error("Please provide an answer before submitting.")

                # Button to go to the next question
                if st.button("Next"):
                    if answer:
                        st.session_state.question_index += 1  # Move to the next question
                    else:
                        st.error("Please provide an answer before proceeding to the next question.")

            # When all questions are answered
            if current_index >= len(questions):
                st.success("You have completed all questions!")

                # Upload all answers to Firestore
                if st.button("Upload All Answers"):
                    collection_name = os.getenv('FIREBASE_COLLECTION')
                    if collection_name is None:
                        st.error("FIREBASE_COLLECTION environment variable not set.")
                        return
                    try:
                        data = {f"question_{i + 1}": ans for i, ans in enumerate(st.session_state.answers)}
                        db.collection(collection_name).add(data)
                        st.success("All answers saved to Firebase!")
                    except Exception as e:
                        st.error(f"Error saving answers: {e}")

        if __name__ == '__main__':
            main()

    except json.JSONDecodeError:
        st.error("Error parsing FIREBASE_KEY: Invalid JSON format.")
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


