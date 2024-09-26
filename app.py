import streamlit as st

def main():
    st.title("Physical Examination Selection")

    # Create two columns for the prompts
    col1, col2 = st.columns(2)

    # First prompt
    with col1:
        st.markdown("### Please select the parts of physical examination required, in order to exclude some unlikely, but important hypotheses.")
        # Checkbox options
        options1 = [
            "General Appearance", "Eyes", "Ears, Neck, Throat", "Lymph Nodes",
            "Cardiovascular", "Lungs", "Skin", "Abdomen", "Extremities",
            "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
        ]
        selected_exams1 = st.multiselect("Select options:", options1, key="exam_selection_1")

    # Second prompt
    with col2:
        st.markdown("### Please select examinations necessary to confirm the most likely hypothesis and to discriminate between others.")
        # Checkbox options
        selected_exams2 = st.multiselect("Select options:", options1, key="exam_selection_2")

    # Display selected options
    if selected_exams1 or selected_exams2:
        st.subheader("Selected Options:")
        if selected_exams1:
            st.write("From first prompt:", selected_exams1)
        if selected_exams2:
            st.write("From second prompt:", selected_exams2)

if __name__ == "__main__":
    main()
