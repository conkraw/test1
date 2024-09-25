import streamlit as st
import pandas as pd
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from docx import Document

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

        # Function to load questions from a Word document
        def load_questions(doc_path):
            doc = Document(doc_path)
            questions = [p.text for p in doc.paragraphs if p.text]
            return questions

        # Main Streamlit App
        def main():
            st.title("Questionnaire Application")

            # Load questions from a Word document
            questions = load_questions("questions.docx")  # Ensure this file is in the same directory

            # Initialize session state for answers and question index
            if 'answers' not in st.session_state:
                st.session_state.answers = []
            if 'diagnoses' not in st.session_state:
                st.session_state.diagnoses = []
            if 'question_index' not in st.session_state:
                st.session_state.question_index = 0

            current_index = st.session_state.question_index

            # Display the current question
            if current_index < len(questions):
                question = questions[current_index]

                # Handle the first prompt with a larger text area
                if current_index == 0:
                    answer = st.text_area(question, key=f"answer_{current_index}", height=150)

                # Handle the second prompt with five separate inputs for diagnoses
                elif current_index == 1:
                    diagnoses = []
                    for i in range(5):
                        diagnosis = st.text_input(f"Diagnosis {i + 1}:", key=f"diagnosis_{i}")
                        diagnoses.append(diagnosis)
                    answer = diagnoses

                else:
                    answer = st.text_input(question, key=f"answer_{current_index}")

                # Button to go to the next question
                if st.button("Next"):
                    if current_index == 1:  # For the second question, check all diagnoses
                        if all(diagnosis for diagnosis in answer):
                            st.session_state.diagnoses = answer  # Store the diagnoses
                            st.session_state.question_index += 1  # Move to the next question
                            st.success("Diagnoses recorded! Click Next for the next question.")
                        else:
                            st.error("Please provide all 5 diagnoses before proceeding.")
                    else:
                        if answer:  # Check if an answer is provided for other questions
                            st.session_state.answers.append(answer)
                            st.session_state.question_index += 1  # Move to the next question
                            st.success("Answer recorded! Click Next for the next question.")
                        else:
                            st.error("Please provide an answer before proceeding to the next question.")

            # When all questions are answered
            if current_index >= len(questions):
                st.success("You have completed all questions!")

                # Create and display a 6x6 table
                if st.session_state.diagnoses:
                    diagnosis_columns = ["Historical Facts"] + st.session_state.diagnoses
                    diagnosis_df = pd.DataFrame(columns=diagnosis_columns)

                    # Add 5 blank rows for user input
                    for i in range(5):
                        diagnosis_df.loc[i] = [""] + [""] * 5  # One blank row with Historical Facts and five blank columns

                    # Display the table with text input in each cell
                    for i in range(5):
                        for j in range(len(diagnosis_columns)):
                            diagnosis_df.iloc[i, j] = st.text_input(f"Cell ({i+1}, {j+1})", value="", key=f"cell_{i}_{j}")

                    st.table(diagnosis_df)  # Display the table

                # Upload all answers to Firestore
                if st.button("Upload Answers"):
                    collection_name = os.getenv('FIREBASE_COLLECTION')
                    if collection_name is None:
                        st.error("FIREBASE_COLLECTION environment variable not set.")
                        return
                    try:
                        data = {f"question_{i + 1}": ans for i, ans in enumerate(st.session_state.answers)}
                        db.collection(collection_name).add(data)
                        st.success("All answers saved to Firestore!")
                    except Exception as e:
                        st.error(f"Error saving answers: {e}")

        if __name__ == '__main__':
            main()

    except json.JSONDecodeError:
        st.error("Error parsing FIREBASE_KEY: Invalid JSON format.")
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


