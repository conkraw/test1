import streamlit as st

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "historical_features"
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = ["Diagnosis 1", "Diagnosis 2", "Diagnosis 3", "Diagnosis 4", "Diagnosis 5"]
    if 'historical_features' not in st.session_state:
        st.session_state.historical_features = [""] * 5

    st.title("Historical Features App")

    # Historical Features Page
    if st.session_state.current_page == "historical_features":
        st.markdown("### HISTORICAL FEATURES")
        
        for i in range(5):
            st.session_state.historical_features[i] = st.text_input(f"Enter historical feature {i + 1}", key=f"hist_row_{i}")

        if st.button("Submit Historical Features"):
            assessments = {}
            for i in range(5):
                assessment = st.selectbox(f"Assessment for feature {i + 1}", options=["", "Supports", "Does not support"], key=f"select_{i}")

                if assessment:
                    assessments[i] = {
                        'historical_feature': st.session_state.historical_features[i],
                        'assessment': assessment
                    }

            # Debugging output
            st.write("Assessments collected:", assessments)

            if assessments:
                st.success("Historical features submitted successfully.")
                st.session_state.current_page = "Simple Success"
            else:
                st.warning("No assessments were made.")

if __name__ == "__main__":
    main()



