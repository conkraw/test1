import streamlit as st

# Set page layout to wide
st.set_page_config(layout="wide")

def main():
    st.title("Physical Examination Selection")

    # Smaller font for prompts
    st.markdown("<h5>Please select the parts of physical examination required, in order to exclude some unlikely, but important hypotheses:</h5>", unsafe_allow_html=True)
    
    # Checkbox options
    options1 = [
        "General Appearance", "Eyes", "Ears, Neck, Throat",
        "Lymph Nodes", "Cardiovascular", "Lungs",
        "Skin", "Abdomen", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary"
    ]
    
    # First prompt with multiselect
    selected_exams1 = st.multiselect("Select options:", options1, key="exclude_exams")

    # Second prompt
    st.markdown("<h5>Please select examinations necessary to confirm the most likely hypothesis and to discriminate between others:</h5>", unsafe_allow_html=True)
    
    # Second multiselect
    selected_exams2 = st.multiselect("Select options:", options1, key="confirm_exams")

    if st.button("Submit"):
        st.success(f"Examinations selected to exclude hypotheses: {selected_exams1}")
        st.success(f"Examinations selected to confirm hypotheses: {selected_exams2}")

if __name__ == "__main__":
    main()

