import streamlit as st

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

# Function to read laboratory tests from a file
def read_lab_tests_from_file():
    try:
        with open('labtests.txt', 'r') as file:
            lab_tests = [line.strip() for line in file.readlines() if line.strip()]
        return lab_tests
    except Exception as e:
        st.error(f"Error reading labtests.txt: {e}")
        return []

def display_laboratory_tests():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "laboratory_tests"
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""  

    # Load diagnoses and laboratory tests from files
    dx_options = read_diagnoses_from_file()
    lab_tests = read_lab_tests_from_file()
    dx_options.insert(0, "")  

    st.title("Laboratory Tests App")

    st.markdown("""
        ### LABORATORY TESTS
        Please select up to 5 laboratory tests that influence the differential diagnosis.
    """)

    # Reorder section in the sidebar
    with st.sidebar:
        st.subheader("Reorder Diagnoses")

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
                st.session_state.diagnoses[idx], st.session_state.diagnoses[idx - 1] = (
                    st.session_state.diagnoses[idx - 1], st.session_state.diagnoses[idx]
                )
                st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx - 1]  
            elif move_direction == "Lower Priority" and idx < len(st.session_state.diagnoses) - 1:
                st.session_state.diagnoses[idx], st.session_state.diagnoses[idx + 1] = (
                    st.session_state.diagnoses[idx + 1], st.session_state.diagnoses[idx]
                )
                st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx + 1]  

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
                        index_to_change = st.session_state.diagnoses.index(change_diagnosis)
                        st.session_state.diagnoses[index_to_change] = option
                        st.rerun()  

    # Display laboratory tests
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Laboratory Tests")

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis)

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            selected_lab_test = st.selectbox(
                f"",
                options=[""] + lab_tests,
                key=f"lab_row_{i}",
                label_visibility="collapsed",
            )

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.selectbox(
                    "Assessment for " + diagnosis,
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_{diagnosis}_lab",
                    label_visibility="collapsed"
                )

    # Submit button for laboratory tests
    if st.button("Submit Laboratory Tests"):
        assessments = {}
        for i in range(5):
            for diagnosis in st.session_state.diagnoses:
                assessment = st.session_state[f"select_{i}_{diagnosis}_lab"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'laboratory_test': st.session_state[f"lab_row_{i}"],
                    'assessment': assessment
                })
        
        st.session_state.page = "Radiology Tests"  # Change to the Simple Success page
        st.success("Laboratory tests submitted successfully.")
        st.rerun()  # Rerun to update the app

