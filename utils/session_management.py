# utils/session_management.py

import streamlit as st

def collect_session_data():
    session_data = {
        "unique_code": st.session_state.get("unique_code", ""),
        'heart_rate': heart_rate_checkbox,
        'respiratory_rate': respiratory_rate_checkbox,
        'blood_pressure': blood_pressure_checkbox,
        'pulseox': pulseox_checkbox,
        'temperature': temperature_checkbox,
        'weight': weight_checkbox,
        #"diagnoses": st.session_state.get("diagnoses", []),
        # Add other session state variables as needed
    }
    return session_data




