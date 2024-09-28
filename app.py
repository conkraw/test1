# Function to display the assessment page
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

        # Adjust subheader to match font and size, and reduce spacing
        st.markdown("<h4 style='font-family: \"DejaVu Sans\"; font-size: 18px; margin: -20px 0 0 0;'>&nbsp;Of the following vital signs within the intake form, check the vital signs that are abnormal.</h4>", unsafe_allow_html=True)

        # Patient Vital Signs Table
        col1, col2 = st.columns([1, 2])  # Define two columns

        with col2:
            # Indent labels and checkboxes
            st.markdown("<div style='margin-left: 20px;'>", unsafe_allow_html=True)  # Indent using a div

            # Checkboxes for vital signs
            heart_rate = vital_signs.get("heart_rate", "N/A")
            heart_rate_checkbox = st.checkbox(f"HEART RATE: {heart_rate}", key='heart_rate_checkbox')

            respiratory_rate = vital_signs.get("respiratory_rate", "N/A")
            respiratory_rate_checkbox = st.checkbox(f"RESPIRATORY RATE: {respiratory_rate}", key='respiratory_rate_checkbox')

            blood_pressure = vital_signs.get("blood_pressure", "N/A")
            blood_pressure_checkbox = st.checkbox(f"BLOOD PRESSURE: {blood_pressure}", key='blood_pressure_checkbox')

            pulseox = vital_signs.get("pulseox", "N/A")
            pulseox_checkbox = st.checkbox(f"PULSE OXIMETRY: {pulseox}", key='pulseox_checkbox')

            temperature = vital_signs.get("temperature", "N/A")
            temperature_checkbox = st.checkbox(f"TEMPERATURE: {temperature}", key='temperature_checkbox')

            weight = vital_signs.get("weight", "N/A")
            weight_checkbox = st.checkbox(f"WEIGHT: {weight}", key='weight_checkbox')

            st.markdown("</div>", unsafe_allow_html=True)  # Close the div

        # Button to upload data to Firebase
        if st.button("Submit Assessment"):
            entry = {
                'unique_code': st.session_state.unique_code,  # Use the stored unique code
                'heart_rate': heart_rate_checkbox,
                'respiratory_rate': respiratory_rate_checkbox,
                'blood_pressure': blood_pressure_checkbox,
                'pulseox': pulseox_checkbox,
                'temperature': temperature_checkbox,
                'weight': weight_checkbox,
            }
            result = upload_to_firebase(entry)
            st.success(result)

            # Navigate to the diagnoses page
            st.session_state.page = "diagnoses"
            st.rerun()  # Rerun to refresh the view
    else:
        st.error("No vital signs data available.")


