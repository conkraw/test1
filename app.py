import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []  # Return an empty list in case of error

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
        if 'laboratory_features' not in st.session_state:
            st.session_state.laboratory_features = [""] * 5

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
            dx_options.insert(0, "")  # Add a blank option at the beginning

            # Create columns for each diagnosis input
            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.session_state.diagnoses[i] = st.selectbox(
                        f"Diagnosis {i + 1}",
                        options=dx_options,
                        index=0,  # Default to the blank option
                        key=f"diagnosis_{i}"
                    )

            # Button to submit the diagnoses
            if st.button("Submit Diagnoses"):
                diagnoses = [d.strip() for d in st.session_state.diagnoses]
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):
                        st.session_state.current_page = "laboratory_features"  # Move to Laboratory Features page
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        # Laboratory Features Page
        elif st.session_state.current_page == "laboratory_features":
            st.markdown("""
                ### LABORATORY FEATURES
                Please provide up to 5 laboratory features that influence the differential diagnosis.
            """)

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Laboratory Features")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.laboratory_features[i] = st.text_input("", key=f"lab_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_lab",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Laboratory Features"):
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_lab"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'laboratory_feature': st.session_state.laboratory_features[i],
                            'assessment': assessment
                        })

                # Prepare the entry for Firebase with the new key for diagnoses
                entry = {
                    'updated_diagnoses': st.session_state.diagnoses,  # Renamed key
                    'laboratory_features': st.session_state.laboratory_features,
                    'lab_assessments': assessments
                }

                result = upload_to_firebase(entry)
                st.success(result)

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

