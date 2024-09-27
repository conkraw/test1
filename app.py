import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    with open('dx_list.txt', 'r') as file:
        diagnoses = [line.strip() for line in file.readlines() if line.strip()]
    return diagnoses

# Set the page config to normal
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

        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "diagnoses"
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5

        # Title of the app
        st.title("")

        # Diagnoses Page
        if st.session_state.current_page == "diagnoses":
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Please select 5 possible diagnoses you would consider. Do not provide duplicates.
            """)

            # Load diagnoses from file
            dx_options = read_diagnoses_from_file()
            dx_options.insert(0, "")
            
            # Create columns for each diagnosis input
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.session_state.diagnoses[i] = st.selectbox(
                        f"Diagnosis {i + 1}",
                        options=dx_options,
                        index=0,
                        key=f"diagnosis_{i}"
                    )

            # Button to submit the diagnoses
            if st.button("Submit Diagnoses"):
                diagnoses = [d.strip() for d in st.session_state.diagnoses]
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):
                        # Move to prioritization page
                        st.session_state.current_page = "prioritize"
                        st.session_state.prioritized_diagnoses = diagnoses  # Store diagnoses for prioritization
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        # Prioritization Page
        elif st.session_state.current_page == "prioritize":
            st.markdown("""
                ## PRIORITIZE YOUR DIAGNOSES
                Please prioritize the diagnoses you selected by ranking them from 1 to 5.
            """)

            priorities = {}
            for i, diagnosis in enumerate(st.session_state.prioritized_diagnoses):
                priority = st.selectbox(
                    f"Priority for {diagnosis}",
                    options=[1, 2, 3, 4, 5],
                    key=f"priority_{i}"
                )
                priorities[diagnosis] = priority

            if st.button("Submit Prioritization"):
                # Sort the diagnoses by priority
                sorted_diagnoses = sorted(priorities.items(), key=lambda x: x[1])
                entry = {
                    'diagnoses': [d[0] for d in sorted_diagnoses],
                    'priorities': [d[1] for d in sorted_diagnoses]
                }
                result = upload_to_firebase(entry)
                st.success(result)

                # Optionally reset the session state or navigate to another page
                st.session_state.current_page = "diagnoses"  # or any other page
                st.session_state.diagnoses = [""] * 5  # Reset for the next round
                st.session_state.prioritized_diagnoses = []
                st.rerun()  # Rerun to refresh the app

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


