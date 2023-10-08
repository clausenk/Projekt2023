import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
import altair as alt

# Define the x and y axes
x_axis = alt.Axis(title='Impact', grid=True)
y_axis = alt.Axis(title=None, grid=True, labels=False)
y_axis_with_labels = alt.Axis(title='Certainty', grid=True)

# Load the Excel file
df = pd.read_excel('indikatoren.xlsx')
st.set_page_config(layout='wide')





# Add a small offset to the Certainty values of the data points that have the same value
offset = 0.07
df_offset = df.groupby('Certainty', sort=False).apply(lambda x: x.assign(Certainty=x['Certainty'] + offset * x.groupby('Certainty').cumcount()))
df_offset['Prognose Group'] = pd.cut(df_offset['Prognose'], bins=[-float('inf'), 5, 10, float('inf')], labels=['Group 1', 'Group 2', 'Group 3'])


col1, col2 = st.columns([1800, 300])


subset_df = df_offset[['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group']]
subset_df = subset_df.dropna(subset=['Certainty', 'Impact'])


# Define the color bands
green_band = alt.Chart(pd.DataFrame({'x': [0, 3]})).mark_rect(color='green', opacity=0.2).encode(
    x='x:Q'
)

yellow_band = alt.Chart(pd.DataFrame({'x': [3, 6]})).mark_rect(color='yellow', opacity=0.2).encode(
    x='x:Q'
)

red_band = alt.Chart(pd.DataFrame({'x': [6, 9]})).mark_rect(color='red', opacity=0.2).encode(
    x='x:Q'
)

point_groupOne = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 1']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(zero=False), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=500,
    height=600,
)

point_groupTwo = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 2']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(zero=False), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=500,
    height=600,
).interactive()

point_groupThree = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 3']).mark_circle(size=60).encode(
    x=alt.X('Impact', scale=alt.Scale(zero=False), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator']
).properties(
    width=500,
    height=600,
)

# Create the scatter plot with padding
scatter_plot1 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 1']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=500,
    height=600,
    title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
)


scatter_plot2 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 2']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', scale=alt.Scale(zero=False), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    text='Indikator:N'
).properties(
    width=500,
    height=600,
    title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
)

scatter_plot3 = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 3']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', scale=alt.Scale(zero=False), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    text='Indikator:N'
).properties(
    width=500,
    height=600,
    title=alt.TitleParams(text='10 - 15 Jahre', align='center', anchor='middle', fontSize=16)
)

# Link the zoom and movement of all three plots

title = alt.TitleParams(text='Timeframe', align='center', anchor='middle', fontSize=20)


scatter_plots = (scatter_plot1 + point_groupOne | scatter_plot2 + point_groupTwo | scatter_plot3 + point_groupThree).resolve_scale(
    x='shared',
    y='shared'
)
scatter_plots = alt.vconcat(scatter_plots, title=title)

#with col2:
    #category = st.radio("Select a STEEP-Kategorie", ['Technological', 'Economical', 'Social', 'Political'])
selection = alt.selection_single(fields=['STEEP-Kategorie'], name='Select')
with col1:
    st.altair_chart(scatter_plots, use_container_width=False)

st.table(subset_df)


# Display the table
#st.altair_chart(scatter_plots, use_container_width=True)
#st.table(subset_df)
