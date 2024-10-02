def run_virtual_patient(db):
    st.title("Virtual Patient: Case #1")

    st.info(
        "You will have the opportunity to perform a history and ask for important physical examination details. "
        "You will be limited to 15 minutes. Alternatively, you may end the session."
    )

    # Initialize start_time only if it's not already set
    if 'start_time' not in st.session_state or st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    # Initialize session data for storing questions
    if 'session_data' not in st.session_state:
        st.session_state.session_data = {
            'questions_asked': []
        }

    # Calculate elapsed time
    elapsed_time = (time.time() - st.session_state.start_time) / 60

    # Display patient information
    if elapsed_time < 15:
        with st.form("question_form"):
            user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
            submit_button = st.form_submit_button("Submit")

            if submit_button and user_input:
                # Store the user question in the session data
                st.session_state.session_data['questions_asked'].append(user_input)

                # Get the virtual patient's response
                virtual_patient_response = get_chatgpt_response(user_input)
                st.write(f"Virtual Patient: {virtual_patient_response}")

                # Optionally display the questions asked so far
                st.write("Questions asked so far:")
                for question in st.session_state.session_data['questions_asked']:
                    st.write(f"- {question}")

        # Option to save questions and upload to Firebase
        if st.button("Save Questions"):
            if st.session_state.session_data['questions_asked']:
                # Collect session data
                session_data = collect_session_data()  # Collect session data
                
                # Append questions to the session data
                session_data['questions_asked'] = st.session_state.session_data['questions_asked']

                # Upload the session data to Firebase
                upload_message = upload_to_firebase(db, session_data)  # Upload to Firebase
                
                st.success("Your questions have been saved successfully.")
                
                # Optionally, you can change the page here
                st.session_state.page = "Focused Physical Examination"  # Change to the next page
                st.rerun()  # Rerun to navigate to the next page
            else:
                st.error("Please ask at least one question before saving.")

    else:
        st.warning("Session time is up. Please end the session.")
        if st.button("End Session"):
            st.session_state.start_time = None  # Reset start_time only when ending session
            st.session_state.page = "Focused Physical Examination"
            st.success("Session ended. You can start a new session.")

    # Option to move to a new screen
    if st.button("End Session"):
        st.session_state.start_time = None
        st.session_state.page = "Focused Physical Examination"
        st.rerun()
        st.write("Redirecting to a new screen...")

