import streamlit as st
import openai
from docx import Document

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
        model="gpt-3.5-turbo",  # Adjust model as needed
        messages=[
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": croup_info}
        ]
    )
    return response['choices'][0]['message']['content']

# Streamlit app layout
st.title("Virtual Patient: Croup")

# Session state to track time and session status
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Check if the session is active
if st.session_state.start_time is None:
    st.session_state.start_time = st.time()

# Calculate elapsed time
elapsed_time = (st.time() - st.session_state.start_time) / 60  # Convert to minutes

# Display patient information
if elapsed_time < 15:
    st.subheader("Patient Information:")
    st.write(croup_info)

    user_input = st.text_input("Describe the patient's symptoms:")

    if st.button("Submit"):
        # Call the OpenAI API
        if user_input:
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



