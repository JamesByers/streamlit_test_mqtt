# This program publishes analytics to the web
# Author: JamesByers

import pandas as pd
import streamlit as st
import altair as alt

st.title('Backyard temperature (F)')
st.write('Measured by a Pi Pico W using MicroPython. Updated every 30 min')
st.write('')

# Read in and prep raw data
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT7WzKwr6VIXA4iGEQDBluX677Ed1UlYtOXUI4I7MwiySxa0Ja_o4Mh05nLp7MAdh8ZmyyARSexSm5x/pub?gid=0&single=true&output=csv")
df['Datetime PT'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df.drop('Datetime (Pacific Time)', axis=1, inplace=True)
df = df[~(df['Datetime PT'] < '2023-03-20 00:00')]
df['Datetime PT'] = pd.to_datetime(df['Datetime PT'],format='%-d/%-m/%-y %H:%M')
st.write(df)
df['Moving avg (3)'] = df.rolling(3).mean() 

# Publish chart of temperature over time
df2 = df[['Datetime PT','Moving avg (3)']]
chart1 = alt.Chart(df2, title= "Backyard Temperature").mark_line().encode(
    x=alt.X('Datetime PT:T', axis=alt.Axis(format="%-m/%-d/%y", tickCount="day", title=None)),
    y=alt.Y('Moving avg (3):Q', title= "Degrees F"),
    tooltip=[
        alt.Tooltip('Datetime PT', format="%-m/%-d/%y", title="Date"),
        alt.Tooltip('Datetime PT', format="%-H:%M %p", title="Time"),
        alt.Tooltip('Moving avg (3)', format=".1f", title="Temp (F)"),
    ]
)
st.altair_chart(chart1, use_container_width=True)

# Create Max/Min by day dataframe
df_day_max =  df.groupby(pd.Grouper(key='Datetime PT', axis=0, 
                      freq='1D', sort=True)).max().rename(columns={'Pi Pico Temperature (F)':'Max temp'}).drop('Moving avg (3)', axis=1)
df_day_min =  df.groupby(pd.Grouper(key='Datetime PT', axis=0, 
                      freq='1D', sort=True)).min().rename(columns={'Pi Pico Temperature (F)':'Min temp'}).drop('Moving avg (3)', axis=1)
df_day = pd.concat([df_day_min, df_day_max], axis=1).sort_index(ascending=False)
df_day.index.rename('Date', inplace= True)

# Publish Max/Min by day chart
df_day_index = df_day.reset_index()
chart2 = alt.Chart(df_day_index, title= "Max/Min by day").mark_line().transform_fold(
    fold=['Max temp','Min temp'], 
    as_=['variable', 'value']
).encode(
    x=alt.X('Date:T', axis=alt.Axis(format="%-m/%-d/%y", tickCount="day", title=None)),
    y=alt.Y('value:Q', title= "Degrees F"),
    color =alt.Color('variable:N', legend=alt.Legend(
        orient='bottom-right', title=None)),
    tooltip=[
        alt.Tooltip('Date:T', format='%m/%d/%y'),
        alt.Tooltip('Max temp', format='.1f', title='Max Temp (F)'),
        alt.Tooltip('Min temp', format='.1f', title='Min Temp (F)'),
    ]
)
st.altair_chart(chart2, use_container_width=True)

# Write table of daily Max/Min values
df_day.index = df_day.index.date
df_day.index.rename('Date', inplace= True)
st.write(df_day.round(2))

# Write table of readings
df_date_index = df.set_index('Datetime PT')
df_date_index = df_date_index.sort_index(ascending=False)
df_date_index.index = df_date_index.index.strftime('%Y-%m-%d  %H:%M')
df_date_index.index.rename('Timestamp', inplace= True)
df_date_index = df_date_index.rename(columns={"Pi Pico Temperature (F)": '     Temp F', 'Moving avg (6)': 'Moving avg'})
st.write(df_date_index.round(2))

st.write('**Data Flow**')
st.write('Sensor > Pi Pico > MQTT > HiveMQ.cloud > MQTT > Rasberry Pi Node Red > Google API > Google Sheets > Streamlit.io Python visualization')
link="**Code [repo](https://github.com/JamesByers/streamlit_test_mqtt/blob/main/code/mqtt_test1/google_sheet_001_read/google_sheet_001_read.py)**"
st.markdown(link,unsafe_allow_html=True)






