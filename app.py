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
from utils.simple_success import display_simple_success  # Make sure this import is correct
from utils.physical_examination_features import main as physical_examination_features

st.set_page_config(layout="wide")

def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Default page

    print(f"Current page: {st.session_state.page}")  # Debugging statement

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
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
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        history_illness_script()
    #elif st.session_state.page == "Physical Examination Features":
    #    physical_examination_features()  # Show the simple success page
    elif st.session_state.page == "Simple Success":
        display_simple_success()  # Show the simple success page

if __name__ == "__main__":
    main()


