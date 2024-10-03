# login.py

import streamlit as st
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase

def login_page(users, db, document_id):  # Accept document_id as a parameter
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    
    # Check if users DataFrame is empty
    if users.empty:
        st.error("No users found. Please check the user data source.")
        return

    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit", key="login"):
        if unique_code_input:
            try:
                # Convert the input to an integer and check if it's valid
                unique_code = int(unique_code_input.strip())
                if unique_code in users['code'].astype(str).values:  # Ensure comparison is correct
                    # Store the unique code in session state
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.unique_code = unique_code

                    # Check for existing session data in Firebase
                    existing_data = db.collection('your_collection_name').document(unique_code_input).get()  # Update with your collection name
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
                        # Add any other session data as needed
                    }
                    
                    # Upload the session data to Firebase
                    upload_message = upload_to_firebase(db, document_id, entry)
                    
                    st.success(upload_message)  # Show success message
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

