import streamlit as st
import os

# Function to read tests from a file
def read_tests_from_file(filename):
    try:
        with open(filename, 'r') as file:
            tests = [line.strip() for line in file.readlines() if line.strip()]
        return tests
    except Exception as e:
        st.error(f"Error reading {filename}: {e}")
        return []  # Return an empty list if error occurs

def display_laboratory_tests():
    st.markdown("### LABORATORY TESTING")
    st.write("For each laboratory test that you have chosen, please describe how they would influence your differential diagnosis.")

    lab_options = read_tests_from_file('labtests.txt')
    cols = st.columns(len(st.session_state.laboratory_testing) + 1)
    with cols[0]:
        st.markdown("Laboratory Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.laboratory_testing) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + lab_options,
                key=f"lab_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis in range(5):
            with cols[diagnosis + 1]:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_lab_{diagnosis}",  # Make the key unique
                    label_visibility="collapsed"
                )

    if st.button("Submit Laboratory Testing"):
        assessments = {}
        for i in range(5):
            for diagnosis in range(5):
                assessment = st.session_state[f"select_{i}_lab_{diagnosis}"]
                assessments[f"lab_test_{i}"] = assessment

        st.success("Laboratory testing assessments submitted successfully.")
        st.session_state.page = "Radiological Tests"  # Move to Radiological Tests page
        st.rerun()  # Rerun the app to refresh the page

def display_radiological_tests():
    st.markdown("### RADIOLOGICAL TESTS")
    st.write("For each radiological test that you have chosen, please describe how they would influence your differential diagnosis.")

    rad_options = read_tests_from_file('radtests.txt')
    cols = st.columns(len(st.session_state.radiological_tests) + 1)
    with cols[0]:
        st.markdown("Radiological Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.radiological_tests) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + rad_options,
                key=f"rad_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis in range(5):
            with cols[diagnosis + 1]:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_rad_{diagnosis}",  # Make the key unique
                    label_visibility="collapsed"
                )

    if st.button("Submit Radiological Tests"):
        assessments = {}
        for i in range(5):
            for diagnosis in range(5):
                assessment = st.session_state[f"select_{i}_rad_{diagnosis}"]
                assessments[f"rad_test_{i}"] = assessment

        st.success("Radiological tests assessments submitted successfully.")
        st.session_state.page = "Other Tests"  # Move to Other Tests page
        st.rerun()  # Rerun the app to refresh the page

def display_other_tests():
    # Check if 'other_tests' key is in session state; if not, initialize it
    if 'other_tests' not in st.session_state:
        st.session_state.other_tests = [""] * 5  # Initialize if not present

    st.markdown("### OTHER TESTS")
    st.write("For each other test that you have chosen, please describe how they would influence your differential diagnosis.")

    other_options = read_tests_from_file('othertests.txt')
    cols = st.columns(len(st.session_state.other_tests) + 1)
    with cols[0]:
        st.markdown("Other Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.other_tests) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + other_options,
                key=f"other_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis in range(5):
            with cols[diagnosis + 1]:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_other_{diagnosis}",  # Make the key unique
                    label_visibility="collapsed"
                )

    if st.button("Submit Other Tests"):
        assessments = {}
        for i in range(5):
            for diagnosis in range(5):
                assessment = st.session_state[f"select_{i}_other_{diagnosis}"]
                assessments[f"other_test_{i}"] = assessment

        st.success("Other tests assessments submitted successfully.")
        st.session_state.page = "Simple Success"  # Move to Simple Success page
        st.rerun()  # Rerun the app to refresh the page

# Initialize session state
if 'laboratory_testing' not in st.session_state:
    st.session_state.laboratory_testing = [""] * 5
if 'radiological_tests' not in st.session_state:
    st.session_state.radiological_tests = [""] * 5
if 'other_tests' not in st.session_state:
    st.session_state.other_tests = [""] * 5  # Ensure this is initialized



