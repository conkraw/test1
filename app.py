import streamlit as st
import os

# Load physical examination text from a file
def load_phys_exam_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please check the file path.")
        return ""

# Function to display selected examination component text
def display_selected_component(selected_component):
    if selected_component:
        text = load_phys_exam_data("phys_exam.txt")
        
        if text:
            # Extract and display the relevant section
            component_texts = text.split('\n\n')  # Assuming sections are separated by double newlines
            for component_text in component_texts:
                if selected_component.lower() in component_text.lower():
                    st.markdown(f"### {selected_component}\n")
                    st.markdown(component_text)
                    break
        else:
            st.write("No text available for the selected component.")

# Function to check and display an image if present
def display_image(base_image_name):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff','.PNG','.JPG','.JPEG','.GIF','.BMP','.TIFF']
    image_found = False

    for ext in image_extensions:
        image_path = f"{base_image_name}{ext}"
        if os.path.isfile(image_path):
            st.image(image_path, caption="Image interpretation required.", use_column_width=True)
            image_found = True
            break  # Exit loop if an image is found

    if not image_found:
        st.write("No image file named 'image_1' found.")

# Main Streamlit app
def main():
    st.title("Physical Examination Components")

    st.markdown("""
    Please select and review the physical examination components to help develop your differential diagnosis.
    Please note that any image provided requires interpretation.
    """)

    # List of examination components
    components = [
        "General Appearances", "Eyes", "Ears, Neck, Nose, Throat", "Lymph Nodes",
        "Cardiovascular", "Lungs", "Abdomen", "Skin", "Extremities",
        "Musculoskeletal", "Neurological", "Psychiatry", "Genitourinary", "Image"
    ]

    # User selection
    selected_component = st.selectbox("Select a physical examination component:", components)

    if st.button("Review"):
        display_selected_component(selected_component)

        # Check for image file if "Image" is selected
        if selected_component == "Image":
            display_image("image_1")  # No extension needed here

if __name__ == '__main__':
    main()

