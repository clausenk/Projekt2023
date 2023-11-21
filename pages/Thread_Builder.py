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
st.title('Tool zur erstellung von Threads')
st.write('Die Kategorien in der Legende können angeklickt werden, um die Indikatoren nach Kategorien zu filtern.')
keep_checkbox = st.checkbox('Nur Relevante Indikatoren', value=True, key='Keep')
#merge dataframe with other dataframe
df = pd.merge(df, df_withRandom_Values, on='Indikator', how='outer')
df_SzenarioDescription = pd.read_excel('./Szenario/Szenario.xlsx')

df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Name des Scenarios'])
df_SzenarioDescription = df_SzenarioDescription.dropna(subset=['Kurzbeschreibung des Thread /Scenarios'])

dfBuilder = pd.DataFrame(columns=['Indikator', 'Kurzindikator', 'Impact', 'Certainty', 'Zeit', 'STEEP-Kategorie', 'Kategorie', 'Szenario'])

if keep_checkbox == True:
    #drop all lines where the value of the column 'Keep' is 0
    df = df[df['Keep'] != 0]

fileName = st.text_input('Name des Threads', value='Name des Threads')
fileName = fileName + '.csv'


if 'dfBuilder' not in st.session_state:
    st.session_state.dfBuilder = pd.DataFrame(columns=['Indikator', 'Kurzindikator', 'Impact', 'Certainty', 'Zeit', 'STEEP-Kategorie', 'Kategorie', 'Szenario'])

df.loc[df['Impact_y'] <= 0, 'Impact_y'] = 0.1
indikator = st.selectbox('Kurzindikator',df['Kurzindikator'].unique())

#on button press take the value of the selectbox 'Indikator' and search for its corresponding row in the Df
if st.button('Add Indikator to DataFrame', key='addIndikator'):
    #get the row of the selected Indikator
    row = df.loc[df['Kurzindikator'] == indikator]
    #add the row to the DataFrame
    st.session_state.dfBuilder = st.session_state.dfBuilder.append(row, ignore_index=True)

st.write(st.session_state.dfBuilder)

csv = st.session_state.dfBuilder.to_csv(index=False)
st.download_button('Download CSV', csv, file_name=fileName)


#button to download the DataFrame as a csv file

#check if st.session_state.dfBuilder has any rows and if not display a message
if st.session_state.dfBuilder.empty:
    st.write('Noch keine Indikatoren ausgewählt. Bitte wählen Sie Indikatoren aus der Liste aus und fügen Sie sie dem DataFrame hinzu.')
    fig = px.scatter_3d(df, x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', opacity = 0.3, hover_data=['Indikator', 'Kurzindikator'], text='Kurzindikator')
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.session_state.dfBuilder = st.session_state.dfBuilder.sort_values(by='Zeit_y')

#check if all values in df ['Impact_y'] are greater than 0 and if not put them to 0.1

    fig = px.scatter_3d(df, x='Certainty_y', y='Zeit_y', z='Impact_y', color='STEEP-Kategorie_y', width = 1000, height = 1000, size='Impact_y', opacity = 0.3, hover_data=['Indikator', 'Kurzindikator'], text='Kurzindikator')
    lineChartBox = px.line_3d(st.session_state.dfBuilder, x='Certainty_y', y='Zeit_y', z='Impact_y', width=1000, height=1000, text='Kurzindikator', hover_data=['Kurzbeschreibung'])
    fig.update_layout(
    )
    fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))
    fig.add_trace(lineChartBox.data[0])
    st.plotly_chart(fig, use_container_width=True)

    #add button to clear the DataFrame
    if st.button('Clear DataFrame', key='clearDataFrame'):
        st.session_state.dfBuilder = pd.DataFrame(columns=['Indikator', 'Kurzindikator', 'Impact', 'Certainty', 'Zeit', 'STEEP-Kategorie', 'Kategorie', 'Szenario'])

    #add dropdown to select indicators to remove from the DataFrame
    indikatorToRemove = st.selectbox('Indikator to remove', st.session_state.dfBuilder['Kurzindikator'].unique())
    #add button to remove the selected indicator from the DataFrame
    if st.button('Remove Indikator from DataFrame', key='removeIndikator'):
        st.session_state.dfBuilder = st.session_state.dfBuilder[st.session_state.dfBuilder['Kurzindikator'] != indikatorToRemove]


    