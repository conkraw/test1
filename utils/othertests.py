import streamlit as st
from utils.session_management import collect_session_data  #######NEED THIS
from utils.firebase_operations import upload_to_firebase  

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

# Function to read other tests from a file
def read_other_tests_from_file():
    try:
        with open('other_tests.txt', 'r') as file:
            other_tests = [line.strip() for line in file.readlines() if line.strip()]
        return other_tests
    except Exception as e:
        st.error(f"Error reading other_tests.txt: {e}")
        return []

def display_other_tests(db, document_id):  # Updated to include db and document_id
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "other_tests"
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""  

    # Load diagnoses and other tests from files
    dx_options = read_diagnoses_from_file()
    other_tests = read_other_tests_from_file()
    dx_options.insert(0, "")  

    st.title("Other Tests")

    st.markdown("""Of the following, please select up to 5 other tests that you would order and describe how they influence the differential diagnosis.""")

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

    # Display other tests
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Other Tests")

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis)

    at_least_one_selected = False  # Track if any test has been selected

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            selected_other_test = st.selectbox(
                f"",
                options=[""] + other_tests,
                key=f"other_row_{i}",
                label_visibility="collapsed",
            )

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                assessment = st.selectbox(
                    "Assessment for " + diagnosis,
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_{diagnosis}_other",
                    label_visibility="collapsed"
                )
                if selected_other_test:  # Check if a test is selected
                    at_least_one_selected = True

    # Submit button for other tests
    if st.button("Submit",key="othertests_submit_button"):
        assessments = {}
        if not at_least_one_selected:
            st.error("Please select at least one test.")
        else:
            for i in range(5):
                for diagnosis in st.session_state.diagnoses:
                    assessment = st.session_state[f"select_{i}_{diagnosis}_other"]
                    if diagnosis not in assessments:
                        assessments[diagnosis] = []
                    assessments[diagnosis].append({
                        'other_test': st.session_state[f"other_row_{i}"],
                        'assessment': assessment
                    })
            
            # Save diagnoses to Firebase
            st.session_state.diagnoses_s5 = [dx for dx in st.session_state.diagnoses if dx]  # Update with current order

            entry = {
                'other_tests': assessments,  # Include other tests data
                'diagnoses_s5': st.session_state.diagnoses_s5  # Include diagnoses_s5 in the entry
            }

            # Upload to Firebase
            #upload_message = upload_to_firebase(db, 'your_collection_name', document_id, entry)
            upload_message = upload_to_firebase(db, document_id, entry)
            
            st.session_state.page = "Results"  # Change to the Simple Success page
            st.success("Other tests submitted successfully.")
            st.rerun()  # Rerun to update the app
