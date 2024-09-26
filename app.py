import streamlit as st
import openai
from docx import Document
import time

# Function to read the croup document
def read_croup_doc():
    doc = Document("croup.docx")
    content = []
    for para in doc.paragraphs:
        content.append(para.text)
    return "\n".join(content)

# Load the document content
croup_info = read_croup_doc()

# Set up OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get response from ChatGPT
def get_chatgpt_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": "Pretend to be a virtual patient with croup."}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit app layout
st.title("Virtual Patient: Case #1")

# Instructions for the user
st.info(
    "You will have the opportunity to perform a history and ask for important physical examination details using a virtual patient/parent. "
    "When you are ready, please start asking questions. You will be limited to 15 minutes. "
    "Alternatively, you may end the session if you click end."
)

# Session state to track time and session status
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# Calculate elapsed time
elapsed_time = (time.time() - st.session_state.start_time) / 60  # Convert to minutes

# Display patient information
if elapsed_time < 15:
    with st.form("question_form"):
        user_input = st.text_input("Ask the virtual patient a question about their symptoms:")
        submit_button = st.form_submit_button("Submit")

        if submit_button and user_input:
            virtual_patient_response = get_chatgpt_response(user_input)
            st.write(f"Virtual Patient: {virtual_patient_response}")

else:
    st.warning("Session time is up. Please end the session.")
    if st.button("End Session"):
        st.session_state.start_time = None
        st.success("Session ended. You can start a new session.")

# Option to move to a new screen
if st.button("Go to New Screen"):
    st.session_state.start_time = None
    st.write("Redirecting to a new screen...")



