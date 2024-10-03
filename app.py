def main():
    # Initialize Firebase
    db = initialize_firebase()
    
    # Initialize session state
    if "user_code" not in st.session_state:
        st.session_state.user_code = None
        
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    
    if "document_id" not in st.session_state:
        st.session_state.document_id = str(uuid.uuid4())

    # Debugging: Print current user code and page
    st.write("User Code:", st.session_state.user_code)
    st.write("Current Page Before Routing:", st.session_state.page)

    # Load last page if user is logged in
    if st.session_state.user_code:
        last_page = load_last_page(db)
        if last_page:
            st.session_state.page = last_page

    # Debugging: Print current page after loading last page
    st.write("Current Page After Loading Last Page:", st.session_state.page)

    # Page routing
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        users = load_users()
        login_page(users, db, st.session_state.document_id)

        # Check if login was successful
        if st.session_state.user_code:
            st.session_state.page = load_last_page(db) or "welcome"
            st.experimental_rerun()  # Refresh to navigate to the last page
    elif st.session_state.page == "intake_form":
        display_intake_form(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "diagnoses":
        display_diagnoses(db, st.session_state.document_id, save_user_state)
    elif st.session_state.page == "Intervention Entry":
        intervention_entry_main(db, st.session_state.document_id)
    # Add other page conditions...
    else:
        st.write("Page not found. Redirecting to welcome.")
        st.session_state.page = "welcome"
        st.experimental_rerun()  # Redirect to welcome page

if __name__ == "__main__":
    main()

