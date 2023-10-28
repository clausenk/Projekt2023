import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import numpy as np

# Define Session States
if 'text_marks_visible' not in st.session_state:
    st.session_state.text_marks_visible = True
if 'steep_category' not in st.session_state:
    st.session_state.steep_category = 'Alle'

# Define the x and y axes
x_axis = alt.Axis(title='Impact', grid=True)
y_axis = alt.Axis(title=None, grid=True, labels=False)
y_axis_with_labels = alt.Axis(title='Certainty', grid=True)

# Load the Excel file
df = pd.read_excel('indikatoren_timeRandomized.xlsx')


#Page configuration
st.set_page_config(layout='wide')


# Chart configuration
chart_width = 400
chart_height = 400
megatrend_symbol = 'square'
trend_symbol = 'circle'
signal_symbol = 'triangle'
schwachessignal_symbol = 'diamond'
treiber_symbol = 'cross'
megatrend_color = '#1f77b4'
trend_color = '#ff7f0e'
signal_color = '#2ca02c'
schwachessignal_color = '#d62728'
treiber_color = '#9467bd'
symbol_size = 90
text_marks_visible = True
steep_category = 'Alle'


# Add a small offset to the Certainty values of the data points that have the same value
offset = 0.07
#df['Prognose Group'] = pd.cut(df['Prognose'], bins=[-float('inf'), 5, 10, float('inf')], labels=['Group 1', 'Group 2', 'Group 3'])
subset_df = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group', 'Zeit']]
subset_df = subset_df.dropna(subset=['Certainty', 'Impact'])
subset_df_original = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df_original = subset_df_original.dropna(subset=['Certainty', 'Impact'])


bubble_plot = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Trend') & (subset_df['STEEP-Kategorie'] == 'Political')])).mark_circle().encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty'),
    size = alt.Size('Impact'),
    color = alt.Color('STEEP-Kategorie'),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    text = 'Indikator:Q'
).properties(
    width=2300,
    height=1080,
).interactive()

# Add the text marks
bubble_plot_text = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Trend') & (subset_df['STEEP-Kategorie'] == 'Political')])).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=18,
    fontWeight=500,
).encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty'),
    text='Indikator',
    color= alt.Color('STEEP-Kategorie')
).properties(
    width=2300,
    height=1080,
).interactive()

bubble_plot = bubble_plot + bubble_plot_text

st.altair_chart(bubble_plot, use_container_width=False)