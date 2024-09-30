import streamlit as st

def display_simple_success():
    st.title("Simple Success Module")

    # Simulated success message
    if st.button("Submit Historical Features"):
        st.success("Success! Historical features submitted.")
        
        # Button to go to the next page
        if st.button("Go to Next Page"):
            st.session_state.current_page = "next_page"  # Change this to your actual next page
            st.experimental_rerun()  # Rerun the app to reflect the change

if __name__ == "__main__":
    display_simple_success()
