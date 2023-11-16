import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import numpy as np
import plotly.express as px

df = pd.read_excel('indikatoren.xlsx')
df_withRandom_Values = pd.read_excel('indikatoren_timeRandomized.xlsx')

st.set_page_config(layout='wide')
st.title('Darstellung der Indikatoren in den jeweiligen Szenarien')
keep_checkbox = st.checkbox('Nur Relevante Indikatoren', value=True, key='Keep')
#merge dataframe with other dataframe
df = pd.merge(df, df_withRandom_Values, on='Indikator', how='outer')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')

df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Name des Scenarios'])
df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Kurzbeschreibung des Thread /Scenarios'])

if keep_checkbox == True:
    #drop all lines where the value of the column 'Keep' is 0
    df = df[df['Keep'] != 0]

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


#count the number of Szenarios
number_of_Szenarios = len(df_SzenarioDescription['Name des Scenarios'].unique())

#create a 2 column layout based on the number of Szenarios
col1, col2 = st.columns(2)

#iterate over the number of Szenarios and display the Szenario 1 in the first column, Szenario 2 in the second column, Szenario 3 in the first column, Szenario 4 in the second column, etc.
for i in range(number_of_Szenarios):
    if i % 2 == 0:
        with col1:
            szenario = df_SzenarioDescription['Name des Scenarios'].unique()[i]
            szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
            szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]
            seleceted_column = df[szenarioCreator]
            seleceted_column = df[df[szenarioCreator].notna()]
            df.loc[df['Impact_y'] <= 0, 'Impact_y'] = 0.1
            fig = px.sunburst(
                seleceted_column, 
                path=['Kategorie_x', 'STEEP-Kategorie_x', 'Kurzindikator'],  # Define the hierarchy including Kurzindikator
                values='Impact_x',                        # The size of each segment                       # Color of each segment, based on Impact value
                title=df_SzenarioDescription['Name des Scenarios'].unique()[i],
                height=600,
                width=600,
                hover_data=['Indikator', 'Kurzbeschreibung']
            )
            st.plotly_chart(fig, use_container_width=False)
    else:
        with col2:
            szenario = df_SzenarioDescription['Name des Scenarios'].unique()[i]
            szenarioDescription = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Kurzbeschreibung des Thread /Scenarios'].iloc[0]
            szenarioCreator = df_SzenarioDescription.loc[df_SzenarioDescription['Name des Scenarios'] == szenario, 'Name'].iloc[0]
            seleceted_column = df[szenarioCreator]
            seleceted_column = df[df[szenarioCreator].notna()]
            df.loc[df['Impact_y'] <= 0, 'Impact_y'] = 0.1
            fig = px.sunburst(
                seleceted_column, 
                path=['Kategorie_x', 'STEEP-Kategorie_x', 'Kurzindikator'],  # Define the hierarchy including Kurzindikator
                values='Impact_x',                        # The size of each segment                       # Color of each segment, based on Impact value
                title=df_SzenarioDescription['Name des Scenarios'].unique()[i],
                height=600,
                width=600,
                hover_data=['Indikator', 'Kurzbeschreibung']
            )
            st.plotly_chart(fig, use_container_width=False)



