import streamlit as st

with st.sidebar:
    NX = st.number_input("Number columns", 1, 10, 4, 1)
    NY = st.number_input("Number rows", 1, 10, 3, 1)

## Define list of parameters 
x_list = [*"abcdefghij"][:NX]
y_list = [*"xyzmnpqrst"][:NY]

## Write the first row of number inputs
cols = st.columns(len(x_list) + 1)
for x, col in zip(x_list, cols[1:]):
    with col:
        st.number_input(f"${x}$", 0.0, 1.0, 0.5, 0.1, key=x)



## For each new row, start with a number input and 
## write the the corresponding product
for y in y_list:
    cols = st.columns(len(x_list) + 1)
    with cols[0]:  # The first column is an input field
        st.number_input(f"${y}$", 0.0, 1.0, 0.5, 0.1, key=y)
    
for x, col in zip(x_list, cols[1:]):  # The rest of the columns are for results
        with col:
            xval = st.session_state[x]
            yval = st.session_state[y]
            st.metric(f"$({x},{y})$", f"({xval:.1f},{yval:.1f})")

