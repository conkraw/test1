import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import os
import json

# Constants
COLLECTION_NAME = 'your_collection_name'  # Change this to your collection name

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []  # Return an empty list if error occurs

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
            db.collection(COLLECTION_NAME).add(entry)
            return "Data uploaded to Firebase."

        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "diagnoses"
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5
        if 'laboratory_testing' not in st.session_state:
            st.session_state.laboratory_testing = [""] * 5
        if 'radiological_tests' not in st.session_state:
            st.session_state.radiological_tests = [""] * 5
        if 'other_tests' not in st.session_state:
            st.session_state.other_tests = [""] * 5

        # Title of the app
        st.title("Differential Diagnosis Tool")

        # Diagnoses Page
        if st.session_state.current_page == "diagnoses":
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Please select 5 possible diagnoses you would consider. Do not provide duplicates.
            """)

            # Load diagnoses from file
            dx_options = read_diagnoses_from_file()
            if not dx_options:
                st.error("No diagnoses available. Please check the dx_list.txt file.")
            else:
                dx_options.insert(0, "")  # Add a blank option at the beginning

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
                            st.session_state.current_page = "laboratory_testing"  # Move to Laboratory Testing page
                            st.rerun()  # Rerun the app to refresh the page
                        else:
                            st.error("Please do not provide duplicate diagnoses.")
                    else:
                        st.error("Please select all 5 diagnoses.")

        # Laboratory Testing Page
        elif st.session_state.current_page == "laboratory_testing":
            st.markdown("### LABORATORY TESTING")
            st.write("For each laboratory test that you have chosen, please describe how they would influence your differential diagnosis.")

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Laboratory Tests")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.laboratory_testing[i] = st.text_input("", key=f"lab_test_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_lab",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Laboratory Testing"):
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_lab"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'laboratory_test': st.session_state.laboratory_testing[i],
                            'assessment': assessment
                        })

                entry = {
                    'diagnoses': st.session_state.diagnoses,
                    'laboratory_testing': st.session_state.laboratory_testing,
                    'lab_assessments': assessments
                }

                result = upload_to_firebase(entry)
                st.success(result)

                # Move to Radiological Tests page
                st.session_state.current_page = "radiological_tests"
                st.rerun()  # Rerun the app to refresh the page

        # Radiological Tests Page
        elif st.session_state.current_page == "radiological_tests":
            st.markdown("### RADIOLOGICAL TESTS")
            st.write("For each radiological test that you have chosen, please describe how they would influence your differential diagnosis.")

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Radiological Tests")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.radiological_tests[i] = st.text_input("", key=f"radio_test_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_radio",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Radiological Tests"):
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_radio"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'radiological_test': st.session_state.radiological_tests[i],
                            'assessment': assessment
                        })

                entry = {
                    'diagnoses': st.session_state.diagnoses,
                    'radiological_tests': st.session_state.radiological_tests,
                    'radio_assessments': assessments
                }

                result = upload_to_firebase(entry)
                st.success(result)

                # Move to Other Tests page
                st.session_state.current_page = "other_tests"
                st.rerun()  # Rerun the app to refresh the page

        # Other Tests Page
        elif st.session_state.current_page == "other_tests":
            st.markdown("### OTHER TESTS")
            st.write("For each other test that you have chosen, please describe how they would influence your differential diagnosis.")

            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.markdown("Other Tests")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.markdown(diagnosis)

            for i in range(5):
                cols = st.columns(len(st.session_state.diagnoses) + 1)
                with cols[0]:
                    st.session_state.other_tests[i] = st.text_input("", key=f"other_test_row_{i}", label_visibility="collapsed")

                for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                    with col:
                        st.selectbox(
                            "",
                            options=["", "Supports", "Does not support"],
                            key=f"select_{i}_{diagnosis}_other",
                            label_visibility="collapsed"
                        )

            if st.button("Submit Other Tests"):
                assessments = {}
                for i in range(5):
                    for diagnosis in st.session_state.diagnoses:
                        assessment = st.session_state[f"select_{i}_{diagnosis}_other"]
                        if diagnosis not in assessments:
                            assessments[diagnosis] = []
                        assessments[diagnosis].append({
                            'other_test': st.session_state.other_tests[i],
                            'assessment': assessment
                        })

                entry = {
                    'diagnoses': st.session_state.diagnoses,
                    'other_tests': st.session_state.other_tests,
                    'other_assessments': assessments
                }

                result = upload_to_firebase(entry)
                st.success(result)

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")
``


