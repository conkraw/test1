import streamlit as st
from utils import read_diagnoses_from_file

def display_diagnoses():
    if not st.session_state.assessment_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()
    
    st.markdown("""
        ## DIFFERENTIAL DIAGNOSIS
        Based on the information that has been provided in the above case, please formulate a differential diagnosis list. During the case, you will be permitted to update as necessary.
    """)

    # Create columns for each diagnosis input
    cols = st.columns(5)  # Create 5 columns for 5 diagnoses

    for i, col in enumerate(cols):
        current_diagnosis = st.session_state.diagnoses[i]

        with col:
            # Search input for diagnosis
            search_input = st.text_input(
                f"Diagnosis {i + 1}",
                value=current_diagnosis,
                key=f"diagnosis_search_{i}"
            )

            # Filter options based on the search input
            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

            # Display filtered options
            if filtered_options and not st.session_state.selected_buttons[i]:
                st.write("**Suggestions:**")
                for option in filtered_options[:5]:  # Show a maximum of 5 options
                    button_key = f"select_option_{i}_{option}"
                    if st.button(f"{option}", key=button_key):
                        st.session_state.diagnoses[i] = option
                        st.session_state.selected_buttons[i] = True  # Mark as selected
                        st.rerun()  # Refresh the app

    # Button to submit the diagnoses
    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                # Prepare the complete entry to upload to Firebase
                complete_entry = {
                    'unique_code': st.session_state.unique_code,
                    'assessment_data': st.session_state.assessment_data,
                    'diagnoses': diagnoses
                }
                st.session_state.complete_entry = complete_entry  # Save entry for later use
                st.session_state.page = "intervention"  # Move to Intervention page
                st.rerun()  # Rerun the app to refresh the page
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")
