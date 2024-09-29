import streamlit as st
from utils.file_operations import read_diagnoses_from_file

def display_diagnoses():
    """Display the diagnoses page."""
    if not st.session_state.assessment_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()

    st.markdown("## DIFFERENTIAL DIAGNOSIS UPDATE")
    cols = st.columns(5)

    for i, col in enumerate(cols):
        current_diagnosis = st.session_state.diagnoses[i]

        with col:
            search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")
            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

            if filtered_options and not st.session_state.selected_buttons[i]:
                st.write("**Suggestions:**")
                for option in filtered_options[:5]:
                    button_key = f"select_option_{i}_{option}"
                    if st.button(option, key=button_key):
                        st.session_state.diagnoses[i] = option
                        st.session_state.selected_buttons[i] = True
                        st.rerun()

    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                st.success("Diagnoses submitted successfully!")
                st.session_state.page = "welcome"
                st.rerun()
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")
