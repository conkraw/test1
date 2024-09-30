import streamlit as st

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        print("Diagnoses loaded successfully:", diagnoses)  # Debugging statement
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

def main():
    # Initialize session state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "historical_features"  # Start on historical features page
        print("Initialized current_page to historical_features")  # Debugging statement
    if 'diagnoses' not in st.session_state:
        st.session_state.diagnoses = [""] * 5
        print("Initialized diagnoses state")  # Debugging statement
    if 'historical_features' not in st.session_state:
        st.session_state.historical_features = [""] * 5
        print("Initialized historical_features state")  # Debugging statement
    if 'selected_buttons' not in st.session_state:
        st.session_state.selected_buttons = [False] * 5  
        print("Initialized selected_buttons state")  # Debugging statement
    if 'selected_moving_diagnosis' not in st.session_state:
        st.session_state.selected_moving_diagnosis = ""  
        print("Initialized selected_moving_diagnosis state")  # Debugging statement

    # Load diagnoses from file
    dx_options = read_diagnoses_from_file()
    dx_options.insert(0, "")  
    print("Diagnosis options:", dx_options)  # Debugging statement

    # Title of the app
    st.title("")

    # Historical Features Page
    if st.session_state.current_page == "historical_features":
        st.markdown("""
            ### HISTORICAL FEATURES
            Please provide up to 5 historical features that influence the differential diagnosis.
        """)

        # Reorder section in the sidebar
        with st.sidebar:
            st.subheader("Reorder Diagnoses")

            selected_diagnosis = st.selectbox(
                "Select a diagnosis to move",
                options=st.session_state.diagnoses,
                index=st.session_state.diagnoses.index(st.session_state.selected_moving_diagnosis) if st.session_state.selected_moving_diagnosis in st.session_state.diagnoses else 0,
                key="move_diagnosis"
            )
            print(f"Selected diagnosis to move: {selected_diagnosis}")  # Debugging statement

            move_direction = st.radio("Adjust Priority:", options=["Higher Priority", "Lower Priority"], key="move_direction")

            if st.button("Adjust Priority"):
                idx = st.session_state.diagnoses.index(selected_diagnosis)
                print(f"Adjusting priority for: {selected_diagnosis}, direction: {move_direction}")  # Debugging statement
                if move_direction == "Higher Priority" and idx > 0:
                    st.session_state.diagnoses[idx], st.session_state.diagnoses[idx - 1] = (
                        st.session_state.diagnoses[idx - 1], st.session_state.diagnoses[idx]
                    )
                    st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx - 1]
                elif move_direction == "Lower Priority" and idx < len(st.session_state.diagnoses) - 1:
                    st.session_state.diagnoses[idx], st.session_state.diagnoses[idx + 1] = (
                        st.session_state.diagnoses[idx + 1], st.session_state.diagnoses[idx]
                    )
                    st.session_state.selected_moving_diagnosis = st.session_state.diagnoses[idx + 1]  

            # Change a diagnosis section
            st.subheader("Change a Diagnosis")
            change_diagnosis = st.selectbox(
                "Select a diagnosis to change",
                options=st.session_state.diagnoses,
                key="change_diagnosis"
            )
            print(f"Change diagnosis selected: {change_diagnosis}")  # Debugging statement

            new_diagnosis_search = st.text_input("Search for a new diagnosis", "")
            if new_diagnosis_search:
                new_filtered_options = [dx for dx in dx_options if new_diagnosis_search.lower() in dx.lower() and dx not in st.session_state.diagnoses]
                if new_filtered_options:
                    st.write("**Available Options:**")
                    for option in new_filtered_options:
                        if st.button(f"{option}", key=f"select_new_{option}"):
                            index_to_change = st.session_state.diagnoses.index(change_diagnosis)
                            st.session_state.diagnoses[index_to_change] = option
                            print(f"Changed diagnosis: {change_diagnosis} to {option}")  # Debugging statement
                            st.rerun()  

        # Display historical features
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            st.markdown("Historical Features")

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.markdown(diagnosis)

        for i in range(5):
            cols = st.columns(len(st.session_state.diagnoses) + 1)
            with cols[0]:
                st.session_state.historical_features[i] = st.text_input("Enter historical feature", key=f"hist_row_{i}")

            for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
                with col:
                    st.selectbox(
                        "Assessment for " + diagnosis,
                        options=["", "Supports", "Does not support"],
                        key=f"select_{i}_{diagnosis}_hist",
                        label_visibility="collapsed"
                    )

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

            print("Assessments collected:", assessments)  # Debugging statement
            st.session_state.current_page = "Simple Success"  # Change to the next page
            st.success("Historical features submitted successfully.")
            print("Transitioning to Simple Success page.")  # Debugging statement
            st.rerun()

# Call the main function to run the app
if __name__ == "__main__":
    main()


