# utils/orders.py

import streamlit as st

def display_laboratory_testing():
    st.markdown("### LABORATORY TESTING")
    st.write("For each laboratory test that you have chosen, please describe how they would influence your differential diagnosis.")

    lab_options = read_tests_from_file('labtests.txt')  # Ensure this function is defined elsewhere
    cols = st.columns(1)
    with cols[0]:
        st.markdown("Laboratory Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + lab_options,
                key=f"lab_test_row_{i}",
                label_visibility="collapsed"
            )

    if st.button("Submit Laboratory Testing"):
        st.success("Laboratory testing assessments submitted successfully.")
        st.session_state.current_page = "radiological_tests"
        st.experimental_rerun()  # Rerun the app to refresh the page


def display_radiological_tests():
    st.markdown("### RADIOLOGICAL TESTS")
    st.write("For each radiological test that you have chosen, please describe how they would influence your differential diagnosis.")

    rad_options = read_tests_from_file('radtests.txt')  # Ensure this function is defined elsewhere
    cols = st.columns(1)
    with cols[0]:
        st.markdown("Radiological Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + rad_options,
                key=f"rad_test_row_{i}",
                label_visibility="collapsed"
            )

    if st.button("Submit Radiological Tests"):
        st.success("Radiological tests assessments submitted successfully.")
        st.session_state.current_page = "other_tests"
        st.experimental_rerun()  # Rerun the app to refresh the page


def display_other_tests():
    st.markdown("### OTHER TESTS")
    st.write("For each other test that you have chosen, please describe how they would influence your differential diagnosis.")

    other_options = read_tests_from_file('othertests.txt')  # Ensure this function is defined elsewhere
    cols = st.columns(1)
    with cols[0]:
        st.markdown("Other Tests", unsafe_allow_html=True)

    for i in range(5):
        cols = st.columns(1)
        with cols[0]:
            st.selectbox(
                "",
                options=[""] + other_options,
                key=f"other_test_row_{i}",
                label_visibility="collapsed"
            )

    if st.button("Submit Other Tests"):
        st.success("Other tests assessments submitted successfully.")
        st.session_state.current_page = "Simple Success"
        st.experimental_rerun()  # Rerun the app to refresh the page
