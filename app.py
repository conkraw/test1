import streamlit as st
import pandas as pd

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")
    
    # Load the user data
    users = load_users()
    
    # Prompt user for unique code
    unique_code = st.text_input("Welcome! Please enter your unique code to access this assessment:")
    
    if st.button("Submit"):
        # Check if the entered code is valid
        if unique_code in users['code'].values:
            user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
            st.success(f"Hi, {user_name}!")
        else:
            st.error("Invalid code. Please try again.")

if __name__ == "__main__":
    main()


