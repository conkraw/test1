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
        # Display welcome message if user is logged in
        st.write(f"Welcome, {st.session_state.user_name}!")
    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")

        # Create columns for input
        col1, col2 = st.columns([2, 1])  # Adjust the proportions as needed

        with col1:
            unique_code = st.text_input("Unique Code:", placeholder="Enter your unique code")

        with col2:
            if st.button("Next"):
                if unique_code:
                    try:
                        unique_code = int(unique_code.strip())  # Convert input to integer
                        if unique_code in users['code'].values:
                            st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                            # Rerun to display the welcome page
                            st.rerun()
                        else:
                            st.error("Invalid code. Please try again.")
                    except ValueError:
                        st.error("Please enter a valid code.")
                else:
                    st.error("Please enter a code.")

if __name__ == "__main__":
    main()

