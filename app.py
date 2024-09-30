# app.py

import streamlit as st
from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page
from utils.intake_form import display_intake_form
from utils.diagnoses import display_diagnoses
from utils.intervention_entry import main as intervention_entry_main
from utils.history_with_ai import run_virtual_patient
from utils.focused_physical_examination import display_focused_physical_examination 
from utils.physical_examination import main as display_physical_examination  # Import the main function
from utils.history_illness_script import main as history_illness_script  # Import the history illness script
from simple_success import display_simple_success  # Import the simple success module

st.set_page_config(layout="wide")

# Main function to control the app flow
def main():
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Default page

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()  # Ensure you have this function
        login_page(users)
    elif st.session_state.page == "intake_form":
        display_intake_form()
    elif st.session_state.page == "diagnoses":
        display_diagnoses()
    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main()
    elif st.session_state.page == "History with AI":
        run_virtual_patient()
    elif st.session_state.page == "Focused Physical Examination":
        display_focused_physical_examination()  
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()  # Call the main function from physical_examination.py
    elif st.session_state.page == "History Illness Script":
        history_illness_script()  # Call the main function from history_illness_script.py
    elif st.session_state.page == "Simple Success":  # Use the new condition here
        display_simple_success()  # Call the simple success module

if __name__ == "__main__":
    main()

