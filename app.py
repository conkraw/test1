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
from utils.firebase_operations import initialize_firebase, upload_to_firebase  # Import your Firebase functions
from utils.session_management import collect_session_data  # Import the session management function

st.set_page_config(layout="wide")

def main():
    # Initialize Firebase
    db = initialize_firebase()  # Call Firebase initialization
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Default page

    print(f"Current page: {st.session_state.page}")  # Debugging statement

    # Collect and upload session data whenever the page changes
    #previous_page = st.session_state.get("previous_page")
    #if previous_page != st.session_state.page:
    #    save_session_data(db)  # Pass db to the save function
    #    st.session_state.previous_page = st.session_state.page  

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        login_page(users, db)
    elif st.session_state.page == "intake_form":
        display_intake_form(db)
    elif st.session_state.page == "diagnoses":
        display_diagnoses(db)
    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main(db)
    elif st.session_state.page == "History with AI":
        run_virtual_patient()
    elif st.session_state.page == "Focused Physical Examination":
        display_focused_physical_examination()
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        history_illness_script()
    elif st.session_state.page == "Physical Examination Features":
        display_physical_examination_features()
    elif st.session_state.page == "Laboratory Tests":
        display_laboratory_tests()
    elif st.session_state.page == "Radiology Tests":
        display_radiological_tests()
    elif st.session_state.page == "Other Tests":
        display_other_tests()
    elif st.session_state.page == "Results":
        display_results_image()
    elif st.session_state.page == "Laboratory Features":
        display_laboratory_features()
    elif st.session_state.page == "Treatments":
        display_treatments()
    elif st.session_state.page == "Simple Success":
        display_simple_success1()

def save_session_data(db):
    session_data = collect_session_data()
    try:
        upload_message = upload_to_firebase(db, session_data)  # Pass db as an argument
        st.success(upload_message)  # Provide feedback to the user
    except Exception as e:
        st.error(f"Error saving progress: {e}")


def collect_session_data():
    session_data = {
        "unique_code": st.session_state.get("unique_code", ""),
        "diagnoses": st.session_state.get("diagnoses", []),
        # ... add other session state variables here
    }
    return session_data

if __name__ == "__main__":
    main()
