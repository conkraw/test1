# Diagnoses Page function
def display_diagnoses():
    # Initialize diagnoses if not already done
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5  # Or however many diagnoses you want to allow

    # Check if assessment data exists
    if not st.session_state.assessment_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()  # Load diagnosis options from the file

    st.markdown("""## DIFFERENTIAL DIAGNOSIS UPDATE
                    Based on the information that has been subsequently provided in the above case, please review your initial differential diagnosis list and update it as necessary.""")
    
    # Create columns for each diagnosis input
    cols = st.columns(5)  # Create 5 columns for 5 diagnoses

    for i, col in enumerate(cols):
        current_diagnosis = st.session_state.diagnoses[i]

        with col:
            # Search input for diagnosis
            search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")

            # Filter options based on the search input
            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

            # Display filtered options
            if filtered_options:
                st.write("**Suggestions:**")
                for option in filtered_options[:5]:  # Show a maximum of 5 options
                    button_key = f"select_option_{i}_{option}"
                    if st.button(f"{option}", key=button_key):
                        st.session_state.diagnoses[i] = option
                        st.rerun()  # Refresh the app

    # Button to submit the diagnoses
    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        # Check for empty diagnoses and duplicates
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                # Handle the submission logic here
                st.success("Diagnoses submitted successfully.")
                st.session_state.page = "next_page"  # Change to the next page
                st.rerun()
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")

