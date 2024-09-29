import streamlit as st
from firebase_setup import initialize_firebase, upload_to_firebase
from user_management import load_users, welcome_page, login_page
from assessment import display_assessment
from diagnoses import display_diagnoses
from intervention import upload_intervention
from virtual_patient import run_virtual_patient_app
from focused_physical_exam import focused_physical_exam  # Import the new function

def main():
    st.set_page_config(layout="wide")

    # Initialize Firebase
    initialize_firebase()

    # Load user data
    users = load_users()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
        st.session_state.diagnoses = [""] * 5
        st.session_state.selected_buttons = [False] * 5
        st.session_state.assessment_data = {}
        st.session_state.intervention_entry = None  # Initialize intervention entry

    # Check which page to display
    if st.session_state.page == "assessment":
        display_assessment()
    elif st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        login_page(users)
    elif st.session_state.page == "diagnoses":
        display_diagnoses()
    elif st.session_state.page == "intervention":
        upload_intervention()  # Just collects data, does not upload yet
    elif st.session_state.page == "virtual_patient":
        run_virtual_patient_app()  # Call the virtual patient app
        st.session_state.page = "focused_physical_exam"  # Set the next page

    # Handle focused physical examination selection
    if st.session_state.page == "focused_physical_exam":
        focused_physical_exam()

if __name__ == "__main__":
    main()



