import streamlit as st
import pandas as pd
import os
import json
from firebase_setup import initialize_firebase, upload_to_firebase

# Initialize Firestore client
try:
    db = initialize_firebase()  # Call the function to initialize Firebase
except ValueError as e:
    st.error(str(e))
    st.stop()  # Stop the app if Firebase initialization fails
except Exception as e:
    st.error(f"Error initializing Firebase: {e}")
    st.stop()

# Cache loading of users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to upload intervention
def upload_intervention():
    st.title("Intervention Description Entry")
    st.header("Describe any interventions that you would currently perform.")
    interventions = st.text_area("Interventions Description", height=200)

    if st.button("Upload Intervention"):
        if interventions:
            entry = {
                'interventions': interventions,
                'unique_code': st.session_state.unique_code,
                'assessment_data': st.session_state.assessment_data,
                'diagnoses': st.session_state.diagnoses
            }
            result = upload_to_firebase(db, entry)
            st.success("Your interventions have been accepted and are under review.")
        else:
            st.error("Please enter a description of the interventions.")

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
        upload_intervention()  # Call the intervention upload function

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
    txt_file_path = "ptinfo.txt"
    document_text = read_text_file(txt_file_path)

    if document_text:
        title_html = """
        <h2>Patient Information:</h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        custom_html = f"""
        <div style="background-color: #ecf0f1; padding: 15px; border-radius: 8px;">
            {document_text.replace('\n', '<br>')}
        </div>
        """
        st.markdown(custom_html, unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

    # Load vital signs
    vital_signs_file = "vital_signs.txt"
    vital_signs = load_vital_signs(vital_signs_file)

    if vital_signs:
        title_html = "<h2>Vital Signs:</h2>"
        st.markdown(title_html, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])  # Define two columns

        with col2:
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

# Load vital signs from a TXT file
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
            search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_{i}")

            if st.button(f"Submit Diagnosis {i + 1}", key=f"submit_diagnosis_{i}"):
                if search_input:
                    st.session_state.diagnoses[i] = search_input  # Update session state
                    st.success(f"Diagnosis {i + 1} updated!")
                else:
                    st.error("Please enter a diagnosis.")

    if st.button("Next to Interventions"):
        st.session_state.page = "intervention"  # Move to Interventions page
        st.rerun()  # Rerun the app to refresh the page

# Function to read diagnoses from a TXT file
def read_diagnoses_from_file():
    diagnoses = []
    try:
        with open("diagnoses.txt", 'r') as file:
            diagnoses = [line.strip() for line in file]
    except FileNotFoundError:
        st.error("Diagnoses file not found. Please check the file path.")
    return diagnoses

if __name__ == "__main__":
    main()

