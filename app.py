import streamlit as st
import pandas as pd

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
        st.success(f"Hi, {st.session_state.user_name}! Welcome to the assessment.")
    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")
        
        # Prompt user for unique code
        unique_code = st.text_input("Unique Code:")
        
        if st.button("Submit"):
            try:
                unique_code = int(unique_code.strip())  # Convert input to integer
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    # Redirect to welcome message by refreshing
                    st.experimental_rerun()  # Refresh to show the welcome page
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")

if __name__ == "__main__":
    main()



