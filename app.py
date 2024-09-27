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
        return []

# Set the page config to normal
st.set_page_config(layout="wide")

# Load Firebase credentials from environment variable
FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

if FIREBASE_KEY_JSON is None or FIREBASE_KEY_JSON == "":
    st.error("FIREBASE_KEY environment variable not set or is empty.")
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
            db.collection('your_collection_name').add(entry)
            return "Data uploaded to Firebase."

        # Initialize session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "diagnoses"
        if 'diagnoses' not in st.session_state:
            st.session_state.diagnoses = [""] * 5
        if 'laboratory_features' not in st.session_state:
            st.session_state.laboratory_features = [""] * 5
        if 'selected_diagnosis' not in st.session_state:
            st.session_state.selected_diagnosis = st.session_state.diagnoses[0]

        # Load diagnoses from file after Firebase initialization
        dx_options = read_diagnoses_from_file()
        dx_options.insert(0, "")  # Add a blank option at the beginning

        # Title of the app
        st.title("")

        # Diagnoses Page
        if st.session_state.current_page == "diagnoses":
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS UPDATE
                Based on the information that has been subsequently provided in the above case, please review your initial differential diagnosis list and update it as necessary. 
            """)

            # Debugging output
            st.write("Diagnoses:", st.session_state.diagnoses)
            st.write("Diagnosis options:", dx_options)

            # Create a draggable list for diagnoses
            for i in range(5):
                current_diagnosis = st.session_state.diagnoses[i]
                
                # Use a safe index for selectbox
                if current_diagnosis not in dx_options:
                    current_diagnosis = ""  # Default to blank if not found

                st.session_state.diagnoses[i] = st.selectbox(
                    f"Diagnosis {i + 1}",
                    options=dx_options,
                    index=dx_options.index(current_diagnosis),
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

            # Create a container for centering
            main_container = st.container()

            with main_container:
                # Reorder section in the sidebar
                with st.sidebar:
                    st.subheader("Reorder Diagnoses")

                    selected_diagnosis = st.selectbox(
                        "Select a diagnosis to move",
                        options=st.session_state.diagnoses,
                        key="move_diagnosis",
                        index=st.session_state.diagnoses.index(st.session_state.selected_diagnosis) if st.session_state.selected_diagnosis in st.session_state.diagnoses else 0
                    )

                    move_direction = st.radio("Adjust Priority:", options=["Higher Priority", "Lower Priority"], key="move_direction")

                    if st.button("Adjust Priority"):
                        idx = st.session_state.diagnoses.index(selected_diagnosis)
                        if move_direction == "Higher Priority" and idx > 0:
                            # Swap with the previous diagnosis
                            st.session_state.diagnoses[idx], st.session_state.diagnoses[idx - 1] = st.session_state.diagnoses[idx - 1], st.session_state.diagnoses[idx]
                        elif move_direction == "Lower Priority" and idx < len(st.session_state.diagnoses) - 1:
                            # Swap with the next diagnosis
                            st.session_state.diagnoses[idx], st.session_state.diagnoses[idx + 1] = st.session_state.diagnoses[idx + 1], st.session_state.diagnoses[idx]

                        # Update the selected diagnosis
                        st.session_state.selected_diagnosis = selected_diagnosis

                    # Diagnosis change section
                    st.subheader("Change a Diagnosis")
                    diagnosis_to_change = st.selectbox(
                        "Select a diagnosis to change",
                        options=st.session_state.diagnoses,
                        key="change_diagnosis"
                    )
                    new_diagnosis = st.selectbox(
                        "Select a new diagnosis",
                        options=dx_options,
                        key="new_diagnosis"
                    )

                    if st.button("Change Diagnosis"):
                        change_index = st.session_state.diagnoses.index(diagnosis_to_change)
                        st.session_state.diagnoses[change_index] = new_diagnosis

                # Create columns for each diagnosis input
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

                # Submit button for laboratory features
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

                    # Prepare the entry for Firebase
                    entry = {
                        'updated_diagnoses': st.session_state.diagnoses,
                        'laboratory_features': st.session_state.laboratory_features,
                        'lab_assessments': assessments
                    }

                    result = upload_to_firebase(entry)
                    st.success(result)

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


