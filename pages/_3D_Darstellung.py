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
keep_checkbox = st.checkbox('Nur Relevante Indikatoren', value=True, key='Keep')
keepSzenario_checkbox = st.checkbox('Nur Relevante Szenarien', value=True, key='KeepSzenario')
#merge dataframe with other dataframe
df = pd.merge(df, df_withRandom_Values, on='Indikator', how='outer')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')

df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Name des Scenarios'])
df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Kurzbeschreibung des Thread /Scenarios'])

if keepSzenario_checkbox == True:
    #drop all lines where the value of the column 'Presentable' is 0
    df_SzenarioDescription = df_SzenarioDescription[df_SzenarioDescription['Presentable'] != 0]

if keep_checkbox == True:
    #drop all lines where the value of the column 'Keep' is 0
    df = df[df['Keep'] != 0]


#check if all the Szenarios have a corresponding Data in the other Excel file
for index, row in df_SzenarioDescription.iterrows():
    #check in the other Excel file if the Szenario is in there based on the Name of the Creator
    if row['Name'] not in df.columns:
        #if the Szenario is not in the other Excel file, delete the row from the DataFrame
        df_SzenarioDescription.drop(index, inplace=True)

szenario = st.selectbox('Szenario',df_SzenarioDescription['Name des Scenarios'].unique())

#get the description of the selected Szenario and show it
szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
st.write(szenarioDescription)
szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]
st.write(szenarioCreator)

seleceted_column = df[szenarioCreator]
seleceted_column = df[df[szenarioCreator].notna()]


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Szenarien', 'Treiber', 'Trends', 'Signale', 'Alle'])


#check if all values in df ['Impact_y'] are greater than 0 and if not put them to 0.1
df.loc[df['Impact_y'] <= 0, 'Impact_y'] = 0.1

seleceted_column = seleceted_column.sort_values(by='Zeit_y')


with tab1:
    fig = px.scatter_3d(df, x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', opacity = 0.3, hover_data=['Indikator', 'Kurzindikator'])
    fig.update_layout(
    )
    lineChartBox = px.line_3d(seleceted_column, x='Certainty_y', y='Zeit_y', z='Impact_y', width=1000, height=1000, text='Kurzindikator', hover_data=['Kurzbeschreibung'])
    lineChartBox.update_layout(
        font=dict(
            family="Calibri",
            size=34
        )
    )
    lineChartBox.update_traces(marker=dict(size=0))
    fig.add_trace(lineChartBox.data[0])
    st.plotly_chart(fig, use_container_width=True)

    #only show the columns 'kurzindikator'

    #change the column name of the column with the selected_column name to Indikatorbeschreibung
    st.write(seleceted_column)

    #get all the values in the column certainty_x and calculate the mean of them
    meanCertainty = seleceted_column['Certainty_x'].mean()
    meanImpact = seleceted_column['Impact_x'].mean()

    #round the mean to 1 decimal place
    meanCertainty = round(meanCertainty, 1)
    meanImpact = round(meanImpact, 1)

    st.write('Durchschnittliche Sicherheit: ' + str(meanCertainty))
    st.write('Durchschnittlicher Impact: ' + str(meanImpact))

    #count the occurences of the values in the column 'STEEP-Kategorie_x' and show them in a bar chart
    steepKategorie = seleceted_column['STEEP-Kategorie_x'].value_counts()
    steepKategorie = steepKategorie.to_frame()
    steepKategorie = steepKategorie.rename(columns={'STEEP-Kategorie_x': 'Anzahl'})
    steepKategorie = steepKategorie.reset_index()
    steepKategorie = steepKategorie.rename(columns={'index': 'STEEP-Kategorie'})
    steepKategorie = steepKategorie.sort_values(by='STEEP-Kategorie')
    steepKategorie = steepKategorie.reset_index(drop=True)
    st.write(steepKategorie)
    steepKategorieChart = alt.Chart(steepKategorie).mark_bar().encode(
        x='STEEP-Kategorie',
        y='Anzahl'
    )


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

with tab5:
    fig = px.scatter_3d(df, x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)
