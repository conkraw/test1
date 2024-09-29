# utils/focused_physical_examination.py

import streamlit as st

def display_focused_physical_examination():
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

    #if st.button("End Session"):
    #    st.session_state.start_time = None
    #    st.session_state.page = "Focused Physical Examination"
    #    st.rerun()
    #    st.write("Redirecting to a new screen...")

    
    if st.button("Submit"):
        # Prepare the data to upload
        entry = {
            'excluded_exams': selected_exams1,
            'confirmed_exams': selected_exams2
        }
        # Upload to Firebase
        #result = upload_to_firebase(entry)
        #st.success(result)
        st.session_state.page = "Physical Examination Components"
        st.rerun()
        st.write("Redirecting to a new screen...")

        st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
        st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")
