import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import numpy as np
import plotly.express as px

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
st.set_page_config(layout='centered')
st.title('Darstellung der Indikatoren in 3D')
st.write('Die Kategorien in der Legende können angeklickt werden, um die Indikatoren nach Kategorien zu filtern.')

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

social_checkbox = True
tech_checkbox = True
environment_checkbox = True
economical_checkbox = True
politics_checkbox = True

treiber_checkbox = True
trend_checkbox = True
signal_checkbox = True
schwaches_signal_checkbox = True

group_one_checkbox = True
group_two_checkbox = True
group_three_checkbox = True



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
    df_selected_steep = df_selected_steep.append(df_SzenarioMerged.loc[(df_SzenarioMerged['STEEP-Kategorie_x'] == 'Political')])

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


tab1, tab2 = st.tabs(['Treiber', 'Trends'])

with tab1:
    fig = px.scatter_3d(df_selected_indicators.loc[(df_selected_indicators['Kategorie_x'] == 'Treiber')], x='Zeit', y='Certainty_y', z='Impact_y', color='STEEP-Kategorie_x', size='Impact_x', width=1000, height=1000, hover_name='Indikator', text='Indikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=False)

with tab2:
    fig = px.scatter_3d(df_selected_indicators.loc[(df_selected_indicators['Kategorie_x'] == 'Trend')], x='Zeit', y='Certainty_y', z='Impact_y', color='STEEP-Kategorie_x', size='Impact_x', width=1000, height=1000, hover_name='Indikator', text='Indikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=False)
