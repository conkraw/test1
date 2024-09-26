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

        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "diagnoses"
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5
        if 'historical_features' not in st.session_state:
            st.session_state.historical_features = [""] * 5
        if 'physical_examination_features' not in st.session_state:
            st.session_state.physical_examination_features = [""] * 5

        # Title of the app
        st.title("Differential Diagnosis App")

        # Diagnoses Page
        if st.session_state.current_page == "diagnoses":
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Please provide 5 possible diagnoses you would consider. Do not provide duplicates.
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
                diagnoses = [d.strip() for d in st.session_state.diagnoses]
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):
                        st.session_state.current_page = "historical_features"  # Move to Historical Features page
                        st.experimental_rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please enter all 5 diagnoses.")

        # Historical Features Page
        elif st.session_state.current_page == "historical_features":
            st.markdown("""
                ### HISTORICAL FEATURES
                Please provide up to 5 historical features that influence the differential diagnosis.
            """)

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Historical Features")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.historical_features[i] = st.text_input("", key=f"hx_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_hx",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Historical Features"):
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

                result = upload_to_firebase(entry)
                st.success(result)

                # Move to Physical Examination Features page
                st.session_state.current_page = "physical_examination_features"
                st.rerun()  # Rerun the app to refresh the page

        # Physical Examination Features Page
        elif st.session_state.current_page == "physical_examination_features":
            st.markdown("""
                ### PHYSICAL EXAMINATION FEATURES
                Please provide up to 5 features based on the physical examination.
            """)

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Physical Examination Features")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.physical_examination_features[i] = st.text_input("", key=f"pe_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_pe",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Physical Examination Features"):
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

                result = upload_to_firebase(entry)
                st.success(result)

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


