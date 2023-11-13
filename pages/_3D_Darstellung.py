import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import numpy as np
import plotly.express as px

df = pd.read_excel('indikatoren.xlsx')
df_withRandom_Values = pd.read_excel('indikatoren_timeRandomized.xlsx')

st.set_page_config(layout='wide')
st.title('Darstellung der Indikatoren in 3D')
st.write('Die Kategorien in der Legende können angeklickt werden, um die Indikatoren nach Kategorien zu filtern.')

#merge dataframe with other dataframe
df = pd.merge(df, df_withRandom_Values, on='Indikator', how='outer')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')

df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Name des Scenarios'])
df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Kurzbeschreibung des Thread /Scenarios'])

#check if all the Szenarios have a corresponding Data in the other Excel file
for index, row in df_SzenarioDescription.iterrows():
    #check in the other Excel file if the Szenario is in there based on the Name of the Creator
    if row['Name'] not in df.columns:
        #if the Szenario is not in the other Excel file, delete the row from the DataFrame
        df_SzenarioDescription.drop(index, inplace=True)
    else:
        #check if the Column of the Creator is empty or only contains 1 value
        if df[row['Name']].isnull().all() or df[row['Name']].nunique() == 1:
            #if the Column of the Creator is empty or only contains 1 value, delete the row from the DataFrame
            df_SzenarioDescription.drop(index, inplace=True)


szenario = st.selectbox('Thread (Beta)',df_SzenarioDescription['Name des Scenarios'].unique())

#get the description of the selected Szenario and show it
szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
st.write(szenarioDescription)
szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]
st.write(szenarioCreator)

seleceted_column = df[szenarioCreator]
seleceted_column = df[df[szenarioCreator].notna()]


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Szenarien', 'Treiber', 'Trends', 'Signale', 'Schwache Signale'])


#check if all values in df ['Impact_y'] are greater than 0 and if not put them to 0.1
df.loc[df['Impact_y'] <= 0, 'Impact_y'] = 0.1

with tab1:
    fig = px.scatter_3d(df, x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', opacity = 0.3)
    fig.update_layout(
    )
    lineChartBox = px.line_3d(seleceted_column, x='Certainty_y', y='Zeit_y', z='Impact_y', width=1000, height=1000, text='Kurzindikator', hover_data=['Kurzbeschreibung'])
    lineChartBox.update_layout(
        font=dict(
            family="Calibri",
            size=34
        )
    )
    fig.add_trace(lineChartBox.data[0])
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.scatter_3d(df.loc[(df['Kategorie_x'] == 'Treiber')], x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    fig = px.scatter_3d(df.loc[(df['Kategorie_x'] == 'Trend')], x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    fig = px.scatter_3d(df.loc[(df['Kategorie_x'] == 'Signal')], x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    fig = px.scatter_3d(df.loc[(df['Kategorie_x'] == 'Schwaches Signal')], x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)