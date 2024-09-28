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

        # Main app function
        def main():
            st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

            # Load user data
            users = load_users()

            # Initialize session state for the necessary variables
            if "page" not in st.session_state:
                st.session_state.page = "welcome"  # Start on the welcome page
            if "user_name" not in st.session_state:
                st.session_state.user_name = ""
            if "unique_code" not in st.session_state:
                st.session_state.unique_code = None
            if "diagnoses" not in st.session_state:
                st.session_state.diagnoses = [""] * 5  # Initialize for 5 diagnoses
            if "selected_buttons" not in st.session_state:
                st.session_state.selected_buttons = [False] * 5  # Track if a button is selected

            # Check which page to display
            if st.session_state.page == "assessment":
                display_assessment()
            elif st.session_state.page == "welcome":
                welcome_page()
            elif st.session_state.page == "login":
                login_page(users)
            elif st.session_state.page == "diagnoses":
                display_diagnoses()

        # Welcome page function
        def welcome_page():
            st.markdown("<h3>Welcome to the Pediatric Clerkship Assessment!</h3>", unsafe_allow_html=True)
            st.markdown("<p>This assessment is designed to evaluate your clinical reasoning skills.</p>", unsafe_allow_html=True)
            st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
            st.markdown("<p>1. Please enter your unique code on the next page.<br>2. Follow the prompts to complete the assessment.</p>", unsafe_allow_html=True)

            if st.button("Next"):
                st.session_state.page = "login"  # Change to login page
                st.rerun()  # Rerun to refresh the view

        # Login page function
        def login_page(users):
            st.markdown("<p>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
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
            st.markdown(f"<h3>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

            # Read and display the text from ptinfo.txt
            document_text = read_text_file("ptinfo.txt")
            if document_text:
                st.markdown("<h2>Patient Information:</h2>", unsafe_allow_html=True)
                st.markdown(f"<div>{document_text.replace('\n', '<br>')}</div>", unsafe_allow_html=True)
            else:
                st.write("No text found in the document.")

            # Load vital signs
            vital_signs = load_vital_signs("vital_signs.txt")

            # Check if vital_signs is not empty before creating checkboxes
            if vital_signs:
                # Vital Signs Title
                title_html = """
                <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 0; color: #2c3e50;">
                    Vital Signs:</h2>
                """
                st.markdown(title_html, unsafe_allow_html=True)

                # Adjust subheader to match font and size, and reduce spacing
                st.markdown("<h4 style='font-family: \"DejaVu Sans\"; font-size: 16px; margin: -20px 0 0 0;'>&nbsp;Of the following vital signs within the intake form, check the vital signs that are abnormal.</h4>", unsafe_allow_html=True)
                #st.markdown("<h2>Vital Signs: Please select </h2>", unsafe_allow_html=True)
                for key, value in vital_signs.items():
                    st.checkbox(f"{key.upper()}: {value}", key=f"{key}_checkbox")

                # Button to upload data to Firebase
                if st.button("Submit"):
                    entry = {
                        'unique_code': st.session_state.unique_code,  # Use the stored unique code
                        **{f"{key}_checkbox": st.session_state.get(f"{key}_checkbox", False) for key in vital_signs.keys()}
                    }
                    result = upload_to_firebase(entry)
                    st.success(result)

                    # Navigate to the diagnoses page
                    st.session_state.page = "diagnoses"
                    st.rerun()  # Rerun to refresh the view
            else:
                st.error("No vital signs data available.")

        # Diagnoses Page function
        def display_diagnoses():
            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS UPDATE
                Based on the information that has been subsequently provided in the above case, please review your initial differential diagnosis list and update it as necessary. 
            """)

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

                    # Filter options based on the search input (You need to define dx_options)
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
                        st.session_state.page = "laboratory_features"  # Move to Laboratory Features page
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        if __name__ == "__main__":
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")



