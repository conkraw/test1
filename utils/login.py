# login.py

import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase

def login_page(users, db, document_id):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            try:
                unique_code = int(unique_code_input.strip())  # Ensure the code is an integer
                st.write(f"Entered Unique Code: {unique_code}")  # Debug output
                
                if str(unique_code) in users['code'].astype(str).values:
                #if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code
                    
                    # Prepare the entry data
                    entry = {
                        "unique_code": unique_code,
                        "user_name": st.session_state.user_name,
                    }
                    upload_message = upload_to_firebase(db, document_id, entry)

                    st.success(upload_message)  # Show success message
                    st.session_state.page = "intake_form"  # Navigate to the next page
                    st.rerun()  # Refresh the page
                    return unique_code  # Return the unique code for further processing
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")
    return None  # Return None if no valid code was entered
