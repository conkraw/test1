import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Initialize session state for page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Start on the login page

    # Check which page to display
    if st.session_state.page == "assessment":
        display_image()
    else:
        login_page(users)

def login_page(users):
    st.write("Welcome! Please enter your unique code to access the assessment.")
    unique_code = st.text_input("Unique Code:")
    if st.button("Next"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.page = "assessment"  # Change to assessment page
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

def display_image():
    st.subheader("")
    st.image("ptinfo.png", use_column_width=True)

if __name__ == "__main__":
    main()


