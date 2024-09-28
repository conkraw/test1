def upload_intervention():
    st.title("Intervention Description Entry")

    # Prompt for user input
    st.header("Describe any interventions that you would currently perform.")
    interventions = st.text_area("Interventions Description", height=200)

    # Button to upload to Firebase
    if st.button("Upload Intervention"):
        if interventions:
            entry = {
                'interventions': interventions,
                'unique_code': st.session_state.unique_code,
                'assessment_data': st.session_state.assessment_data,
                'diagnoses': st.session_state.diagnoses
            }
            # Immediately upload to Firebase
            result = upload_to_firebase(entry)
            st.success("Your interventions have been accepted and are under review.")
        else:
            st.error("Please enter a description of the interventions.")
