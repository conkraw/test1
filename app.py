import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

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

        # Initialize session state for diagnoses and features
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5  # Initialize with empty strings for 5 diagnoses
        if 'historical_features' not in st.session_state:
            st.session_state.historical_features = [""] * 5  # Initialize for historical features
        if 'physical_examination_features' not in st.session_state:
            st.session_state.physical_examination_features = [""] * 5  # Initialize for physical examination features
        if 'submitted_historical' not in st.session_state:
            st.session_state.submitted_historical = False
        if 'submitted_physical' not in st.session_state:
            st.session_state.submitted_physical = False

        # Title of the app

        # Input Section for Diagnoses
        if not st.session_state.submitted_historical:
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Based on the information provided in the above case, please provide 5 possible diagnoses that you would consider when prompted by your attending? Please do not provide duplicate diagnoses.
            """)

            # Create columns for each diagnosis input
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.session_state.diagnoses[i] = st.text_input(
                        f"Diagnosis {i + 1}",
                        value=st.session_state.diagnoses[i],
                        key=f"diagnosis_{i}"
                    )

            # Button to submit the diagnoses
            if st.button("Submit Diagnoses"):
                diagnoses = [d.strip() for d in st.session_state.diagnoses]  # Strip whitespace
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):  # Check for duplicates
                        st.session_state.submitted_historical = True  # Move to historical features
                        st.success("Diagnoses submitted! You can now fill in the Historical Features.")
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please enter all 5 diagnoses.")

        # Historical Features Section
        if st.session_state.submitted_historical and not st.session_state.submitted_physical:
            st.markdown("""
                ### HISTORICAL FEATURES
                Based on the history that you have collected, please provide up to 5 historical features that will influence the differential diagnosis.
            """)

            # Create a header row for diagnoses
            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:  # First column for "Historical Features"
                st.markdown("<div style='text-align: center;'>Historical Features</div>", unsafe_allow_html=True)

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(f"<div style='text-align: center;'>{diagnosis}</div>", unsafe_allow_html=True)

            # Create rows for user inputs and dropdowns
            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)

                with cols[0]:  # The first column is for row headers
                    st.session_state.historical_features[i] = st.text_input("", key=f"hx_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):  # The rest are dropdowns
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],  # Added blank option
                            key=f"select_{i}_{diagnosis}_hx",
                            label_visibility="collapsed"
                        )

            # Upload Data Button
            if st.button("Submit Historical Features"):
                # Gather all the data into a single entry
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_hx"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'historical_feature': st.session_state.historical_features[i],
                            'assessment': assessment
                        })

                entry = {
                    'diagnoses': st.session_state.diagnoses,
                    'historical_features': st.session_state.historical_features,
                    'hx_assessments': assessments
                }

                # Upload to Firebase
                result = upload_to_firebase(entry)
                st.success(result)
                st.session_state.submitted_physical = True  # Allow moving to physical examination features

        # Physical Examination Features Section
        if st.session_state.submitted_physical:
            st.markdown("""
                ### PHYSICAL EXAMINATION FEATURES
                Based on the physical examination, please provide up to 5 features that will influence the differential diagnosis.
            """)

            # Create a header row for diagnoses
            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:  # First column for "Physical Examination Features"
                st.markdown("<div style='text-align: center;'>Physical Examination Features</div>", unsafe_allow_html=True)

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(f"<div style='text-align: center;'>{diagnosis}</div>", unsafe_allow_html=True)

            # Create rows for user inputs and dropdowns for physical examination features
            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)

                with cols[0]:  # The first column is for row headers
                    st.session_state.physical_examination_features[i] = st.text_input("", key=f"pe_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):  # The rest are dropdowns
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],  # Added blank option
                            key=f"select_{i}_{diagnosis}_pe",
                            label_visibility="collapsed"
                        )

            # Upload Data Button
            if st.button("Submit Physical Examination Features"):
                # Gather all the data into a single entry
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_pe"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'physical_examination_feature': st.session_state.physical_examination_features[i],
                            'assessment': assessment
                        })

                entry = {
                    'diagnoses': st.session_state.diagnoses,
                    'physical_examination_features': st.session_state.physical_examination_features,
                    'pe_assessments': assessments
                }

                # Upload to Firebase
                result = upload_to_firebase(entry)
                st.success(result)

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

