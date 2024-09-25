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

            answers = []

            # Ask the user each question
            for i, question in enumerate(questions):
                if i == 0:  # Special handling for the first question
                    answer = st.text_area(question, key=f"answer_{i}", height=150)  # Larger input box
                    answers.append([answer])  # Wrap in a list for consistency
                elif i == 1:  # Special handling for question 2
                    st.subheader(f"{question} (enter up to 5 unique diagnoses):")
                    question_answers = []
                    for j in range(5):  # Create 5 input fields horizontally
                        answer = st.text_input(f"Diagnosis {j + 1}:", key=f"answer_{i}_{j}")
                        question_answers.append(answer)
                    answers.append(question_answers)
                else:
                    answer = st.text_input(question, key=f"answer_{i}")
                    answers.append([answer])  # Wrap in a list for consistency

            # Show the table after question 2
            if len(answers) > 1:
                st.subheader("Historical Facts Table")
                df = pd.DataFrame(columns=[f"question_{i + 1}" for i in range(len(questions))])

                # Fill the DataFrame with answers
                for i in range(5):
                    for j in range(len(answers)):
                        if i < len(answers[j]):
                            df.loc[i, f"question_{j + 1}"] = answers[j][i]
                        else:
                            df.loc[i, f"question_{j + 1}"] = ""  # Leave blank if no answer

                st.table(df)

            # Save answers to Firestore when the user clicks the button
            if st.button("Submit Answers"):
                # Prepare data for Firestore
                data = {}
                for idx, answer_list in enumerate(answers):
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



