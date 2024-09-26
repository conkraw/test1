import streamlit as st

# Initialize session state for diagnoses and table visibility
if 'diagnoses' not in st.session_state:
    st.session_state.diagnoses = []
if 'show_table' not in st.session_state:
    st.session_state.show_table = False

# Title of the app
st.title("Diagnosis Input and Assessment")

# Input Section
if not st.session_state.show_table:
    st.markdown("""
        ## Instructions
        Please enter 5 diagnoses based on what you know about the case.
    """)

    # Create text input fields for each diagnosis
    for i in range(5):
        diagnosis = st.text_input(f"Diagnosis {i + 1}", key=f"diagnosis_{i}")
        st.session_state.diagnoses.append(diagnosis)

    # Button to submit the diagnoses
    if st.button("Submit Diagnoses"):
        # Check if all diagnoses have been entered
        if all(st.session_state.diagnoses):
            st.success("Thank you for your input!")
            st.session_state.show_table = True
        else:
            st.error("Please enter all 5 diagnoses.")

# Assessment Table Section
if st.session_state.show_table:
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


