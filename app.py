import streamlit as st
from firebase_setup import initialize_firebase, upload_to_firebase
from user_management import load_users, welcome_page, login_page
from assessment import display_assessment
from diagnoses import display_diagnoses
from intervention import upload_intervention
from virtual_patient import run_virtual_patient_app

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
        run_virtual_patient_app()

    # At the end of the app or when navigating to a new page, upload the intervention data
    if st.button("Finalize Intervention"):
        if st.session_state.intervention_entry:
            result = upload_to_firebase(st.session_state.intervention_entry)
            if result:  # Assuming upload_to_firebase returns a success condition
                st.success("Intervention data uploaded successfully!")
                st.session_state.intervention_entry = None  # Clear the entry after upload
            else:
                st.error("Failed to upload intervention data.")
        else:
            st.warning("No intervention data to upload.")

if __name__ == "__main__":
    main()


