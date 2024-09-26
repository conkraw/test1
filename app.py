import streamlit as st
import pandas as pd

## Initialize parameter inputs
x_list = {"Parameter": [*"abcd"]}
x_list["Values"] = [0.5] * len(x_list["Parameter"])

y_list = {"Parameter": [*"xyz"]}
y_list["Values"] = [0.5] * len(y_list["Parameter"])

## Display input space
cols = st.columns(2)
with cols[0]:
    "## Rows"
    x_data = st.data_editor(x_list, use_container_width=True, num_rows='dynamic')

with cols[1]:
    "## Columns"
    y_data = st.data_editor(y_list, use_container_width=True, num_rows='dynamic')

## Combine
x_times_y = [ [f"({x}, {y})" for x in x_data["Values"]] for y in y_data["Values"] ]

## Display result
df = pd.DataFrame(x_times_y, columns=x_data["Parameter"])
df.index = y_data["Parameter"]

"## Product"
st.dataframe(df, use_container_width=True)
