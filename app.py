import streamlit as st

# Custom CSS to style the dropdowns and set a fixed column width
st.markdown("""
    <style>
    .stSelectbox > div > div {
        width: 150px;  /* Fixed width for dropdowns */
    }
    .stButton, .stNumberInput, .stSelectbox {
        font-size: 18px; /* Increase font size for better visibility */
    }
    .css-1y2x8r0 {
        width: 115%;  /* Set columns to take up most of the screen */
    }
    .css-1x8g58p {
        max-width: 115%; /* Ensure the main container is wide */
    }
    </style>
    """, unsafe_allow_html=True)

# Define fixed lists of diagnoses and row headers
diagnoses = [f"Diagnosis {i+1}" for i in range(5)]  # 5 fixed diagnoses
row_headers = [f"Row {i+1}" for i in range(5)]  # 5 fixed rows

# Create a header row for diagnoses
cols = st.columns(len(diagnoses) + 1)
for diagnosis, col in zip(diagnoses, cols[1:]):
    with col:
        st.write(diagnosis)

# Create rows for user inputs and dropdowns
for row in row_headers:
    cols = st.columns(len(diagnoses) + 1)
    with cols[0]:  # The first column is for row headers
        st.write(row)
    
    for diagnosis, col in zip(diagnoses, cols[1:]):  # The rest are dropdowns
        with col:
            # Dropdown for user selection
            selection = st.selectbox("", options=["Support", "Does not support"], key=f"{row}_{diagnosis}", 
                                      label_visibility="collapsed")



