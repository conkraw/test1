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

    # Check if the user is logged in
    if "user_name" in st.session_state:
        st.write(f"Welcome, {st.session_state.user_name}!")

        # Button to start assessment
        if st.button("Start Assessment"):
            st.session_state.page = "assessment"  # Set the current page to assessment
            st.rerun()  # Rerun to update the displayed page

        # Display different pages based on session state
        if st.session_state.get("page") == "assessment":
            display_image()

    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")
        unique_code = st.text_input("Unique Code:")
        if st.button("Next"):
            if unique_code:
                try:
                    unique_code = int(unique_code.strip())
                    if unique_code in users['code'].values:
                        st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                        st.session_state.page = "main"  # Reset to main page
                        st.experimental_rerun()
                    else:
                        st.error("Invalid code. Please try again.")
                except ValueError:
                    st.error("Please enter a valid code.")
            else:
                st.error("Please enter a code.")

def display_image():
    st.subheader("Instructions")
    st.image("ptinfo.png", use_column_width=True)

if __name__ == "__main__":
    # Initialize session state for the page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "main"
    main()

