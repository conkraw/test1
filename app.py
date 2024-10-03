def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    # Initialize session state
    if "user_code" not in st.session_state:
        st.session_state.user_code = None
        
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    
    # Generate a unique document ID at the start of the session
    if "document_id" not in st.session_state:
        st.session_state.document_id = str(uuid.uuid4())

    # Debugging: Print current user code and page
    st.write("User Code:", st.session_state.user_code)
    st.write("Current Page Before Loading Last Page:", st.session_state.page)

    # Only load the last page if the user is logged in
    if st.session_state.user_code:
        last_page = load_last_page(db)
        if last_page:
            st.session_state.page = last_page

    # Debugging: Print the page after loading last page
    st.write("Current Page After Loading Last Page:", st.session_state.page)

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        login_page(users, db, st.session_state.document_id)  # Pass document ID
        # Check if login was successful and set user_code
        if st.session_state.user_code:  # Assuming user_code is set upon successful login
            st.session_state.page = load_last_page(db)  # Load last page again to navigate correctly
    elif st.session_state.page == "intake_form":
        display_intake_form(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "diagnoses":
        display_diagnoses(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main(db, st.session_state.document_id)
    elif st.session_state.page == "History with AI":
        run_virtual_patient(db, st.session_state.document_id)
    elif st.session_state.page == "Focused Physical Examination":
        display_focused_physical_examination(db, st.session_state.document_id)
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        history_illness_script(db, st.session_state.document_id)
    elif st.session_state.page == "Physical Examination Features":
        display_physical_examination_features(db, st.session_state.document_id)
    elif st.session_state.page == "Laboratory Tests":
        display_laboratory_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Radiology Tests":
        display_radiological_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Other Tests":
        display_other_tests(db, st.session_state.document_id)
    elif st.session_state.page == "Results":
        display_results_image()
    elif st.session_state.page == "Laboratory Features":
        display_laboratory_features(db, st.session_state.document_id)
    elif st.session_state.page == "Treatments":
        display_treatments(db, st.session_state.document_id)
    elif st.session_state.page == "Simple Success":
        display_simple_success1()

