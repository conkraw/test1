# utils/session_management.py

import streamlit as st

#def collect_session_data():
    #session_data = {
        #"unique_code": st.session_state.get("unique_code", ""),
        #"vs_data": st.session_state.get("vs_data", {}),
        #"diagnoses_s1": st.session_state.get("diagnoses_s1", []),
        #"interventions": st.session_state.get("interventions", []),
        #"questions_asked": st.session_state.get("questions_asked", []),
        #"responses": st.session_state.get("responses", []),
        #"examinations": st.session_state.get("examinations", []),
        # Add other session state variables as needed
    #}
    #return session_data

import streamlit as st

def collect_session_data():
    return {
        'page': st.session_state.page,
        'diagnoses': st.session_state.get('diagnoses', []),
        'treatments': st.session_state.get('treatments', []),
        # Add other fields as necessary
    }






