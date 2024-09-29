# app.py

import streamlit as st
from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page
from utils.intake_form import display_intake_form
from utils.diagnoses import display_diagnoses
from utils.intervention_entry import intervention_entry_main
from utils.history_with_ai import run_virtual_patient

st.set_page_config(layout="wide")

# Main function to control the app flow
def main():
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Default page
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
if __name__ == "__main__":
    main()
