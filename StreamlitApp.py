import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import altDarstellungen as ad

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

point_plot_all = ad.plotAllCertaintyImpact(subset_df_original, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height)
point_plot_all_over_time = ad.plotAllOverTimeImpact(subset_df_original, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height)
point_plot_all_over_time_certainty = ad.plotAllOverTimeCertainty(subset_df_original, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height)
point_plot_all_combined = alt.hconcat(point_plot_all, point_plot_all_over_time, point_plot_all_over_time_certainty)
st.altair_chart(point_plot_all_combined)

point_plot_STEEP = ad.plotAllSteepOverTime(subset_df_original, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height)
st.altair_chart(point_plot_STEEP)

df['impact_bin'] = (df['Impact'] // 1)
df['certainty_bin'] = (df['Certainty'] // 1)
heatmap_data = df.groupby(['impact_bin', 'certainty_bin']).size().reset_index(name='count')
heatmap_data.head()
heatmap = alt.Chart(heatmap_data).mark_rect().encode(
    x=alt.X('impact_bin:O', title='Impact'),
    y=alt.Y('certainty_bin:O', title='Certainty', sort='descending'),
    color=alt.Color('count:Q', scale=alt.Scale(scheme='viridis'), title='Indikatoren'),
    tooltip=['impact_bin', 'certainty_bin', 'count']
).properties(
    width=400,
    height=400,
    title="Heatmap basierend auf Impact und Certainty"
)

# Filter the data based on the selected STEEP-Kategorie
if st.session_state.steep_category != 'Alle':
    subset_df = subset_df.loc[subset_df['STEEP-Kategorie'] == st.session_state.steep_category]
    subset_df_original = subset_df_original.loc[subset_df_original['STEEP-Kategorie'] == st.session_state.steep_category]

point_groupOne_megatrends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 7)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(domain=(0, 7)), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(megatrend_symbol),
    color=alt.value(megatrend_color)
).properties(
    width=chart_width,
    height=chart_height,
).interactive()
point_groupOne_trends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupOne_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupOne_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupOne_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=chart_width,
    height=chart_height,
)
scatterplots_zeitraumOne = point_groupOne_megatrends + point_groupOne_trends + point_groupOne_signal + point_groupOne_schwachessignal + point_groupOne_treiber

point_groupTwo_megatrends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value('square'),
    color=alt.value(megatrend_color)
).properties(
    width=chart_width,
    height=chart_height,
).interactive()
point_groupTwo_trends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupTwo_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupTwo_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupTwo_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=chart_width,
    height=chart_height,
)
scatterplots_zeitraumTwo = point_groupTwo_megatrends + point_groupTwo_trends + point_groupTwo_signal + point_groupTwo_schwachessignal + point_groupTwo_treiber

point_groupThree_megatrends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(megatrend_symbol),
    color=alt.value(megatrend_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupThree_trends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis), 
    y=alt.Y('Certainty', axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupThree_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis), 
    y=alt.Y('Certainty', axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupThree_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis), 
    y=alt.Y('Certainty', axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=chart_width,
    height=chart_height,
)
point_groupThree_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', axis=y_axis),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=chart_width,
    height=chart_height,
)
scatterplots_zeitraumThree = point_groupThree_megatrends + point_groupThree_trends + point_groupThree_signal + point_groupThree_schwachessignal + point_groupThree_treiber

# Create the scatter plots with text labels or without text labels based on the toggle button
if st.session_state.text_marks_visible == True:
    scatter_plot1_text_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Signal') ]).mark_text(size=15, opacity=1.0, color=signal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot1_text_trend = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Trend') ]).mark_text(size=15, opacity=1.0, color=trend_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot1_text_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Treiber') ]).mark_text(size=15, opacity=1.0, color=treiber_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot1_text_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 1') & (subset_df['Kategorie'] == 'Schwaches Signal') ]).mark_text(size=15, opacity=1.0, color=schwachessignal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
    )

    scatter_plot1_text = scatter_plot1_text_signal + scatter_plot1_text_trend + scatter_plot1_text_treiber + scatter_plot1_text_schwachessignal

    scatter_plot2_text_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Signal') ]).mark_text(size=15, opacity=1.0, color=signal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot2_text_trend = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Trend') ]).mark_text(size=15, opacity=1.0, color=trend_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot2_text_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Treiber') ]).mark_text(size=15, opacity=1.0, color=treiber_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot2_text_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 2') & (subset_df['Kategorie'] == 'Schwaches Signal') ]).mark_text(size=15, opacity=1.0, color=schwachessignal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
    )

    scatter_plot2_text = scatter_plot2_text_signal + scatter_plot2_text_trend + scatter_plot2_text_treiber + scatter_plot2_text_schwachessignal

    scatter_plot3_text_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Signal') ]).mark_text(size=15, opacity=1.0, color=signal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=y_axis),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot3_text_trend = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Trend') ]).mark_text(size=15, opacity=1.0, color=trend_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=y_axis),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot3_text_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Treiber') ]).mark_text(size=15, opacity=1.0, color=treiber_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=y_axis),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot3_text_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Schwaches Signal') ]).mark_text(size=15, opacity=1.0, color=schwachessignal_color, dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=y_axis),
        text='Indikator:N'
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
    )

    scatter_plot3_text = scatter_plot3_text_signal + scatter_plot3_text_trend + scatter_plot3_text_treiber + scatter_plot3_text_schwachessignal
