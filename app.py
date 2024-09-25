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

        # Load questions from a CSV file
        questions = pd.read_csv("questions.csv")

        # Initialize session state for answers and question index
        if 'answers' not in st.session_state:
            st.session_state.answers = []
        if 'question_index' not in st.session_state:
            st.session_state.question_index = 0

        # Main Streamlit App
        def main():
            st.title("Questionnaire Application")

            current_index = st.session_state.question_index

            # Display the current question
            if current_index < len(questions):
                question = questions.iloc[current_index]['prompt']

                # For the first prompt, use a larger text area
                if current_index == 0:
                    answer = st.text_area(question, key=f"answer_{current_index}", height=150)
                # For the second prompt, get 5 diagnoses
                elif current_index == 1:
                    diagnosis_answers = []
                    for i in range(5):
                        diagnosis = st.text_input(f"Diagnosis {i + 1}:", key=f"diagnosis_{i}")
                        diagnosis_answers.append(diagnosis)
                    answer = diagnosis_answers
                else:
                    answer = st.text_input(question, key=f"answer_{current_index}")

                # Button to go to the next question
                if st.button("Next"):
                    if current_index == 1 and any(not d for d in answer):
                        st.error("Please provide all 5 diagnoses before proceeding.")
                    else:
                        if answer:  # Check if an answer is provided
                            st.session_state.answers.append(answer)
                            st.session_state.question_index += 1
                            st.success("Answer recorded! Click Next for the next question.")
                        else:
                            st.error("Please provide an answer before proceeding.")

            # When all questions are answered
            if current_index >= len(questions):
                st.success("You have completed all questions!")

                # Create a 6x6 table for user inputs
                st.subheader("Enter Historical Facts and Diagnoses")
                diagnosis_columns = ["Historical Facts"] + st.session_state.answers[1]  # Using the answers from the diagnosis
                diagnosis_df = pd.DataFrame(columns=diagnosis_columns)

                # Create input fields in the table
                for i in range(5):
                    row_data = [st.text_input(f"Row {i + 1} - Historical Facts", key=f"fact_{i}")]
                    for j in range(5):
                        row_data.append(st.text_input(f"Row {i + 1}, Diagnosis {j + 1}", key=f"diagnosis_input_{i}_{j}"))
                    diagnosis_df.loc[i] = row_data

                st.table(diagnosis_df)  # Display the table

                # Upload all answers to Firestore when done
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



