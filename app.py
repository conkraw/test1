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

st.set_page_config(layout="wide")

def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Default page

    print(f"Current page: {st.session_state.page}")  # Debugging statement

    # Sidebar logic
    if st.session_state.page in ["welcome", "login"]:
        st.sidebar.empty()  # Hide sidebar for these pages
    else:
        # Sidebar for navigation (adjust as necessary for your app)
        st.sidebar.title("Navigation")
        st.sidebar.selectbox("Select a page:", [
            "welcome",
            "login",
            "intake_form",
            "diagnoses",
            "Intervention Entry",
            "History with AI",
            "Focused Physical Examination",
            "Physical Examination Components",
            "History Illness Script",
            "Physical Examination Features",
            "Laboratory Tests",
            "Radiology Tests",
            "Other Tests",
            "Results",
            "Laboratory Features",
            "Treatments",
            "Simple Success"
        ], index=list(pages.keys()).index(st.session_state.page), key="page_selector")

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

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()


