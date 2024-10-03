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

def main(db, document_id):
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "historical_features"  
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5
    if 'diagnoses_s2' not in st.session_state:  # New session state for diagnosis order
        st.session_state.diagnoses_s2 = [""] * 5
    if 'historical_features' not in st.session_state:
        st.session_state.historical_features = [""] * 5
    if 'selected_buttons' not in st.session_state:
        st.session_state.selected_buttons = [False] * 5  
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""

    # Load diagnoses from file
    dx_options = read_diagnoses_from_file()
    dx_options.insert(0, "")

    # Title of the app
    st.title("Historical Features App")

    # Update the diagnoses_s2 to match the current order
    st.session_state.diagnoses_s2 = [dx for dx in st.session_state.diagnoses if dx]  # Ensure to remove empty strings

    # Historical Features Page
    if st.session_state.current_page == "historical_features":
        # Sidebar logic remains the same
        with st.sidebar:
            st.subheader("Reorder Diagnoses")
            selected_diagnosis = st.selectbox("Select a diagnosis to move", options=st.session_state.diagnoses)
            move_direction = st.radio("Adjust Priority:", options=["Higher Priority", "Lower Priority"])

            if st.button("Adjust Priority"):
                idx = st.session_state.diagnoses.index(selected_diagnosis)
                if move_direction == "Higher Priority" and idx > 0:
                    st.session_state.diagnoses[idx], st.session_state.diagnoses[idx - 1] = (
                        st.session_state.diagnoses[idx - 1], st.session_state.diagnoses[idx]
                    )
                elif move_direction == "Lower Priority" and idx < len(st.session_state.diagnoses) - 1:
                    st.session_state.diagnoses[idx], st.session_state.diagnoses[idx + 1] = (
                        st.session_state.diagnoses[idx + 1], st.session_state.diagnoses[idx]
                    )
                
                # Update diagnoses_s2 after moving
                st.session_state.diagnoses_s2 = [dx for dx in st.session_state.diagnoses if dx]

        # Change a diagnosis section remains the same...

        # Submit button for historical features
        if st.button("Submit Historical Features"):
            entry = {
                'assessments': {},
                'diagnoses_s2': st.session_state.diagnoses_s2  # Include the reordered diagnoses here
            }

            for i in range(5):
                for diagnosis in st.session_state.diagnoses:  # Keep the original assessments
                    assessment = st.session_state[f"select_{i}_{diagnosis}_hist"]
                    if diagnosis not in entry['assessments']:
                        entry['assessments'][diagnosis] = []
                    entry['assessments'][diagnosis].append({
                        'historical_feature': st.session_state.historical_features[i],
                        'assessment': assessment
                    })

            session_data = collect_session_data()

            # Upload to Firebase using the current diagnosis order in diagnoses_s2
            upload_message = upload_to_firebase(db, 'your_collection_name', document_id, entry)

            st.session_state.page = "Physical Examination Features"  
            st.success("Historical features submitted successfully.")
            st.rerun()  # Rerun to update the app
