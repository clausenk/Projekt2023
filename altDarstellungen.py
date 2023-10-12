import streamlit as st
import altair as alt


def plotAllCertaintyImpact(dataframe, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height):
    scatterPlot_megatrend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(
            zero=False), axis=y_axis_with_labels),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose Group'],
        shape=alt.value('square'),
        color=alt.value('#1f77b4')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_treiber = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(
            zero=False), axis=y_axis_with_labels),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose Group'],
        shape=alt.value('cross'),
        color=alt.value('#9467bd')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_trend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(
            zero=False), axis=y_axis_with_labels),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose Group'],
        shape=alt.value('circle'),
        color=alt.value('#ff7f0e')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_signal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(
            zero=False), axis=y_axis_with_labels),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose Group'],
        shape=alt.value('triangle'),
        color=alt.value('#2ca02c')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_schwachesSignal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Impact', scale=alt.Scale(domain=(0, 5)), axis=x_axis),
        y=alt.Y('Certainty', scale=alt.Scale(
            zero=False), axis=y_axis_with_labels),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose Group'],
        shape=alt.value('diamond'),
        color=alt.value('#d62728')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot = scatterPlot_megatrend + scatterPlot_treiber + \
        scatterPlot_trend + scatterPlot_signal + scatterPlot_schwachesSignal

    return scatterPlot

    # take the dataframe and change the all values in the column Prognose Group based on the following rules: Prognose Group 1 to "0-5", Prognose Group 2 to "5-10" and Prognose Group 3 to "10-15+"
    dataframe['Prognose Group'] = dataframe['Prognose Group'].cat.add_categories([
                                                                                 '0-5', '5-10', '10-15+'])
    dataframe['Prognose Group'] = dataframe['Prognose Group'].replace(
        {1: "0-5", 2: "5-10", 3: "10-15+"})

    # rename the Prognose Group column to Prognose
    dataframe = dataframe.rename(columns={'Prognose Group': 'Prognose'})

    scatterPlot_megatrend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
        y=alt.X('Prognose', scale=alt.Scale(zero=False)),
        x=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('square'),
        color=alt.value('#1f77b4')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_treiber = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
        y=alt.Y('Impact', scale=alt.Scale()),
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('cross'),
        color=alt.value('#9467bd')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_trend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
        y=alt.Y('Impact', scale=alt.Scale()),
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('circle'),
        color=alt.value('#ff7f0e')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_signal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
        y=alt.Y('Impact', scale=alt.Scale()),
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('triangle'),
        color=alt.value('#2ca02c')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_schwachesSignal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
        y=alt.Y('Impact', scale=alt.Scale()),
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('diamond'),
        color=alt.value('#d62728')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot = scatterPlot_megatrend + scatterPlot_treiber + \
        scatterPlot_trend + scatterPlot_signal + scatterPlot_schwachesSignal

    return scatterPlot


def plotAllOverTimeImpact(dataframe, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height):

    # take the dataframe and change the all values in the column Prognose Group based on the following rules: Prognose Group 1 to "0-5", Prognose Group 2 to "5-10" and Prognose Group 3 to "10-15+"
    dataframe['Prognose Group'] = dataframe['Prognose Group'].cat.add_categories([
                                                                                 '0-5', '5-10', '10-15+'])
    dataframe['Prognose Group'] = dataframe['Prognose Group'].replace(
        {"Group 1": "0-5", "Group 2": "5-10", "Group 3": "10-15+"})

    # rename the Prognose Group column to Prognose
    dataframe = dataframe.rename(columns={'Prognose Group': 'Prognose'})

    scatterPlot_megatrend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('square'),
        color=alt.value('#1f77b4'),
        xOffset=alt.value(10)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPLot_treiber = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('cross'),
        color=alt.value('#9467bd'),
        xOffset=alt.value(20)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_trend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('circle'),
        color=alt.value('#ff7f0e'),
        xOffset=alt.value(-10)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_signal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('triangle'),
        color=alt.value('#2ca02c'),
        xOffset=alt.value(-20)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_schwachesSignal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Impact', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('diamond'),
        color=alt.value('#d62728')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot = scatterPlot_megatrend + scatterPLot_treiber + \
        scatterPlot_trend + scatterPlot_signal + scatterPlot_schwachesSignal

    return scatterPlot


