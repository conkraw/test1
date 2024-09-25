import streamlit as st
import pandas as pd
from docx import Document
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('serviceAccountKey.json')  # Path to your service account key
firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to load questions from a Word document
def load_questions(doc_path):
    doc = Document(doc_path)
    questions = [p.text for p in doc.paragraphs if p.text]
    return questions

# Streamlit app
def main():
    st.title("Questionnaire Application")

    # Load questions from a Word document
    questions = load_questions("questions.docx")  # Ensure this file is in the same directory

    answers = []

    # Ask the user each question
    for i, question in enumerate(questions):
        answer = st.text_input(f"{question}:", key=f"answer_{i}")
        answers.append(answer)

    # Show the table after question 2
    if len(answers) > 1:
        st.subheader("Historical Facts Table")
        df = pd.DataFrame(columns=["Historical Fact"])

        # Limit the number of rows to 5
        for i in range(5):
            if i < len(answers):
                df.loc[i] = [answers[i]]
            else:
                df.loc[i] = [""]  # Leave blank if no answer

        st.table(df)

    # Save answers to Firestore when the user clicks the button
    if st.button("Submit Answers"):
        data = {
            "answers": answers[:5]  # Store only the first 5 answers
        }

        try:
            # Store data in Firestore
            db.collection(os.getenv('FIRESTORE_COLLECTION')).add(data)
            st.success("Answers saved to Firestore!")
        except Exception as e:
            st.error(f"Error saving answers: {e}")

if __name__ == "__main__":
    main()


