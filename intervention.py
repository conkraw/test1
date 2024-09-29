import streamlit as st

def upload_intervention():
    st.title("Intervention Description Entry")
    interventions = st.text_area("Interventions Description", height=200)

    if st.button("Submit Intervention"):
        if interventions:
            st.success("Your intervention has been recorded. Moving to the virtual patient...")
            st.session_state.page = "virtual_patient"  # Navigate to virtual patient page
        else:
            st.error("Please enter a description of the intervention.")

