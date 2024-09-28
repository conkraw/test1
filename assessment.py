import streamlit as st
from utils import read_text_file, load_vital_signs

def display_assessment():
    st.markdown(f"<h3>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

    document_text = read_text_file("ptinfo.txt")
    if document_text:
        st.markdown("<h2>Patient Information:</h2>", unsafe_allow_html=True)
        st.markdown(f"<div>{document_text.replace('\n', '<br>')}</div>", unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

    vital_signs = load_vital_signs("vital_signs.txt")
    if vital_signs:
        display_vital_signs(vital_signs)
    else:
        st.error("No vital signs data available.")

def display_vital_signs(vital_signs):
    st.markdown("<h2>Vital Signs:</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Of the following vital signs within the intake form, check the vital signs that are abnormal.</h4>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])  # Define two columns

    with col2:
        st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)  # Indent using a div

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
