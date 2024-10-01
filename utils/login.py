# login.py

import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase 

def login_page(users):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code = st.text_input("Unique Code:")

    if st.button("Submit"):
        session_data = collect_session_data()
        upload_message = upload_to_firebase(db, session_data) 
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code  # Store unique code in session state
                    st.session_state.page = "intake_form"  # Change to assessment page
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")
