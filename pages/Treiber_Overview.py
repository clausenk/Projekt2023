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


#Page configuration
st.set_page_config(layout='wide')
st.title('Prognose der Indikatoren')
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


"""
#Change Prognose Group 1, 2, 3 on X Axis to 0 - 5, 5 - 10, 10 - 15
subset_df['Prognose Group'] = subset_df['Prognose Group'].replace({'Group 1': '0 - 5', 'Group 2': '5 - 10', 'Group 3': '10 - 15'})

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

"""

slidervalue = st.slider('slider', min_value=2, max_value=17, step=1, value=2)



bubble_plot = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Treiber')])).mark_square().encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty'),
    size = alt.Size('Impact'),
    color = alt.Color('STEEP-Kategorie'),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    text = 'Indikator:Q'
).properties(
    width=1920,
    height=1080,
).interactive()

# Add the text marks
bubble_plot_text = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Treiber')])).mark_text(
    align='left',
    baseline='middle',
    dx=14,
    fontSize=10,
    fontWeight=500,
    opacity=0.3
).encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty'),
    text='Indikator',
    color= alt.Color('STEEP-Kategorie')
).properties(
    width=1920,
    height=1080,
).interactive()

bubble_plot_trend = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Trend') & ((subset_df['Zeit'] >= slidervalue - 1) & (subset_df['Zeit'] <= slidervalue + 1))])).mark_circle().encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty'),
    size = alt.Size('Impact'),
    #color = alt.Color('STEEP-Kategorie'),
    color = alt.value('white'),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    text = 'Indikator:Q'
).properties(
    width=1920,
    height=1080,
).interactive()

bubble_plot_trend_text = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Trend') & ((subset_df['Zeit'] >= slidervalue - 1) & (subset_df['Zeit'] <= slidervalue + 1))])).mark_text().encode(
    x=alt.X('Zeit'),
    y=alt.Y('Certainty'),
    #set the color to white
    color = alt.value('white'),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    text = 'Indikator'
).properties(
    width=1920,
    height=1080,
).interactive()

line_plot = alt.Chart((subset_df.loc[(subset_df['Kategorie'] == 'Trend') & ((subset_df['Zeit'] >= slidervalue - 1) & (subset_df['Zeit'] <= slidervalue + 1))])).mark_line(color= 'red').encode(
    x=alt.X('Zeit'),
    y=alt.value(0),
    strokeWidth=alt.value(10),
    color=alt.value('red')
)

bubble_plot = bubble_plot + bubble_plot_text + bubble_plot_trend + bubble_plot_trend_text + line_plot

#Add Button that lets me download the current chart as a xls file
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

csv = convert_df(subset_df)

st.download_button(
   "Press to Download",
   csv,
   "file.csv",
   "text/csv",
   key='download-csv'
)


st.altair_chart(bubble_plot, use_container_width=False)