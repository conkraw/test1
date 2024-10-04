import streamlit as st
from utils.session_management import collect_session_data 

def login_page(users, db):  # Accept document_id as a parameter
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            # No need to convert input to integer, treat it as a string
            unique_code = unique_code_input.strip()
            if unique_code in users['code'].values:
                # Store the unique code in session state
                st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                st.session_state.unique_code = unique_code

                # Collect session data after setting the unique code
                #session_data = collect_session_data()
                
                # Define the entry data (without uploading to Firebase)
                entry = {
                    "unique_code": unique_code,
                    "user_name": st.session_state.user_name,
                    # Add any other session data as needed
                }
                
                # Navigate to the intake form page
                st.session_state.page = "intake_form"  # Change to assessment page
                st.success("Code validated successfully!")  # Success message without Firebase upload
                st.rerun()  # Rerun to refresh the view
            else:
                st.error("Invalid code. Please try again.")
        else:
            st.error("Please enter a code.")
