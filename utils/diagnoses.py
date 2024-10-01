import streamlit as st
from utils.file_operations import read_diagnoses_from_file

def display_diagnoses():
    # Ensure diagnoses are initialized
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5

    # Initialize selected_buttons if not already done
    if 'selected_buttons' not in st.session_state:
        st.session_state.selected_buttons = [False] * 5

    # Check if assessment data exists
    if 'vs_data' not in st.session_state or not st.session_state.vs_data:
        st.error("Please complete the assessment before updating diagnoses.")
        return

    dx_options = read_diagnoses_from_file()

    st.markdown("""## DIFFERENTIAL DIAGNOSIS UPDATE
                    Please review and update your differential diagnosis list as necessary.""")

    cols = st.columns(5)

    for i, col in enumerate(cols):
        current_diagnosis = st.session_state.diagnoses[i]

        with col:
            search_input = st.text_input(f"Diagnosis {i + 1}", value=current_diagnosis, key=f"diagnosis_search_{i}")

            if search_input != current_diagnosis:
                st.session_state.diagnoses[i] = search_input
                st.session_state.selected_buttons[i] = False
                st.rerun()

            # Modify filtering to check for exact matches
            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower() and search_input.strip() != ""] if search_input else []

            if current_diagnosis:
                st.write(f"**Selected:** {current_diagnosis}")

            if not st.session_state.selected_buttons[i]:
                if filtered_options:
                    st.write("**Suggestions:**")
                    for option in filtered_options[:5]:
                        button_key = f"select_option_{i}_{option}"
                        if st.button(f"{option}", key=button_key):
                            st.session_state.diagnoses[i] = option
                            st.session_state.selected_buttons[i] = True
                            st.success(f"Selected diagnosis: {option}")
                            st.rerun()

    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                st.success("Diagnoses submitted successfully.")
                st.session_state.page = "Intervention Entry"
                st.rerun()
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")

if __name__ == "__main__":
    display_diagnoses()


