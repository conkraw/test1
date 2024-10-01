# utils/session_management.py

import streamlit as st

def collect_session_data():
    session_data = {
        "unique_code": st.session_state.get("unique_code", ""),
        "vs_data": st.session_state.get("vs_data", {}),
        #"diagnoses": st.session_state.get("diagnoses", []),
        # Add other session state variables as needed
    }
    return session_data




