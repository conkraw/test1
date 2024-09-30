import streamlit as st

def display_simple_success():
    print("Displaying Simple Success page.")  # Debugging statement
    st.title("Success!")
    st.write("Your operation was successful1111.")
    
    if st.button("Proceed to Next Page"):
        print("Proceed button clicked.")  # Debugging statement
        st.session_state.page = "next_page"  # Change this to the actual next page you want to navigate to
        st.rerun()  # Rerun the app to reflect the page change
