# login.py

import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import initialize_firebase, upload_to_firebase, document_id, entry

def login_page(users, db):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            try:
                # Convert the input to an integer and check if it's valid
                unique_code = int(unique_code_input.strip())
                if unique_code in users['code'].values:
                    # Store the unique code in session state
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code

                    # Collect session data after setting the unique code
                    session_data = collect_session_data()
                    upload_message = upload_to_firebase(db, 'your_collection_name', document_id, entry)
                    
                    # Navigate to the intake form page
                    st.session_state.page = "intake_form"  # Change to assessment page
                    st.success(upload_message)  # Show success message
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

