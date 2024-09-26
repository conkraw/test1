import streamlit as st

# Instructions at the top
st.title("Diagnosis Support Table")
st.write("Please enter the diagnoses and select support options.")

# Container for the table
with st.container():
    # Input for diagnoses
    diagnoses = []
    for i in range(5):  # Assuming 5 diagnoses
        diagnosis = st.text_input(f"Diagnosis {i + 1}", key=f"diagnosis_{i}")
        diagnoses.append(diagnosis)

    # Create the table
    cols = st.columns(len(diagnoses) + 1)  # Extra column for row headers
    for col in cols:
        col.markdown("<div style='text-align: center; font-weight: bold;'> </div>", unsafe_allow_html=True)

    # Row inputs and dropdowns
    for i in range(5):  # Assuming 5 row headers
        cols = st.columns(len(diagnoses) + 1)
        with cols[0]:
            row_header = st.text_input("", key=f"row_{i}")  # No label for row input
        for diagnosis, col in zip(diagnoses, cols[1:]):
            with col:
                st.selectbox("", options=["Support", "No Support"], key=f"select_{i}_{diagnosis}",
                              label_visibility="collapsed")

# Set the table width to full
st.markdown("<style>div[data-testid='stVerticalBlock'] { width: 100%; }</style>", unsafe_allow_html=True)




