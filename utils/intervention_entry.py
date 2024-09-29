import streamlit as st
import pandas as pd
from utils.history_with_ai import get_chatgpt_response


def main():
    st.title("Intervention Description Entry")

    # Prompt for user input
    st.header("Describe any interventions that you would currently perform.")
    interventions = st.text_area("Interventions Description", height=200)

    # Button to save to a local file (or any other desired action)
    if st.button("Save Intervention"):
        if interventions:
            # Save to a CSV file or handle as needed
            with open("interventions.csv", "a") as f:
                f.write(f"{interventions}\n")
            st.success("Your interventions have been saved.")
            get_chatgpt_response()
        else:
            st.error("Please enter a description of the interventions.")

if __name__ == '__main__':
    main()
