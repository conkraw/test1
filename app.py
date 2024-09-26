import streamlit as st

# Instructions at the top
st.markdown("""
    ## Instructions
    Please enter 5 diagnoses in the columns below. For each diagnosis, provide your assessment by selecting either "Support" or "Does not support" from the dropdown menu next to each row.
""")

# Custom CSS to style the dropdowns and increase visibility
st.markdown("""
    <style>
    .stSelectbox > div > div {
        width: 100%;  /* Set dropdowns to take full width */
        font-size: 14px; /* Decrease font size */
    }
    .css-1y2x8r0 {
        width: 100%;  /* Set columns to take up most of the screen */
    }
    .css-1x8g58p {
        max-width: 100%; /* Ensure the main container is wide */
    }
    </style>
    """, unsafe_allow_html=True)

# Custom list of diagnoses
diagnoses = ["Croup", "Tuberculosis", "Cystitis", "Heart Failure", "Urinary Tract Infection"]

# Create a header row for diagnoses
cols = st.columns(len(diagnoses) + 1)
for diagnosis, col in zip(diagnoses, cols[1:]):
    with col:
        st.write(diagnosis)

# Create rows for user inputs and dropdowns
for i in range(5):
    cols = st.columns(len(diagnoses) + 1)
    
    with cols[0]:  # The first column is for row headers
        st.text_input("", key=f"row_{i}", label_visibility="collapsed")  # Row header input without label

    for diagnosis, col in zip(diagnoses, cols[1:]):  # The rest are dropdowns
        with col:
            # Ensure the key is unique by using row index and diagnosis name
            st.selectbox("", options=["Support", "Does not support"], key=f"select_{i}_{diagnosis}",
                          label_visibility="collapsed")




