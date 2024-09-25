import streamlit as st
import pandas as pd

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")
    st.write("Welcome! Please enter your unique code to access the assessment.")
    
    # Load user data
    users = load_users()
    
    # Prompt user for unique code
    unique_code = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        unique_code = unique_code.strip()  # Clean the input
        if unique_code in users['code'].values:
            user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
            st.success(f"Hi, {user_name}! Welcome to the assessment.")
        else:
            st.error("Invalid code. Please try again.")

if __name__ == "__main__":
    main()