else:
    scatter_plot1_text = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 1']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
        x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
        y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='0 - 5 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot2_text = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 2']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    ).properties(
        width=400,
        height=400,
        title=alt.TitleParams(text='5 - 10 Jahre', align='center', anchor='middle', fontSize=16)
    )
    scatter_plot3_text = alt.Chart(subset_df.loc[subset_df['Prognose Group'] == 'Group 3']).mark_text(size=15, opacity=1.0, color='white', dy=15).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis),
    ).properties(
    width=400,
    height=400,
    title=alt.TitleParams(text='10 - 15+ Jahre', align='center', anchor='middle', fontSize=16)
    )


#display the heatmap and the scatter plots in 3 columns
st.altair_chart(heatmap, use_container_width=False)

# Link the zoom and movement of all three plots
title = alt.TitleParams(text='Timeframe', align='center', anchor='middle', fontSize=20)
scatter_plots = (scatter_plot1_text + scatterplots_zeitraumOne | scatter_plot2_text + scatterplots_zeitraumTwo | scatter_plot3_text + scatterplots_zeitraumThree).resolve_scale(
    x='shared',
    y='shared'
)
scatter_plots_with_title = alt.vconcat(scatter_plots, title=title)

#Display the elements on the page in 2 columns
with col1:
    st.altair_chart(scatter_plots_with_title, use_container_width=False)
    toggle_button = st.button('Toggle Text Marks')
with col2:
    st.markdown('#### Auswahl der STEEP-Kategorie')
    steep_category = st.radio("Select a STEEP-Kategorie", ['Alle', 'Technological', 'Economical', 'Social', 'Political', 'Environmental'])
    #image = Image.open('description.png')
    #st.image(image)
st.table(subset_df)

point_groupOne_megatrends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 7)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(domain=(0, 7)), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(megatrend_symbol),
    color=alt.value(megatrend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_trends = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(trend_symbol),
    color=alt.value(trend_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(signal_symbol),
    color=alt.value(signal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(schwachessignal_symbol),
    color=alt.value(schwachessignal_color)
).properties(
    width=1920,
    height=1080,
).interactive()
point_groupOne_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
    x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
    y=alt.Y('Certainty', scale=alt.Scale(zero=False), axis=y_axis_with_labels),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose Group'],
    shape=alt.value(treiber_symbol),
    color=alt.value(treiber_color)
).properties(
    width=1920,
    height=1080,
).interactive()

scatterplots_darstellung = point_groupOne_megatrends + point_groupOne_trends + point_groupOne_signal + point_groupOne_schwachessignal + point_groupOne_treiber


scatter_plot1_text_signal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Signal') ]).mark_text(size=15, opacity=1.0, color=signal_color, dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='10 - 15 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_trend = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Trend') ]).mark_text(size=15, opacity=1.0, color=trend_color, dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='10 - 15 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_treiber = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Treiber') ]).mark_text(size=15, opacity=1.0, color=treiber_color, dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='10 - 15 Jahre', align='center', anchor='middle', fontSize=16)
)
scatter_plot1_text_schwachessignal = alt.Chart(subset_df.loc[(subset_df['Prognose Group'] == 'Group 3') & (subset_df['Kategorie'] == 'Schwaches Signal') ]).mark_text(size=15, opacity=1.0, color=schwachessignal_color, dy=15).encode(
    x=alt.X('Impact', title='Impact', scale=alt.Scale(domain=(0, 5)), axis=alt.Axis(format='~')),
    y=alt.Y('Certainty', title='Certainty', scale=alt.Scale(zero=False), axis=alt.Axis(format='~')),
    text='Indikator:N'
).properties(
    width=1920,
    height=1080,
    title=alt.TitleParams(text='10 - 15 Jahre', align='center', anchor='middle', fontSize=16)
)

scatter_plot1_text = scatter_plot1_text_signal + scatter_plot1_text_trend + scatter_plot1_text_treiber + scatter_plot1_text_schwachessignal


scatterplot = scatter_plot1_text + scatterplots_darstellung



st.altair_chart(scatterplot, use_container_width=False)




#Functionality of the toggle button and the radio button
if toggle_button:
    st.session_state.text_marks_visible = not st.session_state.text_marks_visible
    st.experimental_rerun()
if steep_category != st.session_state.steep_category:
    st.session_state.steep_category = steep_category
    st.experimental_rerun()