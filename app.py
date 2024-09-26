import streamlit as st

# Custom CSS to widen the dropdowns and increase table size
st.markdown("""
    <style>
    .stSelectbox > div > div {
        width: 200px;  /* Adjust width of dropdowns */
    }
    .stButton, .stNumberInput, .stSelectbox {
        font-size: 18px; /* Increase font size for better visibility */
    }
    .css-1y2x8r0 {
        width: 100%;  /* Set columns to take full width */
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for user inputs
with st.sidebar:
    num_columns = st.number_input("Number of Diagnoses (Columns)", 1, 10, 5, 1)
    num_rows = st.number_input("Number of Row Headers", 1, 10, 3, 1)

# Define list of diagnoses and row headers
diagnoses = [f"Diagnosis {i+1}" for i in range(num_columns)]
row_headers = [f"Row {i+1}" for i in range(num_rows)]

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
            # Larger dropdowns for better visibility
            selection = st.selectbox("", options=["Support", "Does not support"], key=f"{row}_{diagnosis}", 
                                      label_visibility="collapsed")

# Add a footer or any additional information if needed
st.markdown("## Support Matrix")

