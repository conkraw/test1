import streamlit as st

# Initialize session state for diagnoses and submission status
if 'diagnoses' not in st.session_state:
    st.session_state.diagnoses = [""] * 5  # Initialize with empty strings for 5 diagnoses
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Title of the app
st.title("")

# Input Section
if not st.session_state.submitted:
    st.markdown("""
        ## DIFFERENTIAL DIAGNOSIS
        Based on the information provided in the above case, please provide 5 possible diagnoses that you would consider when prompted by your attending? Please do not provide duplicate diagnoses. 
    """)

    # Create text input fields for each diagnosis
    for i in range(5):
        st.session_state.diagnoses[i] = st.text_input(f"Diagnosis {i + 1}", value=st.session_state.diagnoses[i], key=f"diagnosis_{i}")

    # Button to submit the diagnoses
    if st.button("Submit Diagnoses"):
        # Check if all diagnoses have been entered
        diagnoses = [d.strip() for d in st.session_state.diagnoses]  # Strip whitespace
        if all(diagnosis for diagnosis in diagnoses):
            if len(diagnoses) == len(set(diagnoses)):  # Check for duplicates
                st.session_state.submitted = True  # Move to the assessment table
                st.rerun()  # Rerun the app to clear the inputs and show the table
            else:
                st.error("Please do not provide duplicate diagnoses.")
        else:
            st.error("Please enter all 5 diagnoses.")

# Assessment Table Section
if st.session_state.submitted:
    st.markdown("### Assessment Table")

    # Custom CSS to style the dropdowns
    st.markdown("""
        <style>
        .stSelectbox > div > div {
            width: 100%;  /* Set dropdowns to take full width */
            font-size: 14px; /* Decrease font size */
        }
        </style>
        """, unsafe_allow_html=True)

    # Create a header row for diagnoses
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.write(diagnosis)

    # Create rows for user inputs and dropdowns
    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        
        with cols[0]:  # The first column is for row headers
            st.text_input("", key=f"row_{i}", label_visibility="collapsed")  # Row header input without label

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):  # The rest are dropdowns
            with col:
                # Ensure the key is unique by using row index and diagnosis name
                st.selectbox("", options=["Support", "Does not support"], key=f"select_{i}_{diagnosis}",
                              label_visibility="collapsed")

