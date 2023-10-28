import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import numpy as np

# Load the Excel files
df_Szenario = pd.read_excel('./Szenario/Trendliste.xlsx')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')
df_TrendTime = pd.read_excel('./indikatoren_timeRandomized.xlsx')

column_to_copy = 'Zeit'

df_SzenarioWithTime = pd.merge(df_Szenario, df_TrendTime, on='Indikator')

#Page configuration
st.set_page_config(layout='wide')
st.title('Darstellung der Beta-Szenarien (Threads)')

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


# Add a Dropdown to select the Szenario
szenario = st.selectbox('Thread (Beta)', df_SzenarioDescription['Name des Scenarios'].unique())
#get the description of the selected Szenario and show it
szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
st.write(szenarioDescription)
#get the Name of the Creator of the selected Szenario and show it
szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]
st.write(szenarioCreator)

#use the name of the Creator to get the corresponding Data from the other Excel file
seleceted_column = df_SzenarioWithTime[szenarioCreator]
#use the selected_column to get all lines from all columns where the value of the selected_column is not NaN
seleceted_column = df_SzenarioWithTime[df_SzenarioWithTime[szenarioCreator].notna()]

point_groupOne_treiber = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Treiber')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080
).interactive()
point_groupOne_trend = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Trend')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_signal = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Signal')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_schwachessignal = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Schwaches Signal')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

backgroundData = point_groupOne_treiber + point_groupOne_trend + point_groupOne_signal + point_groupOne_schwachessignal

szenario_treiber = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Treiber')]).mark_point(size=200).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080,
).interactive()
szenario_treiber_text = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Treiber')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
).encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty_y'),
    text='Indikator',
    color=alt.value(treiber_color),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_line = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Treiber')]).mark_line(color= 'red', opacity=0.3).encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty_y'),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_chart = backgroundData + szenario_treiber + szenario_treiber_text + szenario_line

st.altair_chart(szenario_chart, use_container_width=False)

#show the data of the selected Szenario
st.write(seleceted_column)