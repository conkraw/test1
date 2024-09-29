def run_virtual_patient_app():
    # Load OpenAI API key from Streamlit secrets
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Function to read the croup document
    def read_croup_doc():
        doc = Document("croup.docx")
        content = []
        for para in doc.paragraphs:
            content.append(para.text)
        return "\n".join(content).lower()  # Convert to lower case for easier matching

    # Load the document content
    croup_info = read_croup_doc()

    # Function to get response from ChatGPT
    def get_chatgpt_response(user_input):
        user_input_lower = user_input.lower()  # Normalize the user input to lower case

        if user_input_lower in croup_info:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": "Role play a parent whose child is experiencing croup. Answer medical inquiries based on the croup document."}
                ]
            )
            return response['choices'][0]['message']['content']
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": "If you cannot answer the medical inquiry from the croup document, please respond naturally as a concerned parent."}
                ]
            )
            return response['choices'][0]['message']['content']

    # Streamlit app layout
    st.title("Virtual Patient: Case #1")

    st.info(
        "You will have the opportunity to perform a history and ask for important physical examination details using a virtual patient/parent. "
        "When you are ready, please start asking questions. You will be limited to 15 minutes. "
        "Alternatively, you may end the session if you click end."
    )

    # Session state to track time
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    elapsed_time = (time.time() - st.session_state.start_time) / 60  # Convert to minutes

    if elapsed_time < 15:
        with st.form("question_form"):
            user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
            submit_button = st.form_submit_button("Submit")

            if submit_button and user_input:
                virtual_patient_response = get_chatgpt_response(user_input)
                st.write(f"Virtual Patient: {virtual_patient_response}")

    else:
        st.warning("Session time is up. Please end the session.")

    # End session button with unique key
    if st.button("End Session", key="end_session_button"):
        st.session_state.start_time = None
        st.session_state.page = "physical_examination"  # Navigate to physical examination selection
        st.success("Session ended. You can start a new session.")
        st.rerun()  # Re-run to apply session state changes


