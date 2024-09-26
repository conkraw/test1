import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

st.set_page_config(layout="wide")

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

        def upload_to_firebase(entry):
            db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
            return "Data uploaded to Firebase."

        # Main Streamlit App
        def main():
            st.title("Physical Examination Selection")

            # Prompt for excluding hypotheses
            st.markdown("<h5>Please select the parts of physical examination required, in order to exclude some unlikely, but important hypotheses:</h5>", unsafe_allow_html=True)
            options1 = [
                "General Appearance", "Eyes", "Ears, Neck, Throat",
                "Lymph Nodes", "Cardiovascular", "Lungs",
                "Skin", "Abdomen", "Extremities",
                "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
            ]
            selected_exams1 = st.multiselect("Select options:", options1, key="exclude_exams")

            # Prompt for confirming hypotheses
            st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis and to discriminate between others:</h5>", unsafe_allow_html=True)
            selected_exams2 = st.multiselect("Select options:", options1, key="confirm_exams")

            if st.button("Submit"):
                # Prepare the data to upload
                entry = {
                    'excluded_exams': selected_exams1,
                    'confirmed_exams': selected_exams2
                }
                # Upload to Firebase
                result = upload_to_firebase(entry)
                st.success(result)
                st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
                st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")

        if __name__ == '__main__':
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

