import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
from streamlit_echarts import st_echarts


# Define the x and y axes
x_axis = alt.Axis(title='Impact', grid=True)
y_axis = alt.Axis(title=None, grid=True, labels=False)
y_axis_with_labels = alt.Axis(title='Certainty', grid=True)

# Load the Excel file
df = pd.read_excel('adjusted_indikatoren.xlsx')
st.set_page_config(layout='wide')



# Add a small offset to the Certainty values of the data points that have the same value
offset = 0.07
#df_offset = df.groupby('Certainty', sort=False).apply(lambda x: x.assign(Certainty=x['Certainty'] + offset * x.groupby('Certainty').cumcount()))
#df_offset['Prognose Group'] = pd.cut(df_offset['Prognose'], bins=[-float('inf'), 5, 10, float('inf')], labels=['Group 1', 'Group 2', 'Group 3'])
df['Prognose Group'] = pd.cut(df['Prognose'], bins=[-float('inf'), 5, 10, float('inf')], labels=['Group 1', 'Group 2', 'Group 3'])

col1, col2 = st.columns([4, 1])


subset_df = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df = subset_df.dropna(subset=['Certainty', 'Impact'])

subset_df_original = df[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df_original = subset_df_original.dropna(subset=['Certainty', 'Impact'])


certainty_values = [
    0,
    1,
    2,
    3,
    4,
    5,
]



option = {
    "tooltip": {"position": "top"},
    "title": [
        {"textBaseline": "middle", "top": f"{(1 / 3) * 100}%", "text": "0 - 5 Jahre", "left": "center", "textStyle": {"color": "#fff", "fontSize": 16}}
    ],
    "singleAxis": [
        {
            "left": 50,
            "type": "category",
            "boundaryGap": False,
            "data": certainty_values,
            "top": f"{(1 / 3) * 100}%",
            "height": f"{(1 / 3) * 100}%",
            "axisLabel": {"interval": 1},
        }
    ],
    "series": [
        {
            "singleAxisIndex": 0,
            "coordinateSystem": "singleAxis",
            "type": "scatter",
            "data": [
            ],
            "symbolSize": 20,
        }
    ]
}

for data in subset_df.itertuples():
    option['series'][0]['data'].append([data.Certainty, data.Indikator])
st_echarts(option, height=400) 

# Create the scatter plots with data points
point_groupOne = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 1']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(-4, 4)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=400,
    height=400,
)

point_groupTwo = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 2']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(-4, 4)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(domain=(0, 5)), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=400,
    height=400,
).interactive()

point_groupThree = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 3']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(-4, 4)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=400,
    height=400,
)

# Create the scatter plots with text labels
scatter_plot1 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 1']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(-4, 4)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=400,
    height=400,
    title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
)

scatter_plot2 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 2']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(-4, 4)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    text='Indikator:N'
).properties(
    width=400,
    height=400,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)

scatter_plot3 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 3']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(-4, 4)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    text='Indikator:N'
).properties(
    width=400,
    height=400,
    title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
)

# Link the zoom and movement of all three plots
title = alt.TitleParams(text='Timeframe', align='center', anchor='middle', fontSize=20)
scatter_plots = (scatter_plot1 + point_groupOne | scatter_plot2 + point_groupTwo | scatter_plot3 + point_groupThree).resolve_scale(
    x='shared',
    y='shared'
)
scatter_plots_with_title = alt.vconcat(scatter_plots, title=title)

#Display the elements on the page in 2 columns
with col1:
    st.markdown('## Früher-Prototyp zur Darstellung der Indikatoren und Mapping ohne Interaktion und erweiterte Funktionen')
    st.altair_chart(scatter_plots_with_title, use_container_width=False)
with col2:
    st.markdown('#### Auswahl der STEEP-Kategorie')
    category = st.radio("Select a STEEP-Kategorie", ['Technological', 'Economical', 'Social', 'Political', 'Environmental'])
    image = Image.open('description.png')
    st.image(image)
st.table(subset_df)