import streamlit as st
import os

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

def main():  # Add a main function to encapsulate the logic
    # Initialize session state
    if 'pe_features' not in st.session_state:
        st.session_state.pe_features = [""] * 5
    if 'selected_buttons' not in st.session_state:
        st.session_state.selected_buttons = [False] * 5  # Track button visibility for each diagnosis
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""  # Initialize selected moving diagnosis

    # Load diagnoses from file
    dx_options = read_diagnoses_from_file()
    dx_options.insert(0, "")  # Add a blank option at the beginning

    # Title of the app
    st.title("Physical Examination Features")

    # Physical Examination Features Page
    st.markdown("""
        ### PHYSICAL EXAMINATION FEATURES
        Please provide up to 5 physical examination features that influence the differential diagnosis.
    """)

    # Reorder section in the sidebar
    with st.sidebar:
        st.subheader("Reorder Diagnoses")

        selected_diagnosis = st.selectbox(
            "Select a diagnosis to move",
            options=dx_options,
            index=0,  # Default to first option
            key="move_diagnosis"
        )

        move_direction = st.radio("Adjust Priority:", options=["Higher Priority", "Lower Priority"], key="move_direction")

        if st.button("Adjust Priority"):
            idx = dx_options.index(selected_diagnosis)
            if move_direction == "Higher Priority" and idx > 0:
                dx_options[idx], dx_options[idx - 1] = (
                    dx_options[idx - 1], dx_options[idx]
                )
            elif move_direction == "Lower Priority" and idx < len(dx_options) - 1:
                dx_options[idx], dx_options[idx + 1] = (
                    dx_options[idx + 1], dx_options[idx]
                )

    # Create columns for each diagnosis input
    cols = st.columns(len(dx_options) + 1)
    with cols[0]:
        st.markdown("Physical Examination Features")

    for diagnosis, col in zip(dx_options, cols[1:]):
        with col:
            st.markdown(diagnosis)

    for i in range(5):
        cols = st.columns(len(dx_options) + 1)
        with cols[0]:
            st.session_state.pe_features[i] = st.text_input("", key=f"pe_row_{i}", label_visibility="collapsed")

        for diagnosis, col in zip(dx_options, cols[1:]):
            with col:
                st.selectbox(
                    "",
                    options=["", "Supports", "Does not support"],
                    key=f"select_{i}_{diagnosis}_pe",
                    label_visibility="collapsed"
                )

    # Submit button for physical examination features
    if st.button("Submit Physical Examination Features"):
        assessments = {}
        for i in range(5):
            for diagnosis in dx_options:
                assessment = st.session_state[f"select_{i}_{diagnosis}_pe"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'physical_examination_feature': st.session_state.pe_features[i],
                    'assessment': assessment
                })

        st.success("Physical examination features submitted successfully.")
        st.session_state.page = "next_page_name"  # Change to the next page you want to navigate to
        st.rerun()  # Rerun to refresh the app

# Call the main function to run the app
if __name__ == "__main__":
    main()
