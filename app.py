import streamlit as st

# Instructions at the top
st.title("Diagnosis Support Table")
st.write("Please enter the diagnoses and select support options.")

# Input for diagnoses
diagnoses = []
for i in range(5):  # Assuming 5 diagnoses
    diagnosis = st.text_input(f"Diagnosis {i + 1}", key=f"diagnosis_{i}")
    diagnoses.append(diagnosis)

# Create the table
st.write("")  # Add space before the table
for i in range(5):  # Assuming 5 row headers
    cols = st.columns(len(diagnoses) + 1)  # Extra column for row headers
    with cols[0]:
        row_header = st.text_input("", key=f"row_{i}")  # No label for row input
    for diagnosis, col in zip(diagnoses, cols[1:]):
        with col:
            # Ensure unique keys for each dropdown
            st.selectbox("", options=["Support", "No Support"], key=f"select_{i}_{diagnosis}",
                          label_visibility="collapsed")

# Center the headers using markdown
st.markdown("<style>h4 { text-align: center; }</style>", unsafe_allow_html=True)
for diagnosis in diagnoses:
    st.markdown(f"<h4>{diagnosis}</h4>", unsafe_allow_html=True)

# Set the table width to full
st.markdown("<style>div[data-testid='stVerticalBlock'] { width: 100%; }</style>", unsafe_allow_html=True)



