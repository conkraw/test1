import streamlit as st
import os
import json

# Function to read diagnoses from a file
def read_diagnoses_from_file():
    try:
        with open('dx_list.txt', 'r') as file:
            diagnoses = [line.strip() for line in file.readlines() if line.strip()]
        return diagnoses
    except Exception as e:
        st.error(f"Error reading dx_list.txt: {e}")
        return []

# Function to read tests from a file
def read_tests_from_file(filename):
    try:
        with open(filename, 'r') as file:
            tests = [line.strip() for line in file.readlines() if line.strip()]
        return tests
    except Exception as e:
        st.error(f"Error reading {filename}: {e}")
        return []

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "diagnoses"
if 'diagnoses' not in st.session_state:
    st.session_state.diagnoses = [""] * 5
if 'laboratory_testing' not in st.session_state:
    st.session_state.laboratory_testing = [""] * 5
if 'radiological_tests' not in st.session_state:
    st.session_state.radiological_tests = [""] * 5
if 'other_tests' not in st.session_state:
    st.session_state.other_tests = [""] * 5

# Laboratory Testing Page
elif st.session_state.current_page == "laboratory_testing":
    st.markdown("### LABORATORY TESTING")
    st.write("For each laboratory test that you have chosen, please describe how they would influence your differential diagnosis.")

    lab_options = read_tests_from_file('labtests.txt')
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Laboratory Tests", unsafe_allow_html=True)

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis, unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + lab_options,
                key=f"lab_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_{diagnosis}_lab",
                    label_visibility="collapsed"
                )

    if st.button("Submit Laboratory Testing"):
        assessments = {}
        for i in range(5):
            for diagnosis in st.session_state.diagnoses:
                assessment = st.session_state[f"select_{i}_{diagnosis}_lab"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'laboratory_test': st.session_state.laboratory_testing[i],
                    'assessment': assessment
                })

        st.success("Laboratory testing assessments submitted successfully.")
        st.session_state.current_page = "radiological_tests"
        st.rerun()  # Rerun the app to refresh the page

# Radiological Tests Page
elif st.session_state.current_page == "radiological_tests":
    st.markdown("### RADIOLOGICAL TESTS")
    st.write("For each radiological test that you have chosen, please describe how they would influence your differential diagnosis.")

    rad_options = read_tests_from_file('radtests.txt')
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Radiological Tests", unsafe_allow_html=True)

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis, unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + rad_options,
                key=f"rad_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_{diagnosis}_rad",
                    label_visibility="collapsed"
                )

    if st.button("Submit Radiological Tests"):
        assessments = {}
        for i in range(5):
            for diagnosis in st.session_state.diagnoses:
                assessment = st.session_state[f"select_{i}_{diagnosis}_rad"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'radiological_test': st.session_state.radiological_tests[i],
                    'assessment': assessment
                })

        st.success("Radiological tests assessments submitted successfully.")
        st.session_state.current_page = "other_tests"
        st.rerun()  # Rerun the app to refresh the page

# Other Tests Page
elif st.session_state.current_page == "other_tests":
    st.markdown("### OTHER TESTS")
    st.write("For each other test that you have chosen, please describe how they would influence your differential diagnosis.")

    other_options = read_tests_from_file('othertests.txt')
    cols = st.columns(len(st.session_state.diagnoses) + 1)
    with cols[0]:
        st.markdown("Other Tests", unsafe_allow_html=True)

    for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
        with col:
            st.markdown(diagnosis, unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(len(st.session_state.diagnoses) + 1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + other_options,
                key=f"other_test_row_{i}",
                label_visibility="collapsed"
            )

        for diagnosis, col in zip(st.session_state.diagnoses, cols[1:]):
            with col:
                st.selectbox(
                    "",
                    options=["", "Necessary", "Neither More Nor Less Useful", "Unnecessary"],
                    key=f"select_{i}_{diagnosis}_other",
                    label_visibility="collapsed"
                )

    if st.button("Submit Other Tests"):
        assessments = {}
        for i in range(5):
            for diagnosis in st.session_state.diagnoses:
                assessment = st.session_state[f"select_{i}_{diagnosis}_other"]
                if diagnosis not in assessments:
                    assessments[diagnosis] = []
                assessments[diagnosis].append({
                    'other_test': st.session_state.other_tests[i],
                    'assessment': assessment
                })

        st.success("Other tests assessments submitted successfully.")
        # Set the session state to redirect to the Simple Success page
        st.session_state.current_page = "Simple Success"
        st.rerun()  # Rerun the app to refresh the page
