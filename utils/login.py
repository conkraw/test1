import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase

def login_page(users):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            # Set the unique code to the session state
            unique_code = unique_code_input.strip()
            if unique_code in users['code'].values:
                # Store the unique code in session state
                st.session_state.user_code = unique_code
                st.session_state.page = "intake_form"  # Redirect to the intake form page
                st.success("Login successful!")
            else:
                st.error("Invalid code. Please try again.")
        else:
            st.error("Please enter a code.")

