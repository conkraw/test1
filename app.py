import streamlit as st
import pandas as pd
from pdf2image import convert_from_path

st.set_page_config(layout="wide")

# Load users from CSV
@st.cache_data
def load_users():
    return pd.read_csv('users.csv')

# Function to convert PDF pages to images
def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = f"page_{i + 1}.png"
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

# Main app function
def main():
    st.title("Pediatric Clerkship Virtual Clinical Reasoning Assessment")

    # Load user data
    users = load_users()

    # Check if the user is logged in
    if "user_name" in st.session_state:
        # Display welcome message if user is logged in
        st.write(f"Welcome, {st.session_state.user_name}!")
        st.button("Start Assessment", on_click=lambda: display_pdf("ptinfo.pdf"))
    else:
        st.write("Welcome! Please enter your unique code to access the assessment.")

        # Prompt user for unique code
        unique_code = st.text_input("Unique Code:")

        if st.button("Next"):
            if unique_code:
                try:
                    unique_code = int(unique_code.strip())  # Convert input to integer
                    if unique_code in users['code'].values:
                        st.session_state.user_name = users.loc[users['code'] == unique_code, 'name'].values[0]
                        # Rerun to display the welcome page
                        st.rerun()
                    else:
                        st.error("Invalid code. Please try again.")
                except ValueError:
                    st.error("Please enter a valid code.")
            else:
                st.error("Please enter a code.")

def display_pdf(pdf_path):
    st.subheader("Instructions")
    images = pdf_to_images(pdf_path)
    for image_path in images:
        st.image(image_path, use_column_width=True)

if __name__ == "__main__":
    main()