def plotAllOverTimeCertainty(dataframe, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height):
    # take the dataframe and change the all values in the column Prognose Group based on the following rules: Prognose Group 1 to "0-5", Prognose Group 2 to "5-10" and Prognose Group 3 to "10-15+"
    dataframe['Prognose Group'] = dataframe['Prognose Group'].replace(
        {"Group 1": "0-5", "Group 2": "5-10", "Group 3": "10-15+"})

    # rename the Prognose Group column to Prognose
    dataframe = dataframe.rename(columns={'Prognose Group': 'Prognose'})

    scatterPlot_megatrend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Megatrend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Certainty', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('square'),
        color=alt.value('#1f77b4'),
        xOffset=alt.value(10)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPLot_treiber = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Treiber')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Certainty', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('cross'),
        color=alt.value('#9467bd'),
        xOffset=alt.value(20)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_trend = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Trend')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Certainty', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('circle'),
        color=alt.value('#ff7f0e'),
        xOffset=alt.value(-10)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_signal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Certainty', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('triangle'),
        color=alt.value('#2ca02c'),
        xOffset=alt.value(-20)
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot_schwachesSignal = alt.Chart(dataframe.loc[(dataframe['Kategorie'] == 'Schwaches Signal')]).mark_point(size=symbol_size).encode(
        x=alt.X('Prognose', scale=alt.Scale(zero=False)),
        y=alt.Y('Certainty', scale=alt.Scale()),
        tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie',
                 'Certainty', 'Impact', 'Prognose'],
        shape=alt.value('diamond'),
        color=alt.value('#d62728')
    ).properties(
        width=chart_width,
        height=chart_height,
    ).interactive()

    scatterPlot = scatterPlot_megatrend + scatterPLot_treiber + \
        scatterPlot_trend + scatterPlot_signal + scatterPlot_schwachesSignal

    return scatterPlot

def plotAllSteepOverTime(dataframe, symbol_size, x_axis, y_axis_with_labels, megatrend_symbol, megatrend_color, chart_width, chart_height, ):
    #remap the steep categories to their first letter
    dataframe['STEEP-Kategorie'] = dataframe['STEEP-Kategorie'].map({'Social': 'SOC', 'Technological': 'TEC', 'Environmental': 'ENV', 'Economical': 'ECO', 'Political': 'POL'})
    dataframe = dataframe.rename(columns={'Prognose Group': 'Prognose'})

    chartGroupOne = alt.Chart(dataframe.loc[(dataframe['Prognose'] == '0-5')]).mark_circle().encode(
    # Kombiniere die Time- und Category-Informationen für die x-Achse
    x=alt.X('STEEP-Kategorie:N', sort=["SOC", "TEC", "ENV", "ECO", "POL"], axis=alt.Axis(title='0-5'), scale=alt.Scale(domain=['SOC', 'TEC', 'ENV', 'ECO', 'POL'])),
    y='Impact:Q',
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose'],
    ).properties(
    title='STEEP Scatter-Plot'
    )

    chartGroupTwo = alt.Chart(dataframe.loc[(dataframe['Prognose'] == '5-10')]).mark_circle().encode(
    x=alt.X('STEEP-Kategorie:N', sort=["SOC", "TEC", "ENV", "ECO", "POL"], axis=alt.Axis(title='5-10'), scale=alt.Scale(domain=['SOC', 'TEC', 'ENV', 'ECO', 'POL'])),
    y= alt.Y('Impact:Q', axis=alt.Axis(labels=False, title='')),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose'],
    ).properties(
    )

    chartGroupThree = alt.Chart(dataframe.loc[(dataframe['Prognose'] == '10-15+')]).mark_circle().encode(
    x=alt.X('STEEP-Kategorie:N', sort=["SOC", "TEC", "ENV", "ECO", "POL"], axis=alt.Axis(title='10-15+'), scale=alt.Scale(domain=['SOC', 'TEC', 'ENV', 'ECO', 'POL'])),
    y= alt.Y('Impact:Q', axis=alt.Axis(labels=False, title='')),
    tooltip=['Indikator', 'Kategorie', 'STEEP-Kategorie', 'Certainty', 'Impact', 'Prognose'],
    ).properties(
    )

    chartGrouped = alt.hconcat(chartGroupOne, chartGroupTwo, chartGroupThree).resolve_scale(y='independent').configure_concat(
    spacing=0
    )

    return chartGrouped