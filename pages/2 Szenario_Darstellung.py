import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import numpy as np

# Load the Excel files
df_Szenario = pd.read_excel('indikatoren.xlsx')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')
df_TrendTime = pd.read_excel('./indikatoren_timeRandomized.xlsx')

column_to_copy = 'Zeit_x'

df_SzenarioWithTime = pd.merge(df_Szenario, df_TrendTime, on='Indikator')

#Page configuration
st.set_page_config(layout='wide')
st.title('Darstellung Threads')

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

df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Name des Scenarios'])

#check if all the Szenarios have a corresponding Data in the other Excel file
for index, row in df_SzenarioDescription.iterrows():
    #check in the other Excel file if the Szenario is in there based on the Name of the Creator
    if row['Name'] not in df_SzenarioWithTime.columns:
        #if the Szenario is not in the other Excel file, delete the row from the DataFrame
        df_SzenarioDescription.drop(index, inplace=True)
    else:
        #check if the Column of the Creator is empty or only contains 1 value
        if df_SzenarioWithTime[row['Name']].isnull().all() or df_SzenarioWithTime[row['Name']].nunique() == 1:
            #if the Column of the Creator is empty or only contains 1 value, delete the row from the DataFrame
            df_SzenarioDescription.drop(index, inplace=True)


# Add a Dropdown to select the Szenario
szenario = st.selectbox('Thread (Beta)', df_SzenarioDescription['Name des Scenarios'].unique())
#get the description of the selected Szenario and show it
szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
st.write(szenarioDescription)
#get the Name of the Creator of the selected Szenario and show it
szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]

#use the name of the Creator to get the corresponding Data from the other Excel file
seleceted_column = df_SzenarioWithTime[szenarioCreator]

#use the selected_column to get all lines from all columns where the value of the selected_column is not NaN
seleceted_column = df_SzenarioWithTime[df_SzenarioWithTime[szenarioCreator].notna()]

point_groupOne_treiber = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Treiber')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080
).interactive()
point_groupOne_trend = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Trend')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_signal = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Signal')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_schwachessignal = alt.Chart(df_SzenarioWithTime.loc[(df_SzenarioWithTime['Kategorie_x'] == 'Schwaches Signal')]).mark_point(size=symbol_size, opacity=0.2).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()

backgroundData = point_groupOne_treiber + point_groupOne_trend + point_groupOne_signal + point_groupOne_schwachessignal

szenario_treiber = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Treiber')]).mark_point(size=200).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
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
    fontSize=14,
    fontWeight=500,
).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
    text='Kurzindikator',
    tooltip=['Indikator', szenarioCreator],
    color=alt.value(treiber_color),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_trend = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Trend')]).mark_point(size=150).encode(
    x=alt.X('Zeit_x', scale=alt.Scale(domain=(0, 18))),
    y=alt.Y('Certainty_y', scale=alt.Scale(domain=(0, 6))),
    size=alt.Size('Impact_y', scale=alt.Scale(range=[0, 100])),
    tooltip=['Indikator', 'Kategorie_x', 'STEEP-Kategorie_x', 'Certainty_x', 'Impact_x', 'Zeit_x'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
szenario_trend_text = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Trend')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=14,
    fontWeight=500,
).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
    text='Kurzindikator',
    tooltip=['Indikator', szenarioCreator],
    color=alt.value(trend_color),
).properties(
    width=1920,
    height=1080,
).interactive()
szenario_signal_text = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Signal')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=14,
    fontWeight=500,
).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
    text='Kurzindikator',
    tooltip=['Indikator', szenarioCreator],
    color=alt.value(signal_color),
).properties(
    width=1920,
    height=1080,
).interactive()
szenario_signal_text = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Schwaches Signal')]).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=14,
    fontWeight=500,
).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
    text='Kurzindikator',
    tooltip=['Indikator', szenarioCreator],
    color=alt.value(schwachessignal_color),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_line = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Treiber')]).mark_line(color= treiber_color, opacity=0.3).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_line_trend = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Trend')]).mark_line(color= trend_color, opacity=0.3).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_line_signal = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Trend')]).mark_line(color= signal_color, opacity=0.3).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_line_schwachessignal = alt.Chart(seleceted_column.loc[(seleceted_column['Kategorie_x'] == 'Trend')]).mark_line(color= schwachessignal_color, opacity=0.3).encode(
    x=alt.X('Zeit_x'),
    y=alt.Y('Certainty_y'),
).properties(
    width=1920,
    height=1080,
).interactive()

szenario_chart = backgroundData + szenario_treiber + szenario_treiber_text + szenario_trend + szenario_trend_text + szenario_line + szenario_line_trend

st.altair_chart(szenario_chart, use_container_width=False)

#show the data of the selected Szenario
st.write(seleceted_column)