import streamlit as st

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "historical_features"  # Start on historical features page
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5
    if 'historical_features' not in st.session_state:
        st.session_state.historical_features = [""] * 5
    if 'selected_buttons' not in st.session_state:
        st.session_state.selected_buttons = [False] * 5  
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""  

    # Load diagnoses from file
    dx_options = read_diagnoses_from_file()
    dx_options.insert(0, "")  

    # Title of the app
    st.title("")

    # Historical Features Page
    if st.session_state.current_page == "historical_features":
        st.markdown("""
            ### HISTORICAL FEATURES
            Please provide up to 5 historical features that influence the differential diagnosis.
        """)

        # [Your existing sidebar and feature input code here]

        # Submit button for historical features
        if st.button("Submit Historical Features"):
            assessments = {}
            for i in range(5):
                for diagnosis in st.session_state.diagnoses:
                    assessment = st.session_state[f"select_{i}_{diagnosis}_hist"]
                    if diagnosis not in assessments:
                        assessments[diagnosis] = []
                    assessments[diagnosis].append({
                        'historical_feature': st.session_state.historical_features[i],
                        'assessment': assessment
                    })

            # Debugging statements
            st.write("Current diagnoses:", st.session_state.diagnoses)
            st.write("Historical features submitted:", st.session_state.historical_features)
            st.write("Assessments:", assessments)

            # Change to the next page
            st.session_state.current_page = "Physical Examination Features"  
            st.success("Historical features submitted successfully.")
            st.write("Transitioning to the next page...")  # Debugging line
            st.rerun()

# Call the main function to run the app
if __name__ == "__main__":
    main()


