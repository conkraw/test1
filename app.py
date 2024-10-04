import streamlit as st

st.set_page_config(layout="wide")

from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page
from utils.intake_form import display_intake_form
from utils.diagnoses import display_diagnoses
from utils.intervention_entry import main as intervention_entry_main
from utils.history_with_ai import run_virtual_patient
from utils.focused_physical_examination import display_focused_physical_examination
from utils.physical_examination import main as display_physical_examination
from utils.history_illness_script import main as history_illness_script
from utils.simple_success import display_simple_success
from utils.simple_success1 import display_simple_success1
from utils.physical_examination_features import display_physical_examination_features
from utils.lab_tests import display_laboratory_tests
from utils.radtests import display_radiological_tests
from utils.othertests import display_other_tests
from utils.results import display_results_image
from utils.laboratory_features import display_laboratory_features
from utils.treatments import display_treatments
from utils.firebase_operations import initialize_firebase, upload_to_firebase
from utils.session_management import collect_session_data
from utils.firebase_operations import load_last_page 
from utils.firebase_operations import get_diagnoses_from_firebase 
import uuid  # To generate unique document IDs

def save_user_state(db):
    if st.session_state.user_code:
        entry = {
            "last_page": st.session_state.page,
            # Add other session data if needed
        }
        upload_to_firebase(db, st.session_state.user_code, entry)

def load_last_page(db, document_id):
    collection_name = st.secrets["FIREBASE_COLLECTION_NAME"]  # Get collection name from secrets
    
    # Check if the document ID exists in the database
    if document_id:
        user_data = db.collection(collection_name).document(document_id).get()
        if user_data.exists:
            return user_data.to_dict().get("last_page")  # Return the last_page if found
    return "welcome"  # Default to 'welcome' if no last_page is found

        
def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    # Initialize session state
    if "user_code" not in st.session_state: ###
        st.session_state.user_code = None ###
        
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    
    # Generate a unique document ID at the start of the session
    if "document_id" not in st.session_state:
        st.session_state.document_id = None  

    if st.session_state.user_code:
        last_page = load_last_page(db, st.session_state.document_id)  # Pass the document_id
        if last_page:
            st.session_state.page = last_page

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        #login_page(users, db, st.session_state.document_id)  # Pass document ID
        login_page(users,db)  # Pass document ID
    elif st.session_state.page == "intake_form":
        display_intake_form(db, st.session_state.document_id)
    # Handling the "diagnoses" page
    # Handling the "diagnoses" page
    elif st.session_state.page == "diagnoses":
        # Pull saved diagnoses data from Firebase (in diagnoses_s1)
        diagnoses = get_diagnoses_from_firebase(db, st.session_state.document_id)
    
        # Check if diagnoses are found
        if diagnoses:
            # If diagnoses are found, pre-fill the text area with the existing diagnosis
            st.write("Previously saved diagnoses:")
            st.write(diagnoses)  # Display the saved diagnosis
    
            # Pre-fill the text area with the saved diagnosis for editing
            default_diagnosis = diagnoses  # Use the previously saved diagnosis as default
    
            st.warning("You can modify the diagnoses if needed.")
    
            # Automatically move the user to the next page (after diagnoses) if saved diagnoses exist
            st.session_state.page = "next_page"  # Change "next_page" to the actual page name
    
        else:
            # No saved diagnoses, so prompt user to enter new data
            st.warning("No saved diagnoses found. Please enter your diagnoses.")
            default_diagnosis = ""  # Empty string since no diagnoses are available
    
            # Display form to allow the user to enter new diagnoses
            with st.form(key="diagnosis_form"):
                updated_diagnosis = st.text_area("Enter new diagnosis(es):", value=default_diagnosis, height=150)
    
                # Add a submit button
                submit_button = st.form_submit_button(label="Save Diagnosis")
    
                if submit_button:
                    if updated_diagnosis:
                        # Save the updated or new diagnoses to Firebase
                        save_diagnosis_to_firebase(db, st.session_state.document_id, updated_diagnosis)
                        st.success("Diagnosis saved successfully!")
    
                        # Move to the next page after saving
                        st.session_state.page = "next_page"  # Change "next_page" to the actual page name
                    else:
                        st.error("Please enter a diagnosis before submitting.")


    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main(db,st.session_state.document_id)
    elif st.session_state.page == "History with AI":
        run_virtual_patient(db,st.session_state.document_id)
    elif st.session_state.page == "Focused Physical Examination":
        display_focused_physical_examination(db, st.session_state.document_id)  # Pass document ID
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        history_illness_script(db,st.session_state.document_id)
    elif st.session_state.page == "Physical Examination Features":
        display_physical_examination_features(db,st.session_state.document_id)
    elif st.session_state.page == "Laboratory Tests":
        display_laboratory_tests(db,st.session_state.document_id)
    elif st.session_state.page == "Radiology Tests":
        display_radiological_tests(db,st.session_state.document_id)
    elif st.session_state.page == "Other Tests":
        display_other_tests(db,st.session_state.document_id)
    elif st.session_state.page == "Results":
        display_results_image()
    elif st.session_state.page == "Laboratory Features":
        display_laboratory_features(db,st.session_state.document_id)
    elif st.session_state.page == "Treatments":
        display_treatments(db,st.session_state.document_id)
    elif st.session_state.page == "Simple Success":
        display_simple_success1()

if __name__ == "__main__":
    main()
