import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad
import plotly.express as px
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


#Page configuration
st.set_page_config(layout='wide')
st.title('Treiber Würfel')
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

#Change Prognose Group 1, 2, 3 on X Axis to 0 - 5, 5 - 10, 10 - 15
subset_df['Prognose Group'] = subset_df['Prognose Group'].replace({'Group 1': '0 - 5', 'Group 2': '5 - 10', 'Group 3': '10 - 15'})

#drop all rows that do not have the value "Treiber" in the "Kategorie" column
treiber_rows = subset_df['Kategorie'] == 'Treiber'
subset_df = subset_df.drop(index=set(subset_df.index) - set(treiber_rows.index))


#check if all values in the column Impact are not smaller than 0 and if they are set them to 0
subset_df.loc[subset_df['Impact'] < 0, 'Impact'] = 0

def neues_intervallfive(x):
    if x == '0 - 5':
        return 5
    if x == '5 - 10':
        return 10
    


subset_df['Zeit'] = subset_df['Prognose Group'].apply(neues_intervallfive)

def random_intervallfive(x):
    if x == 5:
        return np.random.uniform(2, 7)
    else:
        return x

subset_df['Zeit'] = subset_df['Zeit'].apply(random_intervallfive)

def random_intervallten(x):
    if x == 10:
        return np.random.uniform(7, 12)
    else:
        return x

subset_df['Zeit'] = subset_df['Zeit'].apply(random_intervallten)

def neues_intervallfifteen(x):
    if pd.isna(x):
        return np.random.uniform(12, 17)
    else:
        return x
    
subset_df['Zeit'] = subset_df['Zeit'].apply(neues_intervallfifteen)


fig = px.scatter_3d(subset_df.loc[(subset_df['Kategorie'] == 'Treiber')], x='Zeit', y='Certainty', z='Impact', color='STEEP-Kategorie', size='Impact', width=800, height=800, hover_name='Indikator', text='Indikator')
fig.for_each_trace(lambda t: t.update(textfont_color=t.marker.color, textposition='top center'))


st.plotly_chart(fig, use_container_width=False)