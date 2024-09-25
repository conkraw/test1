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
            if 'diagnosis_submitted' not in st.session_state:
                st.session_state.diagnosis_submitted = False

            current_index = st.session_state.question_index

            # Display the current question
            if current_index < len(questions):
                question = questions[current_index]
                if current_index == 0:  # Special handling for the first question
                    answer = st.text_area(question, key=f"answer_{current_index}", height=150)
                    st.session_state.answers.append([answer])  # Wrap in a list for consistency
                elif current_index == 1:  # Special handling for question 2
                    st.subheader(f"{question} (enter up to 5 unique diagnoses):")
                    question_answers = []
                    for j in range(5):  # Create 5 input fields horizontally
                        answer = st.text_input(f"Diagnosis {j + 1}:", key=f"answer_{current_index}_{j}")
                        question_answers.append(answer)
                    st.session_state.answers.append(question_answers)

                    # Check if all answers have been entered
                    if all(question_answers):
                        st.session_state.diagnosis_submitted = True
                        st.session_state.question_index += 1  # Move to the next question
                else:
                    answer = st.text_input(question, key=f"answer_{current_index}")
                    st.session_state.answers.append([answer])  # Wrap in a list for consistency

                # Navigation buttons
                if st.button("Next") and not st.session_state.diagnosis_submitted:
                    if current_index + 1 < len(questions):
                        st.session_state.question_index += 1
                    else:
                        st.success("You have reached the end of the questions.")

            # If we are on the last question
            if current_index == len(questions):
                # Show the table with answers
                st.subheader("Historical Facts Table")
                df = pd.DataFrame(columns=[f"question_{i + 1}" for i in range(len(questions))])

                # Fill the DataFrame with answers
                for i in range(5):
                    for j in range(len(st.session_state.answers)):
                        if i < len(st.session_state.answers[j]):
                            df.loc[i, f"question_{j + 1}"] = st.session_state.answers[j][i]
                        else:
                            df.loc[i, f"question_{j + 1}"] = ""  # Leave blank if no answer

                # Create a new prompt and table with the answers from question 2 as column headers
                if st.session_state.diagnosis_submitted:
                    st.subheader("Diagnoses Entered")
                    diagnosis_df = pd.DataFrame(columns=[f"Diagnosis {i + 1}" for i in range(5)])
                    diagnosis_df.loc[0] = st.session_state.answers[1]  # Use the answers from question 2
                    st.table(diagnosis_df)

                st.table(df)

                # Save answers to Firestore when the user clicks the button
                if st.button("Submit Answers"):
                    # Prepare data for Firestore
                    data = {}
                    for idx, answer_list in enumerate(st.session_state.answers):
                        for answer_idx, answer in enumerate(answer_list):
                            if answer:  # Only save non-empty answers
                                data[f"question_{idx + 1}_{answer_idx + 1}"] = answer

                    collection_name = os.getenv('FIREBASE_COLLECTION')
                    
                    if collection_name is None:
                        st.error("FIREBASE_COLLECTION environment variable not set.")
                        return
                    
                    try:
                        # Store data in Firestore
                        db.collection(collection_name).add(data)
                        st.success("Answers saved to Firestore!")

                    except Exception as e:
                        st.error(f"Error saving answers: {e}")

        if __name__ == '__main__':
            main()

    except json.JSONDecodeError:
        st.error("Error parsing FIREBASE_KEY: Invalid JSON format.")
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")



