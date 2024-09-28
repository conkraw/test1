import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import openai
import time

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
            elif st.session_state.page == "chat":
                chat_with_virtual_patient()  # Chat with virtual patient page

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
                title_html = """
                <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px; color: #2c3e50;">
                    Patient Information:
                </h2>
                """
                st.markdown(title_html, unsafe_allow_html=True)

                custom_html = f"""
                <div style="font-family: 'DejaVu Sans'; font-size: 18px; line-height: 1.5; color: #34495e; background-color: #ecf0f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    {document_text.replace('\n', '<br>')}
                </div>
                """
                st.markdown(custom_html, unsafe_allow_html=True)
            else:
                st.write("No text found in the document.")

            # Load vital signs
            vital_signs_file = "vital_signs.txt"
            vital_signs = load_vital_signs(vital_signs_file)

            # Check if vital_signs is not empty before creating checkboxes
            if vital_signs:
                # Vital Signs Title
                title_html = """
                <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 0; color: #2c3e50;">
                    Vital Signs:</h2>
                """
                st.markdown(title_html, unsafe_allow_html=True)

                # Adjust subheader to match font and size, and reduce spacing
                st.markdown("<h4 style='font-family: \"DejaVu Sans\"; font-size: 18px; margin: -20px 0 0 0;'>&nbsp;Of the following vital signs within the intake form, check the vital signs that are abnormal.</h4>", unsafe_allow_html=True)

                # Patient Vital Signs Table
                col1, col2 = st.columns([1, 2])  # Define two columns

                with col2:
                    # Indent labels and checkboxes
                    st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)  # Indent using a div

                    # Checkboxes for vital signs
                    heart_rate = vital_signs.get("heart_rate", "N/A")
                    heart_rate_checkbox = st.checkbox(f"HEART RATE: {heart_rate}", key='heart_rate_checkbox')

                    respiratory_rate = vital_signs.get("respiratory_rate", "N/A")
                    respiratory_rate_checkbox = st.checkbox(f"RESPIRATORY RATE: {respiratory_rate}", key='respiratory_rate_checkbox')

                    blood_pressure = vital_signs.get("blood_pressure", "N/A")
                    blood_pressure_checkbox = st.checkbox(f"BLOOD PRESSURE: {blood_pressure}", key='blood_pressure_checkbox')

                    pulseox = vital_signs.get("pulseox", "N/A")
                    pulseox_checkbox = st.checkbox(f"PULSE OXIMETRY: {pulseox}", key='pulseox_checkbox')

                    temperature = vital_signs.get("temperature", "N/A")
                    temperature_checkbox = st.checkbox(f"TEMPERATURE: {temperature}", key='temperature_checkbox')

                    weight = vital_signs.get("weight", "N/A")
                    weight_checkbox = st.checkbox(f"WEIGHT: {weight}", key='weight_checkbox')

                    st.markdown("</div>", unsafe_allow_html=True)  # Close the div

                # Button to proceed to the diagnoses page
                if st.button("Next to Diagnoses"):
                    # Store the assessment data in the session state
                    st.session_state.assessment_data = {
                        'unique_code': st.session_state.unique_code,
                        'heart_rate': heart_rate_checkbox,
                        'respiratory_rate': respiratory_rate_checkbox,
                        'blood_pressure': blood_pressure_checkbox,
                        'pulseox': pulseox_checkbox,
                        'temperature': temperature_checkbox,
                        'weight': weight_checkbox,
                    }
                    st.session_state.page = "diagnoses"  # Move to Diagnoses page
                    st.rerun()  # Rerun the app to refresh the page

            else:
                st.error("No vital signs data available.")

        # Diagnoses Page function
        def display_diagnoses():
            # Check if assessment data exists
            if not st.session_state.assessment_data:
                st.error("Please complete the assessment before updating diagnoses.")
                return

            dx_options = read_diagnoses_from_file()  # Load diagnosis options from the file

            st.markdown("""
                ## DIFFERENTIAL DIAGNOSIS
                Based on the information that has been provided in the above case, please formulate a differential diagnosis list. During the case, you will be permitted to update as necessary.
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
                        # Prepare the complete entry to upload to Firebase
                        complete_entry = {
                            'unique_code': st.session_state.unique_code,  # Use the stored unique code
                            'assessment_data': st.session_state.assessment_data,  # Include assessment data
                            'diagnoses': diagnoses  # Include diagnoses
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
                        'diagnoses': st.session_state.diagnoses
                    }
                    # Immediately upload to Firebase
                    result = upload_to_firebase(entry)
                    st.success("Your interventions have been accepted and are under review.")
                    st.session_state.page = "chat"  # Move to chat with virtual patient
                    st.rerun()  # Rerun to refresh the page
                else:
                    st.error("Please enter a description of the interventions.")

        # Function to load the croup document content
        def read_croup_doc():
            from docx import Document
            doc = Document("croup.docx")
            content = []
            for para in doc.paragraphs:
                content.append(para.text)
            return "\n".join(content).lower()  # Convert to lower case for easier matching

        # Load the document content
        croup_info = read_croup_doc()

        # Set up OpenAI API key from Streamlit secrets
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        # Function to get response from ChatGPT
        def get_chatgpt_response(user_input):
            user_input_lower = user_input.lower()  # Normalize the user input to lower case

            # Check if the question is a medical question based on croup_info
            if user_input_lower in croup_info:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": "Role play a parent whose child is experiencing croup. Answer medical inquiries based on the croup document."}
                    ]
                )
                return response['choices'][0]['message']['content']
            else:
                # Handle unknown medical inquiries naturally
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": user_input},
                        {"role": "assistant", "content": "If you cannot answer the medical inquiry from the croup document, please respond naturally as a concerned parent."}
                    ]
                )
                return response['choices'][0]['message']['content']

        # Function to chat with the virtual patient
        def chat_with_virtual_patient():
            st.title("Virtual Patient Chat")

            # Instructions for the user
            st.info(
                "You will have the opportunity to perform a history and ask for important physical examination details using a virtual patient/parent. "
                "When you are ready, please start asking questions. You will be limited to 15 minutes. "
                "Alternatively, you may end the session if you click 'End Session'."
            )

            # Session state to track time and session status
            if 'start_time' not in st.session_state:
                st.session_state.start_time = time.time()
                st.session_state.questions_responses = []  # Initialize a list to store questions and responses

            # Calculate elapsed time
            elapsed_time = (time.time() - st.session_state.start_time) / 60  # Convert to minutes

            # Display patient information
            if elapsed_time < 15:
                with st.form("question_form"):
                    user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
                    submit_button = st.form_submit_button("Submit")

                    if submit_button and user_input:
                        virtual_patient_response = get_chatgpt_response(user_input)
                        st.write(f"Virtual Patient: {virtual_patient_response}")

                        # Store the question and response
                        st.session_state.questions_responses.append({'question': user_input, 'response': virtual_patient_response})

                        # Upload the question and response to Firebase (if you want to do it instantly)
                        # upload_to_firebase({'question': user_input, 'response': virtual_patient_response})

                # End session button
                if st.button("End Session"):
                    end_session()

            else:
                st.warning("Session time is up. Please end the session.")
                if st.button("End Session"):
                    end_session()

        def end_session():
            # Upload all questions and responses along with other data to Firebase
            complete_entry = {
                'unique_code': st.session_state.unique_code,
                'assessment_data': st.session_state.assessment_data,
                'diagnoses': st.session_state.diagnoses,
                'questions_responses': st.session_state.questions_responses  # Include questions and responses
            }
            
            # Upload the complete entry to Firebase
            upload_to_firebase(complete_entry)
            st.success("Session ended. Your data has been uploaded.")
            
            # Reset session state for a new session
            st.session_state.start_time = None
            st.session_state.questions_responses = []  # Reset questions and responses list

        if __name__ == "__main__":
            main()

    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")


