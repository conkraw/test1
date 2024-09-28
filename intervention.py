import streamlit as st
from firebase_setup import upload_to_firebase

def upload_intervention():
    st.title("Intervention Description Entry")
    interventions = st.text_area("Interventions Description", height=200)

    if st.button("Upload Intervention"):
        if interventions:
            entry = {
                'interventions': interventions,
                'unique_code': st.session_state.unique_code,
                'assessment_data': st.session_state.assessment_data,
                'diagnoses': st.session_state.diagnoses
            }
            result = upload_to_firebase(entry)
            st.success("Your interventions have been accepted and are under review.")
        else:
            st.error("Please enter a description of the interventions.")
