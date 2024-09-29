import streamlit as st
from utils.file_operations import read_text_file, load_vital_signs

def display_assessment():
    st.markdown(f"<h3 style='font-family: \"DejaVu Sans\";'>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

    # Read and display the text from ptinfo.txt
    txt_file_path = "ptinfo.txt"
    document_text = read_text_file(txt_file_path)

    if document_text:
        title_html = """
        <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px; color: #2c3e50;">
            Patient Information:
        </h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        custom_html = f"""
        <div style="font-family: 'DejaVu Sans'; font-size: 18px; line-height: 1.5; color: #34495e; background-color: #ecf0f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {document_text.replace('\n', '<br>')}
        </div>
        """
        st.markdown(custom_html, unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

    # Load vital signs
    vital_signs_file = "vital_signs.txt"
    vital_signs = load_vital_signs(vital_signs_file)

    # Check if vital_signs is not empty before creating checkboxes
    if vital_signs:
        # Vital Signs Title
        title_html = """
        <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 0; color: #2c3e50;">
            Vital Signs:</h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        st.markdown("<h4 style='font-family: \"DejaVu Sans\"; font-size: 18px; margin: -20px 0 0 0;'>&nbsp;Of the following vital signs within the intake form, check the vital signs that are abnormal.</h4>", unsafe_allow_html=True)

        # Patient Vital Signs Table
        col1, col2 = st.columns([1, 2])  # Define two columns

        with col2:
            # Indent labels and checkboxes
            st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)

            # Checkboxes for vital signs
            for key in vital_signs:
                st.checkbox(f"{key.upper()}: {vital_signs[key]}", key=f"{key}_checkbox")

            st.markdown("</div>", unsafe_allow_html=True)  # Close the div

        # Button to proceed to the diagnoses page
        if st.button("Next to Diagnoses"):
            # Store the assessment data in the session state
            st.session_state.assessment_data = {
                'unique_code': st.session_state.unique_code,
                **{key: st.session_state.get(f"{key}_checkbox", False) for key in vital_signs}
            }
            st.session_state.page = "diagnoses"  # Move to Diagnoses page
            st.rerun()  # Rerun the app to refresh the page
    else:
        st.error("No vital signs data available.")

