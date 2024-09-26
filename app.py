import streamlit as st
import pandas as pd

def main():
    st.title("Diagnosis Support Matrix")

    # Input for 5 diagnoses
    st.info("Please enter exactly 5 diagnoses:")
    diagnoses = [st.text_input(f"Diagnosis {i+1}", "") for i in range(5)]

    # Filter out any empty inputs
    diagnoses = [d for d in diagnoses if d.strip()]

    # Ensure exactly 5 diagnoses
    if len(diagnoses) != 5:
        st.warning("Please make sure to enter exactly 5 diagnoses.")
        return

    # Input for row headers (you can modify this as needed)
    row_count = st.number_input("Number of Row Headers", min_value=1, value=3, step=1)

    row_headers = [st.text_input(f"Row Header {i+1}", "") for i in range(row_count)]
    row_headers = [r for r in row_headers if r.strip()]

    # Create a DataFrame with dropdowns
    if row_headers:
        # Initialize the support matrix
        support_matrix = pd.DataFrame(index=row_headers, columns=diagnoses)

        # Fill the DataFrame with dropdowns
        for row in row_headers:
            for diagnosis in diagnoses:
                support_matrix.at[row, diagnosis] = st.selectbox(
                    f"{row} - {diagnosis}",
                    options=["Support", "Does not support"],
                    key=f"{row}_{diagnosis}"
                )

        # Display the resulting DataFrame
        st.subheader("Support Matrix")
        st.dataframe(support_matrix)

if __name__ == "__main__":
    main()
