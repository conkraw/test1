import streamlit as st
from firebase_setup import initialize_firebase, upload_to_firebase
from user_management import load_users, welcome_page, login_page
from assessment import display_assessment
from diagnoses import display_diagnoses
from intervention import upload_intervention

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
        upload_intervention()

if __name__ == "__main__":
    main()


