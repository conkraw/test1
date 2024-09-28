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
        # Logic to display vital signs checkboxes
        display_vital_signs(vital_signs)

def display_vital_signs(vital_signs):
    st.markdown("<h2>Vital Signs:</h2>", unsafe_allow_html=True)
    # Create checkboxes for each vital sign and handle logic here...
    # Add code similar to what was originally in display_assessment
