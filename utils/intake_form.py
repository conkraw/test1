# utils/intake_form.py

import streamlit as st
from utils.file_operations import read_text_file, load_vital_signs
from utils.session_management import collect_session_data 
from utils.firebase_operations import upload_to_firebase 

def display_intake_form(db):
    st.markdown(f"<h3 style='font-family: \"DejaVu Sans\";'>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

    # Read and display the text from ptinfo.txt
    document_text = read_text_file("ptinfo.txt")
    if document_text:
        st.markdown(f"<div style='font-family: \"DejaVu Sans\";'>{document_text}</div>", unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

    # Load vital signs
    vital_signs = load_vital_signs("vital_signs.txt")
    if vital_signs:
        st.markdown("<h2>Vital Signs:</h2>", unsafe_allow_html=True)
        
        # Create checkboxes for each vital sign
        heart_rate_checkbox = st.checkbox(f"HEART RATE: {vital_signs.get('heart_rate', 'N/A')}", key='heart_rate_checkbox')
        respiratory_rate_checkbox = st.checkbox(f"RESPIRATORY RATE: {vital_signs.get('respiratory_rate', 'N/A')}", key='respiratory_rate_checkbox')
        blood_pressure_checkbox = st.checkbox(f"BLOOD PRESSURE: {vital_signs.get('blood_pressure', 'N/A')}", key='blood_pressure_checkbox')
        pulseox_checkbox = st.checkbox(f"PULSE OXIMETRY: {vital_signs.get('pulseox', 'N/A')}", key='pulseox_checkbox')
        temperature_checkbox = st.checkbox(f"TEMPERATURE: {vital_signs.get('temperature', 'N/A')}", key='temperature_checkbox')
        weight_checkbox = st.checkbox(f"WEIGHT: {vital_signs.get('weight', 'N/A')}", key='weight_checkbox')

        # Button to proceed to the diagnoses page
        if st.button("Next"):
            # Collect data for upload
            st.session_state.vs_data = {
                'unique_code': st.session_state.unique_code,
                'heart_rate': heart_rate_checkbox,
                'respiratory_rate': respiratory_rate_checkbox,
                'blood_pressure': blood_pressure_checkbox,
                'pulseox': pulseox_checkbox,
                'temperature': temperature_checkbox,
                'weight': weight_checkbox,
            }
    
            # Upload to Firebase using session management function
            upload_message = upload_to_firebase(db, st.session_state.vs_data) 
            st.success("Data uploaded successfully!")  # Optional success message
            
            # Move to Diagnoses page
            st.session_state.page = "diagnoses"  
            st.rerun()  # Rerun the app to refresh the page
    else:
        st.error("No vital signs data available.")

