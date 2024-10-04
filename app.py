def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    # Initialize session state
    if "user_code" not in st.session_state:  # Initialize user_code if not present
        st.session_state.user_code = None 
        
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    
    # Set document_id to user_code if the user is logged in (after user_code is set)
    if st.session_state.user_code:
        st.session_state.document_id = st.session_state.user_code  # Set document_id to user_code
    
    # Load last page if user is logged in
    if st.session_state.user_code:
        last_page = load_last_page(db)
        if last_page:
            st.session_state.page = last_page

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        login_page(users, db)  # No need to pass document_id here, as it's now handled in the login
    elif st.session_state.page == "intake_form":
        if st.session_state.document_id:  # Ensure document_id is initialized
            display_intake_form(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "diagnoses":
        if st.session_state.document_id:
            display_diagnoses(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Intervention Entry":
        if st.session_state.document_id:
            intervention_entry_main(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "History with AI":
        if st.session_state.document_id:
            run_virtual_patient(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Focused Physical Examination":
        if st.session_state.document_id:
            display_focused_physical_examination(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Physical Examination Components":
        display_physical_examination()
    elif st.session_state.page == "History Illness Script":
        if st.session_state.document_id:
            history_illness_script(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Physical Examination Features":
        if st.session_state.document_id:
            display_physical_examination_features(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Laboratory Tests":
        if st.session_state.document_id:
            display_laboratory_tests(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Radiology Tests":
        if st.session_state.document_id:
            display_radiological_tests(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Other Tests":
        if st.session_state.document_id:
            display_other_tests(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Results":
        display_results_image()
    elif st.session_state.page == "Laboratory Features":
        if st.session_state.document_id:
            display_laboratory_features(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Treatments":
        if st.session_state.document_id:
            display_treatments(db, st.session_state.document_id)  # Pass document_id here
        else:
            st.error("User code is not set. Please log in.")
    elif st.session_state.page == "Simple Success":
        display_simple_success1()

if __name__ == "__main__":
    main()

