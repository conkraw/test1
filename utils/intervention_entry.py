import streamlit as st
import pandas as pd
from utils.session_management import collect_session_data  #######NEED THIS
from utils.firebase_operations import upload_to_firebase  


def main(db,document_id):
    st.title("Intervention Description Entry")

    # Prompt for user input
    st.header("Describe any interventions that you would currently perform.")
    interventions = st.text_area("Interventions Description", height=200)

    # Button to save to a local file (or any other desired action)
    if st.button("Save Intervention"):
        if interventions:
            # Collect session data
            session_data = collect_session_data()  # Collect session data
            
            # Append interventions to the session data
            #session_data['interventions'].append({
            #    "interventions": interventions
            #})

            # Create entry with the diagnoses data
                entry = {
                    "interventions": interventions
                }
            
            # Upload the session data to Firebase
            upload_message = upload_to_firebase(db, 'your_collection_name', document_id, entry)  # Upload to Firebase
            
            st.success("Your interventions have been saved successfully.")
            
            st.session_state.page = "History with AI"  # Change to the next page
            st.rerun()  # Rerun to navigate to the next page
        else:
            st.error("Please enter a description of the interventions.")

if __name__ == '__main__':
    main()
