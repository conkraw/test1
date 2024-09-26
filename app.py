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
            # Create a dictionary from the text file
            component_dict = {}
            for line in text.split('\n'):
                if ':' in line:  # Only consider lines with a colon
                    key, value = line.split(':', 1)
                    component_dict[key.strip()] = value.strip()

            # Display the selected component's text
            if selected_component in component_dict:
                st.markdown(f"### {selected_component}\n")
                st.markdown(component_dict[selected_component])
            else:
                st.write("No text available for the selected component.")
        else:
            st.write("No text available for the selected component.")

# Function to check and display an image if present
def display_image(base_image_name):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', 
                        '.PNG', '.JPG', '.JPEG', '.GIF', '.BMP', '.TIFF']
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

    # Automatically display the selected component without an additional button
    display_selected_component(selected_component)

    # Check for image file
    if selected_component == "Image":
        display_image("image_1")  # Change the base name if needed

if __name__ == '__main__':
    main()

