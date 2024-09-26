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
        # Display welcome message and instructions if user is logged in
        st.write(f"Welcome, {st.session_state.user_name}!")
        st.subheader("Instructions")
        st.write("""
            Please read the following instructions carefully before proceeding:
            - Step 1: Familiarize yourself with the assessment format.
            - Step 2: Ensure you have a quiet environment to take the assessment.
            - Step 3: Once ready, click on the 'Start Assessment' button below.
        """)
        # Add a button to start the assessment
        if st.button("Start Assessment"):
            st.write("Starting the assessment... (This is where you'd redirect or show the assessment)")
            # You can implement the logic to start the assessment here.

    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")

        # Prompt user for unique code
        unique_code = st.text_input("Unique Code:", placeholder="Enter your unique code")

        if st.button("Next"):
            if unique_code:
                try:
                    unique_code = int(unique_code.strip())  # Convert input to integer
                    if unique_code in users['code'].values:
                        st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                        # Rerun to display the welcome page and instructions
                        st.rerun()
                    else:
                        st.error("Invalid code. Please try again.")
                except ValueError:
                    st.error("Please enter a valid code.")
            else:
                st.error("Please enter a code.")

if __name__ == "__main__":
    main()

