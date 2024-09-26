import streamlit as st
import pandas as pd

# Set page layout to wide
st.set_page_config(layout="wide")

# Cache loading of users from CSV
@st.cache_data
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
    st.write("Welcome to the Pediatric Clerkship Assessment!")
    st.write("This assessment is designed to evaluate your clinical reasoning skills.")
    st.write("### Instructions:")
    st.write("1. Please enter your unique code on the next page.")
    st.write("2. Follow the prompts to complete the assessment.")
    
    if st.button("Next"):
        st.session_state.page = "login"  # Change to login page
        st.experimental_rerun()  # Rerun to refresh the view

# Login page function
def login_page(users):
    st.write("Please enter your unique code to access the assessment.")
    unique_code = st.text_input("Unique Code:")
    
    if st.button("Submit"):
        if unique_code:
            try:
                unique_code = int(unique_code.strip())
                if unique_code in users['code'].values:
                    st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                    st.session_state.page = "assessment"  # Change to assessment page
                    st.experimental_rerun()  # Rerun to refresh the view
                else:
                    st.error("Invalid code. Please try again.")
            except ValueError:
                st.error("Please enter a valid code.")
        else:
            st.error("Please enter a code.")

# Function to display the assessment page
def display_assessment():
    st.write(f"Welcome {st.session_state.user_name}! Here is the assessment.")

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

    # Patient Vital Signs Table
    st.markdown("""
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <td colspan="3" style="border: 1px solid #000; text-align: center; font-weight: bold; font-size: 20px;">
                PATIENT VITAL SIGNS
            </td>
        </tr>
        <tr>
            <td colspan="3" style="border: 1px solid #000; text-align: center;">
                Of the following vital signs that were obtained on patient intake, check the vital signs that are abnormal.
            </td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Vital Sign 1</td>
            <td style="border: 1px solid #000; text-align: center;">Vital Sign 2</td>
            <td style="border: 1px solid #000; text-align: center;">Vital Sign 3</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 1</td>
            <td style="border: 1px solid #000; text-align: center;">Value 2</td>
            <td style="border: 1px solid #000; text-align: center;">Value 3</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 4</td>
            <td style="border: 1px solid #000; text-align: center;">Value 5</td>
            <td style="border: 1px solid #000; text-align: center;">Value 6</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 7</td>
            <td style="border: 1px solid #000; text-align: center;">Value 8</td>
            <td style="border: 1px solid #000; text-align: center;">Value 9</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 10</td>
            <td style="border: 1px solid #000; text-align: center;">Value 11</td>
            <td style="border: 1px solid #000; text-align: center;">Value 12</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 13</td>
            <td style="border: 1px solid #000; text-align: center;">Value 14</td>
            <td style="border: 1px solid #000; text-align: center;">Value 15</td>
        </tr>
        <tr>
            <td style="border: 1px solid #000; text-align: center;">Value 16</td>
            <td style="border: 1px solid #000; text-align: center;">Value 17</td>
            <td style="border: 1px solid #000; text-align: center;">Value 18</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()


