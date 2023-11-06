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
df = pd.read_excel('indikatoren.xlsx')
timeScale = (0, 18)

#Page configuration
st.set_page_config(layout='wide')
st.title('Prognose der Indikatoren')

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

col1, col2, col3, col4, col5 = st.columns([0.1 , 0.1, 0.1, 0.1, 0.1])

st.write(pd.__version__)

# Add checkboxes to select the Steep Categories
with col1:
    social_checkbox = st.checkbox('Soziales', value=True, key='Social')
with col2:
    tech_checkbox = st.checkbox('Technologie', value=True, key='Technological')
with col3:
    environment_checkbox = st.checkbox('Ökologie', value=True, key='Environmental')
with col4:
    economical_checkbox = st.checkbox('Ökonomie', value=True, key='Economical')
with col5:
    politics_checkbox = st.checkbox('Politik', value=True, key='Political')

# Add Checkboxes to select the indicators
with col1:
    treiber_checkbox = st.checkbox('Treiber', value=True, key='Treiber')
with col2:
    trend_checkbox = st.checkbox('Trend', value=True, key='Trend')
with col3:
    signal_checkbox = st.checkbox('Signal', value=True, key='Signal')
with col4:
    schwaches_signal_checkbox = st.checkbox('Schwaches Signal', value=True, key='Schwaches Signal')

# Add a checkbox to select time frame
with col1:
    group_one_checkbox = st.checkbox(' 2 - 7 Jahre', value=True, key='Group 1')
with col2:
    group_two_checkbox = st.checkbox(' 8 - 12 Jahre', value=True, key='Group 2')
with col3:
    group_three_checkbox = st.checkbox(' 13 - 17 Jahre', value=True, key='Group 3')


df_TrendlisteZeit = pd.read_excel('indikatoren_timeRandomized.xlsx')
df_trendliste = pd.read_excel('indikatoren.xlsx')

# Add Trendliste to TrendlisteZeit thorugh the Indikator column

df_SzenarioMerged = pd.merge(df_TrendlisteZeit, df_trendliste, on='Indikator')


# Create empty dataframe to fill with the selected indicators
df_selected_indicators = pd.DataFrame()
df_selected_steep = pd.DataFrame()
df_selected_time = pd.DataFrame()

# Add the selected indicators to the dataframe based on the checkboxes
if treiber_checkbox == True:
    df_selected_indicators = df_selected_indicators.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Treiber')])
if trend_checkbox == True:
    df_selected_indicators = df_selected_indicators.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Trend')])
if signal_checkbox == True:
    df_selected_indicators = df_selected_indicators.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Signal')])
if schwaches_signal_checkbox == True:
    df_selected_indicators = df_selected_indicators.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Schwaches Signal')])

if social_checkbox == True:
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Social')])
if tech_checkbox == True:
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Technological')])
if environment_checkbox == True:
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Environmental')])
if economical_checkbox == True:
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Economical')])
if politics_checkbox == True:
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Politics')])

if group_one_checkbox == True:
    df_selected_time = df_selected_time.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Prognose Group'] == '0 - 5')])
    if group_two_checkbox == False & group_three_checkbox == False:
        timeScale = (1, 8)
if group_two_checkbox == True:
    df_selected_time = df_selected_time.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Prognose Group'] == '5 - 10')])
    if group_three_checkbox == False & group_one_checkbox == False:
        timeScale = (7, 13)
if group_three_checkbox == True:
    df_selected_time = df_selected_time.append(df_SzenarioMerged.loc[(df_SzenarioMerged['Prognose Group'] == '10 - 15')])
    if group_two_checkbox == False & group_one_checkbox == False:
        timeScale = (12, 18)


#Check all lines in df_selected_time ('Indikator') and compare them to the lines in df_selected_steep ('Indikator') and save them in new dataframe
df_selected_indicators_SteepTime = df_selected_time[df_selected_time['Indikator'].isin(df_selected_steep['Indikator'])]
df_selected_indicators_SteepTimeKategorie = df_selected_indicators_SteepTime[df_selected_indicators_SteepTime['Kategorie_x'].isin(df_selected_indicators['Kategorie_x'])]

#Create Background Chart
chart_treiber_background = alt.Chart((df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Treiber')])).mark_point(size=symbol_size, opacity=0.1).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color),
).properties(
    width=1920,
    height=1080,
).interactive()

chart_trend_background = alt.Chart((df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Trend')])).mark_point(size=symbol_size, opacity=0.1).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color),
).properties(
    width=1920,
    height=1080,
).interactive()

chart_signal_background = alt.Chart((df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Signal')])).mark_point(size=symbol_size, opacity=0.1).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color),
).properties(
    width=1920,
    height=1080,
).interactive()

chart_schwachessignal_background = alt.Chart((df_SzenarioMerged.loc[(df_SzenarioMerged['Kategorie_x'] == 'Schwaches Signal')])).mark_point(size=symbol_size, opacity=0.1).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color),
).properties(
    width=1920,
    height=1080,
).interactive()

background = chart_treiber_background + chart_trend_background + chart_signal_background + chart_schwachessignal_background

chart_treiber = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_treiber_text = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Treiber')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    text='Indikator',
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_trend = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_trend_text = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Trend')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    text='Indikator',
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_signal = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_signal_text = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Signal')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    text='Indikator',
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_schwachessignal = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y'),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

chart_schwachessignal_text = alt.Chart(df_selected_indicators_SteepTimeKategorie.loc[(df_selected_indicators_SteepTimeKategorie['Kategorie_x'] == 'Schwaches Signal')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
).encode(
    x=alt.X('Zeit', scale=alt.Scale(domain=timeScale), axis=alt.Axis(tickMinStep=0.1)),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    text='Indikator',
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

mainMap = chart_trend + chart_trend_text + chart_signal + chart_signal_text + chart_schwachessignal + chart_schwachessignal_text + chart_treiber + chart_treiber_text
chart = mainMap + background

tab1, tab2 = st.tabs(['Chart', 'Data'])

with tab1:
    st.altair_chart(chart, use_container_width=False)
with tab2:
    st.write(df_selected_indicators_SteepTimeKategorie)

