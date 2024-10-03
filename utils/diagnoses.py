def display_diagnoses(db, document_id, save_user_state):
    # Ensure diagnoses are initialized
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5

    # Check if assessment data exists
    if 'vs_data' not in st.session_state or not st.session_state.vs_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()

    st.markdown("""## DIFFERENTIAL DIAGNOSIS
    Please search and select 5 possible diagnoses for the condition you think the patient has in order of likelihood. You will be allowed to alter your choices as you go through the case.""")
    
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            current_diagnosis = st.session_state.diagnoses[i]
            search_input = st.text_input(f"Diagnosis # {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")

            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

            if filtered_options:
                st.write("**Suggestions:**")
                for option in filtered_options[:5]:
                    button_key = f"select_option_{i}_{option}"
                    if st.button(f"{option}", key=button_key):
                        st.session_state.diagnoses[i] = option
                        st.rerun()

            if current_diagnosis:
                st.write(f"**Selected:** {current_diagnosis}")

            if not filtered_options and search_input:
                st.warning("Please select a diagnosis from the suggestions. If there are no suggestions, please alter your search and try again.")

            if current_diagnosis and current_diagnosis in dx_options:
                st.session_state.diagnoses[i] = current_diagnosis

    if st.button("Submit"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                session_data = collect_session_data() 

                # Create entry with the diagnoses data
                entry = {
                    "diagnoses_s1": diagnoses
                }

                # Log the entry before uploading
                st.write("Uploading the following entry to Firebase:")
                st.json(entry)  # Log the entry for debugging

                try:
                    # Upload the data to Firebase
                    upload_message = upload_to_firebase(db, document_id, entry)
                    st.success("Diagnoses submitted successfully.")
                    
                    # Update the session state for last page
                    st.session_state.page = "Intervention Entry"  # Set to next page
                    save_user_state(db)  # Save user state, should reflect the updated page
                    st.rerun()  # Rerun to navigate to the next page
                except Exception as e:
                    st.error(f"Error uploading data: {e}")
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")
