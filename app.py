import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Load Firebase credentials from environment variable
FIREBASE_KEY_JSON = os.getenv('FIREBASE_KEY')

if FIREBASE_KEY_JSON is None:
    st.error("FIREBASE_KEY environment variable not set.")
else:
    try:
        # Parse the JSON string into a dictionary
        firebase_credentials = json.loads(FIREBASE_KEY_JSON)

        # Initialize Firebase only if not already initialized
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_credentials)
            firebase_admin.initialize_app(cred)

        # Get Firestore client
        db = firestore.client()

        # Function to upload data to Firebase
        def upload_to_firebase(entry):
            db.collection('your_collection_name').add(entry)  # Change 'your_collection_name' to your collection name
            return "Data uploaded to Firebase."

        # Set page layout to wide
        st.set_page_config(layout="wide")

        # Cache loading of users from CSV
        @st.cache_data
        def load_users():
            return pd.read_csv('users.csv')

        # Function to read text from a TXT file
        def read_text_file(txt_file_path):
            try:
                with open(txt_file_path, 'r') as file:
                    return file.read()
            except FileNotFoundError:
                st.error(f"File not found: {txt_file_path}. Please check the file path.")
                return ""
            except Exception as e:
                st.error(f"An error occurred: {e}")
                return ""

        # Function to load vital signs from a TXT file
        def load_vital_signs(vital_signs_file):
            vital_signs = {}
            try:
                with open(vital_signs_file, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) == 2:
                            key = parts[0].strip()  # Get type (e.g., heart_rate)
                            value = parts[1].strip()  # Get vital sign description
                            vital_signs[key] = value
            except FileNotFoundError:
                st.error(f"File not found: {vital_signs_file}. Please check the file path.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

            return vital_signs

        # Initialize session state for assessment data
        if 'assessment_data' not in st.session_state:
            st.session_state.assessment_data = {}

        # Main app function
        def main():
            st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

            # Load user data
            users = load_users()

            # Initialize session state for page if not already done
            if "page" not in st.session_state:
                st.session_state.page = "welcome"  # Start on the welcome page

            # Check which page to display
            if st.session_state.page == "assessment":
                display_assessment()
            elif st.session_state.page == "welcome":
                welcome_page()
            elif st.session_state.page == "login":
                login_page(users)
            elif st.session_state.page == "diagnoses":
                display_diagnoses()
            elif st.session_state.page == "interventions":
                upload_intervention()

        # Welcome page function
        def welcome_page():
            st.markdown("<h3 style='font-family: \"DejaVu Sans\";'>Welcome to the Pediatric Clerkship Assessment!</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-family: \"DejaVu Sans\";'>This assessment is designed to evaluate your clinical reasoning skills.</p>", unsafe_allow_html=True)
            st.markdown("<h4 style='font-family: \"DejaVu Sans\";'>Instructions:</h4>", unsafe_allow_html=True)
            st.markdown("<p style='font-family: \"DejaVu Sans\";'>1. Please enter your unique code on the next page.<br>2. Follow the prompts to complete the assessment.</p>", unsafe_allow_html=True)

            if st.button("Next"):
                st.session_state.page = "login"  # Change to login page
                st.rerun()  # Rerun to refresh the view

        # Login page function
        def login_page(users):
            st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
            unique_code = st.text_input("Unique Code:")

            if st.button("Submit"):
                if unique_code:
                    try:
                        unique_code = int(unique_code.strip())
                        if unique_code in users['code'].values:
                            st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                            st.session_state.unique_code = unique_code  # Store unique code in session state
                            st.session_state.page = "assessment"  # Change to assessment page
                            st.rerun()  # Rerun to refresh the view
                        else:
                            st.error("Invalid code. Please try again.")
                    except ValueError:
                        st.error("Please enter a valid code.")
                else:
                    st.error("Please enter a code.")

        # Function to display the assessment page
        def display_assessment():
            st.markdown(f"<h3 style='font-family: \"DejaVu Sans\";'>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

            # Read and display the text from ptinfo.txt
            txt_file_path = "ptinfo.txt"
            document_text = read_text_file(txt_file_path)

            if document_text:
                st.markdown("<h2>Patient Information:</h2>", unsafe_allow_html=True)
                st.markdown(f"<div>{document_text.replace('\n', '<br>')}</div>", unsafe_allow_html=True)

            # Load vital signs
            vital_signs_file = "vital_signs.txt"
            vital_signs = load_vital_signs(vital_signs_file)

            if vital_signs:
                st.markdown("<h2>Vital Signs:</h2>", unsafe_allow_html=True)
                st.session_state.assessment_data['vital_signs'] = {}

                for key, value in vital_signs.items():
                    checkbox_label = f"{key.upper()}: {value}"
                    checkbox_value = st.checkbox(checkbox_label)
                    st.session_state.assessment_data['vital_signs'][key] = checkbox_value  # Save checkbox value

            # Button to proceed to diagnoses
            if st.button("Next"):
                if st.session_state.assessment_data:  # Check if assessment data is populated
                    st.session_state.page = "diagnoses"  # Move to Diagnoses page
                    st.rerun()  # Rerun the app to refresh the page
                else:
                    st.error("Please complete the assessment before updating diagnoses.")

        # Diagnoses Page function
        def display_diagnoses():
            if not st.session_state.assessment_data:
                st.error("Please complete the assessment before updating diagnoses.")
                return

            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS UPDATE
                Based on the information that has been subsequently provided in the above case, please review your initial differential diagnosis list and update it as necessary. 
            """)

            # Read diagnoses from file
            dx_options = read_diagnoses_from_file()  # Implement this function

            # Create columns for each diagnosis input
            cols = st.columns(5)  # Create 5 columns for 5 diagnoses

            for i, col in enumerate(cols):
                current_diagnosis = st.session_state.diagnoses[i]

                with col:
                    # Search input for diagnosis
                    search_input = st.text_input(
                        f"Diagnosis {i + 1}",
                        value=current_diagnosis,
                        key=f"diagnosis_search_{i}"
                    )

                    # Filter options based on the search input
                    filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

                    # Display filtered options
                    if filtered_options and not st.session_state.selected_buttons[i]:
                        st.write("**Suggestions:**")
                        for option in filtered_options[:5]:  # Show a maximum of 5 options
                            button_key = f"select_option_{i}_{option}"
                            if st.button(f"{option}", key=button_key):
                                st.session_state.diagnoses[i] = option
                                st.session_state.selected_buttons[i] = True  # Mark as selected
                                st.rerun()  # Refresh the app

            # Button to submit the diagnoses
            if st.button("Submit Diagnoses"):
                diagnoses = [d.strip() for d in st.session_state.diagnoses]
                # Check for empty diagnoses and duplicates
                if all(diagnosis for diagnosis in diagnoses):
                    if len(diagnoses) == len(set(diagnoses)):
                        # Upload to Firebase
                        entry = {
                            'unique_code': st.session_state.unique_code,
                            'diagnoses': diagnoses,
                            'assessment_data': st.session_state.assessment_data,
                        }
                        result = upload_to_firebase(entry)
                        st.success("Diagnoses uploaded to Firebase.")
                        st.session_state.page = "interventions"  # Move to Intervention page
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        # Intervention Page function
        def upload_intervention():
            st.title("Intervention Description Entry")

            # Prompt for user input
            st.header("Describe any interventions that you would currently perform.")
            interventions = st.text_area("Interventions Description", height=200)

            # Button to upload to Firebase
            if st.button("Upload Intervention"):
                if interventions:
                    entry = {'interventions': interventions}
                    # Immediately upload to Firebase
                    result = upload_to_firebase(entry)
                    st.success("Your interventions have been accepted and are under review.")
                else:
                    st.error("Please enter a description of the interventions.")

        # Function to read diagnoses from a file
        def read_diagnoses_from_file():
            try:
                with open('dx_list.txt', 'r') as file:
                    diagnoses = [line.strip() for line in file.readlines() if line.strip()]
                return diagnoses
            except Exception as e:
                st.error(f"Error reading dx_list.txt: {e}")
                return []

        # Run the main function
        if __name__ == "__main__":
            main()


