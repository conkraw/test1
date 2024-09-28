import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import openai

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

        # Function to read diagnoses from file
        def read_diagnoses_from_file():
            try:
                with open('dx_list.txt', 'r') as file:
                    diagnoses = [line.strip() for line in file.readlines() if line.strip()]
                return diagnoses
            except Exception as e:
                st.error(f"Error reading dx_list.txt: {e}")
                return []

        # Function to get response from OpenAI
        def get_chatgpt_response(user_input):
            openai.api_key = st.secrets["OPENAI_API_KEY"]  # Ensure your OpenAI key is set in secrets
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": "You are a virtual patient providing medical information."}
                ]
            )
            return response['choices'][0]['message']['content']

        # Main app function
        def main():
            st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

            # Load user data
            users = load_users()

            # Initialize session state for page if not already done
            if "page" not in st.session_state:
                st.session_state.page = "welcome"  # Start on the welcome page
                st.session_state.diagnoses = [""] * 5  # Initialize empty diagnoses
                st.session_state.selected_buttons = [False] * 5  # Track selection status
                st.session_state.assessment_data = {}  # Store assessment data
                st.session_state.questions_responses = []  # Store questions and responses
                st.session_state.start_time = None  # For timing the session

            # Check which page to display
            if st.session_state.page == "assessment":
                display_assessment()
            elif st.session_state.page == "welcome":
                welcome_page()
            elif st.session_state.page == "login":
                login_page(users)
            elif st.session_state.page == "diagnoses":
                display_diagnoses()
            elif st.session_state.page == "intervention":
                upload_intervention()  # New intervention page

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
                            st.session_state.start_time = time.time()  # Start session timer
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
            txt_file_path = "ptinfo.txt"
            document_text = read_text_file(txt_file_path)

            if document_text:
                st.markdown("<h2>Patient Information:</h2>", unsafe_allow_html=True)
                st.markdown(document_text.replace('\n', '<br>'), unsafe_allow_html=True)

            # Load vital signs
            vital_signs_file = "vital_signs.txt"
            vital_signs = load_vital_signs(vital_signs_file)

            # Display vital signs
            if vital_signs:
                st.markdown("<h2>Vital Signs:</h2>", unsafe_allow_html=True)
                for key, value in vital_signs.items():
                    st.checkbox(f"{key}: {value}", key=key)

            # Chat with virtual patient
            st.markdown("<h3>Chat with Virtual Patient:</h3>", unsafe_allow_html=True)
            if st.button("Start Chat"):
                st.session_state.start_time = time.time()  # Reset timer
                st.session_state.questions_responses = []  # Clear previous responses
                st.session_state.chat_active = True
            
            if st.session_state.chat_active:
                user_input = st.text_input("Ask a question about the patient:")
                if st.button("Submit"):
                    if user_input:
                        response = get_chatgpt_response(user_input)
                        st.write(f"Virtual Patient: {response}")
                        st.session_state.questions_responses.append({'question': user_input, 'response': response})

                # Timer check
                elapsed_time = (time.time() - st.session_state.start_time) / 60  # Convert to minutes
                if elapsed_time >= 15:
                    st.warning("Session time is up. Please proceed to the next step.")

            # Button to proceed to the diagnoses page
            if st.button("Next to Diagnoses"):
                st.session_state.page = "diagnoses"  # Move to Diagnoses page
                st.session_state.assessment_data = {
                    'unique_code': st.session_state.unique_code,
                    'questions_responses': st.session_state.questions_responses  # Include chat data
                }
                st.rerun()  # Rerun to refresh the page

        # Diagnoses Page function
        def display_diagnoses():
            # Check if assessment data exists
            if not st.session_state.assessment_data:
                st.error("Please complete the assessment before updating diagnoses.")
                return

            dx_options = read_diagnoses_from_file()  # Load diagnosis options from the file

            st.markdown("## DIFFERENTIAL DIAGNOSIS")
            cols = st.columns(5)  # Create 5 columns for 5 diagnoses

            for i, col in enumerate(cols):
                current_diagnosis = st.session_state.diagnoses[i]

                with col:
                    # Search input for diagnosis
                    search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")

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
                        complete_entry = {
                            'unique_code': st.session_state.unique_code,
                            'assessment_data': st.session_state.assessment_data,
                            'diagnoses': diagnoses
                        }
                        st.session_state.complete_entry = complete_entry  # Save entry for later use
                        st.session_state.page = "intervention"  # Move to Intervention page
                        st.rerun()  # Rerun the app to refresh the page
                    else:
                        st.error("Please do not provide duplicate diagnoses.")
                else:
                    st.error("Please select all 5 diagnoses.")

        # New function to upload intervention
        def upload_intervention():
            st.title("Intervention Description Entry")

            # Prompt for user input
            st.header("Describe any interventions that you would currently perform.")
            interventions = st.text_area("Interventions Description", height=200)

            # Button to upload to Firebase
            if st.button("Upload Intervention"):
                if interventions:
                    entry = {
                        'interventions': interventions,
                        'unique_code': st.session_state.unique_code,
                        'assessment_data': st.session_state.assessment_data,
                        'diagnoses': st.session_state.diagnoses,
                        'questions_responses': st.session_state.questions_responses  # Include chat data
                    }
                    # Immediately upload to Firebase
                    result = upload_to_firebase(entry)
                    st.success("Your interventions have been accepted and are under review.")
                else:
                    st.error("Please enter a description of the interventions.")

        if __name__ == "__main__":
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

