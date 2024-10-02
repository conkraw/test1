# utils/session_management.py

import streamlit as st

def collect_session_data():
    session_data = {
        "unique_code": st.session_state.get("unique_code", ""),
        "vs_data": st.session_state.get("vs_data", {}),
        "diagnoses_s1": st.session_state.get("diagnoses_s1", []),
        "interventions": st.session_state.get("interventions", []),
        "questions_asked": st.session_state.get("questions_asked", []),
        # Add other session state variables as needed
    }
    return session_data




