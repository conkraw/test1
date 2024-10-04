import streamlit as st
from utils.session_management import collect_session_data 

def login_page(users, db):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code_input = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code_input:
            # No need to convert input to integer, treat it as a string
            unique_code = unique_code_input.strip()
            if unique_code in users['code'].values:
                # Store the unique code in session state
                st.session_state.user_code = unique_code  # Set the user code here
                st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                
                # Debugging: Print to see if user_code is being set correctly
                st.write(f"User code set to: {st.session_state.user_code}")
                st.write(f"User name: {st.session_state.user_name}")

                # Collect session data after setting the unique code
                session_data = collect_session_data()
                
                # Define the entry data
                entry = {
                    "unique_code": unique_code,
                    "user_name": st.session_state.user_name,
                    # Add any other session data as needed
                }
                
                # Upload the session data to Firebase (optional for now)
                upload_message = upload_to_firebase(db, unique_code, entry)
                
                # Navigate to the intake form page
                st.session_state.page = "intake_form"
                st.success(upload_message)  # Show success message
                st.rerun()  # Rerun to refresh the view
            else:
                st.error("Invalid code. Please try again.")
        else:
            st.error("Please enter a code.")

