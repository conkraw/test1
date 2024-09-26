import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide")

# Cache loading of users from CSV
@st.cache_data(persist=True)
def load_users():
    return pd.read_csv('users.csv')

# Function to read text from a TXT file
def read_text_file(txt_file_path):
    try:
        with open(txt_file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File not found: {txt_file_path}. Please check the file path.")
        return ""
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Function to load vital signs from a TXT file
def load_vital_signs(vital_signs_file):
    vital_signs = {}
    try:
        with open(vital_signs_file, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    key = parts[0].strip()  # Get type (e.g., heart_rate)
                    value = parts[1].strip()  # Get vital sign description
                    vital_signs[key] = value
    except FileNotFoundError:
        st.error(f"File not found: {vital_signs_file}. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    return vital_signs

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Initialize session state for page if not already done
    if "page" not in st.session_state:
        st.session_state.page = "welcome"  # Start on the welcome page

    # Check which page to display
    if st.session_state.page == "assessment":
        display_assessment()
    elif st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "login":
        login_page(users)

# Welcome page function
def welcome_page():
    st.markdown("<h3 style='font-family: \"DejaVu Sans\";'>Welcome to the Pediatric Clerkship Assessment!</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>This assessment is designed to evaluate your clinical reasoning skills.</p>", unsafe_allow_html=True)
    st.markdown("<h4 style='font-family: \"DejaVu Sans\";'>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>1. Please enter your unique code on the next page.<br>2. Follow the prompts to complete the assessment.</p>", unsafe_allow_html=True)
    
    if st.button("Next"):
        st.session_state.page = "login"  # Change to login page
        st.rerun()  # Rerun to refresh the view

# Login page function
def login_page(users):
    st.markdown("<p style='font-family: \"DejaVu Sans\";'>Please enter your unique code to access the assessment.</p>", unsafe_allow_html=True)
    unique_code = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.page = "assessment"  # Change to assessment page
                    st.rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

def display_assessment():
    st.markdown(f"<h3 style='font-family: \"DejaVu Sans\";'>Welcome {st.session_state.user_name}! Here is the intake form.</h3>", unsafe_allow_html=True)

    # Read and display the text from ptinfo.txt
    txt_file_path = "ptinfo.txt"
    document_text = read_text_file(txt_file_path)
    
    if document_text:
        title_html = """
        <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px; color: #2c3e50;">
            Patient Information:
        </h2>
        """
        st.markdown(title_html, unsafe_allow_html=True)

        custom_html = f"""
        <div style="font-family: 'DejaVu Sans'; font-size: 18px; line-height: 1.5; color: #34495e; background-color: #ecf0f1; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            {document_text.replace('\n', '<br>')}
        </div>
        """
        st.markdown(custom_html, unsafe_allow_html=True)
    else:
        st.write("No text found in the document.")

    # Load vital signs
    vital_signs_file = "vital_signs.txt"
    vital_signs = load_vital_signs(vital_signs_file)

    # Vital Signs Title
    title_html = """
    <h2 style="font-family: 'DejaVu Sans'; font-size: 24px; margin-bottom: 10px; color: #2c3e50;">
        Vital Signs:
    </h2>
    """
    st.markdown(title_html, unsafe_allow_html=True)

    # Display the table with Streamlit checkboxes
    st.markdown("<h4 style='font-family: \"DejaVu Sans\";'>Vital Signs:</h4>", unsafe_allow_html=True)
    
    for key in ['heart_rate', 'respiratory_rate', 'blood_pressure', 'pulseox', 'temperature', 'weight']:
        value = vital_signs.get(key, 'N/A')
        st.checkbox(f"{key.replace('_', ' ').capitalize()} Abnormal")
        st.write(f"Value: {value}")

# Run the main function
if __name__ == "__main__":
    main()
