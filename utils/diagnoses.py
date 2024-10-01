import streamlit as st
from utils.file_operations import read_diagnoses_from_file

def display_diagnoses():
    # Ensure diagnoses are initialized
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5

    # Check if assessment data exists
    if 'vs_data' not in st.session_state or not st.session_state.vs_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()

    st.markdown("""## DIFFERENTIAL DIAGNOSIS UPDATE
                    Please review and update your differential diagnosis list as necessary.""")

    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            current_diagnosis = st.session_state.diagnoses[i]
            search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")

            # Logic to determine if buttons should be shown
            if current_diagnosis and search_input == current_diagnosis:
                st.write(f"**Selected:** {current_diagnosis}")
                st.warning("Diagnosis already selected. Enter a new diagnosis to see suggestions.")
            else:
                # Update the diagnosis in session state if the input changes
                st.session_state.diagnoses[i] = search_input

                # Filter options based on the search input
                filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

                if filtered_options:
                    st.write("**Suggestions:**")
                    for option in filtered_options[:5]:  # Show up to 5 suggestions
                        button_key = f"select_option_{i}_{option}"
                        if st.button(f"{option}", key=button_key):
                            st.session_state.diagnoses[i] = option
                            st.experimental_rerun()  # Rerun to update the input field with the selected diagnosis

    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                st.success("Diagnoses submitted successfully.")
                st.session_state.page = "Intervention Entry"
                st.experimental_rerun()  # Rerun to navigate to the next page
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")

if __name__ == "__main__":
    display_diagnoses()

