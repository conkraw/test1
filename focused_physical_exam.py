import streamlit as st

def physical_examination_selection():
    st.title("Physical Examination Selection")

    # Prompt for excluding hypotheses
    st.markdown("<h5>Please select the parts of physical examination required:</h5>", unsafe_allow_html=True)
    options1 = [
        "General Appearance", "Eyes", "Ears, Neck, Throat",
        "Lymph Nodes", "Cardiovascular", "Lungs",
        "Skin", "Abdomen", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
    ]
    selected_exams1 = st.multiselect("Select options:", options1, key="exclude_exams")

    # Prompt for confirming hypotheses
    st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis:</h5>", unsafe_allow_html=True)
    selected_exams2 = st.multiselect("Select options:", options1, key="confirm_exams")

    if st.button("Submit"):
        # Display the selected exams
        st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
        st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")
