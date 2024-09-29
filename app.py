import streamlit as st
from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page
from utils.assessment import display_assessment
from utils.diagnoses import display_diagnoses

st.set_page_config(layout="wide")

def main():
    # Load user data
    users = load_users()

    # Initialize session state for page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Start on the welcome page

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
