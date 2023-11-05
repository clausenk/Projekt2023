import altair as alt
import pandas as pd
import streamlit as st

# Example dataframe
data = pd.DataFrame({
    'x': range(5),
    'y': range(5)
})

# Chart with specified axis values
chart = alt.Chart(data).mark_point().encode(
    x=alt.X('x:Q', axis=alt.Axis(values=[0, 0.5,0.75, 1, 1.5, 2, 2.5, 3, 3.5, 4])),  # Specifies exact tick values
    y='y:Q'
)

st.altair_chart(chart, use_container_width=True)