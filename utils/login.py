import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase
from utils.firebase_operations import load_last_page 

def login_page(users, db, document_id):  # Accept document_id as a parameter
#def login_page(users, db):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            unique_code = unique_code_input.strip()
            if unique_code in users['code'].values:
                # Store the unique code and user info in session state
                st.session_state.user_code = unique_code
                st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]

                # Set document_id to the unique code
                st.session_state.document_id = unique_code
                
                # Load the last page from Firebase
                last_page = load_last_page(db, st.session_state.document_id)
                
                # Set the last_page in session state and navigate the user to that page
                st.session_state.page = last_page

                st.success(f"Welcome back! Redirecting to {last_page}...")
                st.rerun()  # Rerun to refresh and redirect to the correct page
            else:
                st.error("Invalid code. Please try again.")
        else:
            st.error("Please enter a code.")


