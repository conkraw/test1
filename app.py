import streamlit as st
from utils.file_operations import load_users
from utils.welcome import welcome_page
from utils.login import login_page
# Add other necessary imports

st.set_page_config(layout="wide")

def main():
    # Your main logic here
    users = load_users()

    if "page" not in st.session_state:
        st.session_state.page = "welcome"

    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        login_page(users)
    # Add more page conditions as needed

if __name__ == "__main__":
    main()
