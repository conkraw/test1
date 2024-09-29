import pandas as pd
import streamlit as st
import os
import json
from firebase_admin import credentials, firestore

# Function to initialize Firebase (if needed)
def initialize_firebase():
    FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

    if FIREBASE_KEY_JSON is None:
        st.error("FIREBASE_KEY environment variable not set.")
    else:
        try:
            firebase_credentials = json.loads(FIREBASE_KEY_JSON)

            if not firebase_admin._apps:
                cred = credentials.Certificate(firebase_credentials)
                firebase_admin.initialize_app(cred)

            return firestore.client()  # Return Firestore client
        except Exception as e:
            st.error(f"Error initializing Firebase: {e}")

# Function for focused physical examination selection
def focused_physical_exam():
    db = initialize_firebase()  # Call to initialize Firebase and get db

    st.title("Focused Physical Examination Selection")

    # Exclude hypotheses selection
    st.markdown("<h5>Please select the parts of physical examination required:</h5>", unsafe_allow_html=True)
    options1 = [
        "General Appearance", "Eyes", "Ears, Neck, Throat",
        "Lymph Nodes", "Cardiovascular", "Lungs",
        "Skin", "Abdomen", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
    ]
    selected_exams1 = st.multiselect("Select options:", options1, key="exclude_exams")

    # Confirm hypotheses selection
    st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis:</h5>", unsafe_allow_html=True)
    selected_exams2 = st.multiselect("Select options:", options1, key="confirm_exams")

    if st.button("Submit"):
        # Prepare the data to upload
        entry = {
            'excluded_exams': selected_exams1,
            'confirmed_exams': selected_exams2
        }
        # Upload to Firebase (if desired)
        # result = upload_to_firebase(entry)  # Uncomment if you want to upload
        st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
        st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")
