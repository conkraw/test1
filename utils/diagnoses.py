import streamlit as st
from utils.file_operations import read_diagnoses_from_file
from utils.session_management import collect_session_data  #######NEED THIS
from utils.firebase_operations import upload_to_firebase  #######NEED THIS

def display_diagnoses(db, document_id):  #######NEED THIS INCLUDING DB
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

            # Filter options based on the search input
            filtered_options = [dx for dx in dx_options if search_input.lower() in dx.lower()] if search_input else []

            if filtered_options:
                st.write("**Suggestions:**")
                for option in filtered_options[:5]:  # Show up to 5 suggestions
                    button_key = f"select_option_{i}_{option}"
                    if st.button(f"{option}", key=button_key):
                        st.session_state.diagnoses[i] = option
                        st.session_state.selected_buttons[i] = True  # Track selection
                        st.rerun()  # Rerun to update the input field with the selected diagnosis

            # Hide buttons if a diagnosis is already selected
            if current_diagnosis:
                st.write(f"**Selected:** {current_diagnosis}")
            else:
                # Only show suggestions if no diagnosis is selected
                if filtered_options:
                    st.warning("Please select a diagnosis from the suggestions.")

            # Update session state with the current input only if it matches an option
            if current_diagnosis and current_diagnosis in dx_options:
                st.session_state.diagnoses[i] = current_diagnosis

    if st.button("Submit Diagnoses"):
        diagnoses = [d.strip() for d in st.session_state.diagnoses]
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                session_data = collect_session_data() #######NEED THIS
                
                # Create entry with the diagnoses data
                entry = {
                    "diagnoses_s1": diagnoses
                }

                # Upload to Firebase
                try:
                    upload_message = upload_to_firebase(db, 'your_collection_name', document_id, entry)
                    st.success("Diagnoses submitted successfully.")
                except Exception as e:
                    st.error(f"Error uploading data: {e}")

                st.session_state.page = "Intervention Entry"
                st.rerun()  # Rerun to navigate to the next page
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")

