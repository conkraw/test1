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

# Set the page config to normal
st.set_page_config(layout="wide")

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "diagnoses"
if 'diagnoses' not in st.session_state:
    st.session_state.diagnoses = [""] * 5
if 'historical_features' not in st.session_state:
    st.session_state.historical_features = [""] * 5
if 'selected_buttons' not in st.session_state:
    st.session_state.selected_buttons = [False] * 5  # Track button visibility for each diagnosis
if 'selected_moving_diagnosis' not in st.session_state:
    st.session_state.selected_moving_diagnosis = ""  # Initialize selected moving diagnosis

# Load diagnoses from file
dx_options = read_diagnoses_from_file()
dx_options.insert(0, "")  # Add a blank option at the beginning

# Title of the app
st.title("")

# Diagnoses Page
if st.session_state.current_page == "diagnoses":
    st.markdown("""
        ## DIFFERENTIAL DIAGNOSIS UPDATE
        Based on the information that has been subsequently provided in the above case, please review your initial differential diagnosis list and update it as necessary.
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
        # Check for empty diagnoses and duplicates
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):
                st.session_state.current_page = "historical_features"  # Move to Historical Features page
                st.rerun()  # Rerun the app to refresh the page
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please select all 5 diagnoses.")

# Historical Features Page
elif st.session_state.current_page == "historical_features":
    st.markdown("""
        ### HISTORICAL FEATURES
        Please provide up to 5 historical features that influence the differential diagnosis.
    """)

    # Reorder section in the sidebar
    with st.sidebar:
        st.subheader("Reorder Diagnoses")

        # Default to the currently selected diagnosis or the first one if none is selected
        selected_diagnosis = st.selectbox(
            "Select a diagnosis to move",
            options=st.session_state.diagnoses,
            index=st.session_state.diagnoses.index(st.session_state.selected_moving_diagnosis) if st.session_state.selected_moving_diagnosis in st.session_state.diagnoses else 0,
            key="move_diagnosis"
        )

        move_direction = st.radio("Adjust Priority:", options=["Higher Priority", "Lower Priority"], key="move_direction")

        if st.button("Adjust Priority"):
            idx = st.session_state.diagnoses.index(selected_diagnosis)
            if move_direction == "Higher Priority" and idx > 0:
                # Move up by one position
                st.session_state.diagnoses[idx], st.session_state.diagnoses[idx - 1] = (
                    st.session_state.diagnoses[idx - 1], st.session_state.diagnoses[idx]
                )
                st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx - 1]  # Update selected diagnosis
            elif move_direction == "Lower Priority" and idx < len(st.session_state.diagnoses) - 1:
                # Move down by one position
                st.session_state.diagnoses[idx], st.session_state.diagnoses[idx + 1] = (
                    st.session_state.diagnoses[idx + 1], st.session_state.diagnoses[idx]
                )
                st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx + 1]  # Update selected diagnosis

        # Change a diagnosis section
        st.subheader("Change a Diagnosis")
        change_diagnosis = st.selectbox(
            "Select a diagnosis to change",
            options=st.session_state.diagnoses,
            key="change_diagnosis"
        )

        new_diagnosis_search = st.text_input("Search for a new diagnosis", "")
        if new_diagnosis_search:
            new_filtered_options = [dx for dx in dx_options if new_diagnosis_search.lower() in dx.lower() and dx not in st.session_state.diagnoses]
            if new_filtered_options:
                st.write("**Available Options:**")
                for option in new_filtered_options:
                    if st.button(f"{option}", key=f"select_new_{option}"):
                        # Change selected diagnosis to the new one
                        index_to_change = st.session_state.diagnoses.index(change_diagnosis)
                        st.session_state.diagnoses[index_to_change] = option
                        st.rerun()  # Rerun to update the displayed diagnoses

    # Create columns for each diagnosis input
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Historical Features")

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis)

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            st.session_state.historical_features[i] = st.text_input("", key=f"hist_row_{i}", label_visibility="collapsed")

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.selectbox(
                    "",
                    options=["", "Supports", "Does not support"],
                    key=f"select_{i}_{diagnosis}_hist",
                    label_visibility="collapsed"
                )

    # Submit button for historical features
    if st.button("Submit Historical Features"):
        assessments = {}
        for i in range(5):
            for diagnosis in st.session_state.diagnoses:
                assessment = st.session_state[f"select_{i}_{diagnosis}_hist"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'historical_feature': st.session_state.historical_features[i],
                    'assessment': assessment
                })

        st.success("Historical features submitted successfully.")



