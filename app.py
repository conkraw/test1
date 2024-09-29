import streamlit as st
from utils.file_operations import load_users, read_text_file, load_vital_signs, read_diagnoses_from_file
from utils.firebase_operations import upload_to_firebase
from utils.user_management import welcome_page, login_page, display_assessment, display_diagnoses

# Main app function
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

