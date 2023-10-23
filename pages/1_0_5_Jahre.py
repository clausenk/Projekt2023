import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad

# Define Session States
if 'text_marks_visible' not in st.session_state:
    st.session_state.text_marks_visible = True
if 'steep_category' not in st.session_state:
    st.session_state.steep_category = 'Alle'

# Define Multipage App



# Define the x and y axes
x_axis = alt.Axis(title='Impact', grid=True)
y_axis = alt.Axis(title=None, grid=True, labels=False)
y_axis_with_labels = alt.Axis(title='Certainty', grid=True)

# Load the Excel file
df = pd.read_excel('indikatoren.xlsx')


#Page configuration
st.set_page_config(layout='wide')
col1, col2 = st.columns([4, 1])

st.sidebar.title('Navigation')

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
df['Prognose Group'] = pd.cut(df['Prognose'], bins=[-float('inf'), 5, 10, float('inf')], labels=['Group 1', 'Group 2', 'Group 3'])
subset_df = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df = subset_df.dropna(subset=['Certainty', 'Impact'])
subset_df_original = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df_original = subset_df_original.dropna(subset=['Certainty', 'Impact'])



point_groupOne_megatrends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 6)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(domain=(0, 6)), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(megatrend_symbol),
    color=alt.value(megatrend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_trends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080,
).interactive()

scatterplots_darstellung = point_groupOne_megatrends + point_groupOne_trends + point_groupOne_signal + point_groupOne_schwachessignal + point_groupOne_treiber


scatter_plot1_text_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Signal') ]).mark_text(size=15, opacity=1.0, color=signal_color, dy=-15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_trend = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Trend') ]).mark_text(size=15, opacity=1.0, color=trend_color, dy=-15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Treiber') ]).mark_text(size=15, opacity=1.0, color=treiber_color, dy=-15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Schwaches Signal') ]).mark_text(size=15, opacity=1.0, color=schwachessignal_color, dy=-15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)

scatter_plot1_text = scatter_plot1_text_signal + scatter_plot1_text_trend + scatter_plot1_text_treiber + scatter_plot1_text_schwachessignal


scatterplot = scatter_plot1_text + scatterplots_darstellung
st.altair_chart(scatterplot, use_container_width=False)