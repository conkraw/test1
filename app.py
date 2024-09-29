import streamlit as st
import pandas as pd
from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page

# Main application function
def main():
    # Initialize session state if it does not exist
    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    # Load users
    users = load_users()

    # Navigation between pages
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        login_page(users)

if __name__ == "__main__":
    main()

