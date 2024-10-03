import streamlit as st
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
import uuid  # To generate unique document IDs

def save_user_state(db):
    if st.session_state.unique_code:  # Ensure unique_code is set
        entry = {
            "last_page": st.session_state.page,
            # Add other session data if needed
        }
        upload_to_firebase(db, str(st.session_state.unique_code), entry)  # Ensure it's a string

def load_last_page(db):
    collection_name = st.secrets["FIREBASE_COLLECTION_NAME"]  # Get collection name from secrets
    if st.session_state.unique_code:  # Ensure unique_code is set
        user_data = db.collection(collection_name).document(str(st.session_state.unique_code)).get()  # Ensure it's a string
        if user_data.exists:
            return user_data.to_dict().get("last_page", "welcome")  # Default to "welcome"
    return "welcome"

def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    # Initialize session state
    if "unique_code" not in st.session_state:
        st.session_state.unique_code = None
        
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    
    if "document_id" not in st.session_state:
        st.session_state.document_id = str(uuid.uuid4())

    # Debugging: Print current unique code and page
    st.write("Unique Code:", st.session_state.unique_code)
    st.write("Current Page:", st.session_state.page)

    # Load last page if user is logged in
    if st.session_state.unique_code:  # Ensure unique_code is set
        last_page = load_last_page(db)
        if last_page:
            st.session_state.page = last_page
            st.write("Loaded last page:", st.session_state.page)

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        login_page(users, db, st.session_state.document_id)

        # Check if login was successful
        if st.session_state.unique_code:  # Ensure unique_code is set
            st.session_state.page = load_last_page(db) or "welcome"
            st.experimental_rerun()  # Refresh to navigate to the last page
    elif st.session_state.page == "intake_form":
        display_intake_form(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "diagnoses":
        display_diagnoses(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main(db, st.session_state.document_id)
    elif st.session_state.page == "History with AI":
        run_virtual_patient(db, st.session_state.document_id)
    elif st.session_state.page == "Focused Physical Examination":
        display_focused_physical_examination(db, st.session_state.document_id)  # Pass document ID
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        history_illness_script(db, st.session_state.document_id)
    elif st.session_state.page == "Physical Examination Features":
        display_physical_examination_features(db, st.session_state.document_id)
    elif st.session_state.page == "Laboratory Tests":
        display_laboratory_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Radiology Tests":
        display_radiological_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Other Tests":
        display_other_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Results":
        display_results_image()
    elif st.session_state.page == "Laboratory Features":
        display_laboratory_features(db, st.session_state.document_id)
    elif st.session_state.page == "Treatments":
        display_treatments(db, st.session_state.document_id)
    elif st.session_state.page == "Simple Success":
        display_simple_success1()
    else:
        st.write("Page not found. Redirecting to welcome.")
        st.session_state.page = "welcome"
        st.experimental_rerun()  # Redirect to welcome page

if __name__ == "__main__":
    main()
