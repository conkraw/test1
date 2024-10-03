# login.py

import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase

def login_page(users, db):  # Removed document_id parameter
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit", key="login"):
        if unique_code_input:
            try:
                # Ensure input is treated as a string for consistency
                unique_code = unique_code_input.strip()
                
                if unique_code in users['code'].astype(str).values:  # Check if the unique code exists
                    # Store the unique code in session state
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code  # Keep as string

                    # Check for existing session data in Firebase
                    existing_data = db.collection(st.secrets["FIREBASE_COLLECTION_NAME"]).document(unique_code).get()  # Use secrets for collection name
                    if existing_data.exists:
                        st.session_state.page = existing_data.to_dict().get("last_page", "intake_form")
                    else:
                        st.session_state.page = "intake_form"  # Default to intake form

                    # Collect session data after setting the unique code
                    session_data = collect_session_data()
                    
                    # Define the entry data
                    entry = {
                        "unique_code": unique_code,
                        "user_name": st.session_state.user_name,
                        "last_page": st.session_state.page,  # Save last page
                    }
                    
                    # Upload the session data to Firebase
                    upload_message = upload_to_firebase(db, unique_code, entry)  # Use unique_code as the document ID
                    
                    st.success(upload_message)  # Show success message
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")
