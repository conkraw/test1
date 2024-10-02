import streamlit as st
from utils.session_management import collect_session_data  #######NEED THIS
from utils.firebase_operations import upload_to_firebase  

def display_focused_physical_examination(db):
    st.title("Focused Physical Examination Selection")

    # Prompt for excluding hypotheses
    st.markdown("<h5>Please select the parts of physical examination required, in order to exclude some unlikely, but important hypotheses:</h5>", unsafe_allow_html=True)
    options1 = [
        "General Appearance", "Eyes", "Ears, Neck, Throat",
        "Lymph Nodes", "Cardiovascular", "Lungs",
        "Skin", "Abdomen", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
    ]
    selected_exams1 = st.multiselect("Select options:", options1, key="exclude_exams")

    # Prompt for confirming hypotheses
    st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis and to discriminate between others:</h5>", unsafe_allow_html=True)
    selected_exams2 = st.multiselect("Select options:", options1, key="confirm_exams")

    if st.button("Submit"):
        # Prepare the data to upload (if needed)
        entry = {
            'excluded_exams': selected_exams1,
            'confirmed_exams': selected_exams2
        }

        # Change the session state to navigate to the next page
        st.session_state.page = "Physical Examination Components"
        st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
        st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")

