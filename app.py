import streamlit as st
from utils.file_operations import load_users
from utils.user_management import welcome_page, login_page
from utils.assessment import display_assessment
from utils.diagnosis import display_diagnoses

def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Initialize session state for the page if not already done
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

if __name__ == "__main__":
    main()

