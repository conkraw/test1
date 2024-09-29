import streamlit as st
import pandas as pd
from utils.file_operations import load_users
from pages.welcome import welcome_page
from pages.login import login_page
from pages.assessment import display_assessment
from pages.diagnoses import display_diagnoses

# Set page layout to wide
st.set_page_config(layout="wide")

def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Initialize session state for page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Start on the welcome page
        st.session_state.diagnoses = [""] * 5  # Initialize empty diagnoses
        st.session_state.selected_buttons = [False] * 5  # Track selection status
        st.session_state.assessment_data = {}  # Store assessment data

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

