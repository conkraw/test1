import streamlit as st

def main():
    st.title("Diagnosis Entry Form")

    st.info("Please enter exactly 5 diagnoses below:")

    # Create a list to hold the diagnoses
    diagnoses = []

    # Create 5 text input fields for diagnoses
    for i in range(1, 6):
        diagnosis = st.text_input(f"Diagnosis {i}", "")
        diagnoses.append(diagnosis)

    # Check if the user has filled all fields
    if st.button("Submit"):
        if all(diagnosis.strip() for diagnosis in diagnoses):
            st.success("Diagnoses submitted successfully!")
            st.write("Your diagnoses:")
            for i, diagnosis in enumerate(diagnoses, 1):
                st.write(f"{i}. {diagnosis}")
        else:
            st.error("Please fill out all 5 diagnosis fields.")

if __name__ == "__main__":
    main()

