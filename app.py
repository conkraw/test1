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
                        st.session_state.question_index += 1  # Move to the next question
                else:
                    answer = st.text_input(question, key=f"answer_{current_index}")
                    st.session_state.answers.append([answer])  # Wrap in a list for consistency

                # Navigation buttons
                if st.button("Next"):
                    if current_index + 1 < len(questions):
                        st.session_state.question_index += 1
                    else:
                        st.success("You have reached the end of the questions.")

            # Save answers to Firestore when the user clicks the button
            if current_index == len(questions) and st.button("Submit Answers"):
                # Prepare data for Firestore
                data = {}
                for idx, answer_list in enumerate(st.session_state.answers):
                    for answer_idx, answer in enumerate(answer_list):
                        if idx == 1:  # For the second question (diagnoses)
                            # Save answers as a list under a single key
                            data['diagnoses'] = [answer if answer else "No diagnosis entered" for answer in answer_list]
                        else:
                            if answer:  # Only save non-empty answers for other questions
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


