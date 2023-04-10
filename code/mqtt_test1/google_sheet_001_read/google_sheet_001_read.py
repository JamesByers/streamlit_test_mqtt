# streamlit_app.py

import pandas as pd
import streamlit as st
import altair as alt
#import numpy as np
#import time

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vT7WzKwr6VIXA4iGEQDBluX677Ed1UlYtOXUI4I7MwiySxa0Ja_o4Mh05nLp7MAdh8ZmyyARSexSm5x/pub?gid=0&single=true&output=csv")
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df = df[~(df['Datetime (Pacific Time)'] < '2023-03-20 00:00')]
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%-d/%-m/%-y %H:%M')
df['Moving avg (6)'] = df.rolling(window=6).mean() 

st.title('Backyard temperature (F)')
st.write('Measured by a Pi Pico W using MicroPython. Updated every 30 min')
st.write('')
df2 = df[['Datetime (Pacific Time)','Moving avg (6)']]
#st.line_chart(df2,x='Datetime (Pacific Time)')

chart1 = alt.Chart(df2, title= "Backyard Temperature").mark_line().encode(
    x=alt.X('Datetime (Pacific Time):T', axis=alt.Axis(format="%-m/%-d/%y", tickCount="day", title=None)),
    y=alt.Y('Moving avg (6):Q', title= "Degrees F"),
    tooltip=[
        alt.Tooltip('Datetime (Pacific Time)', format="%-m/%-d/%y", title="Date"),
        alt.Tooltip('Datetime (Pacific Time)', format="%-H:%M %p", title="Time"),
        alt.Tooltip('Moving avg (6)', format=".1f", title="Temp (F)"),
    ]
)
st.altair_chart(chart1, use_container_width=True)


df_day_max =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).max().rename(columns={'Pi Pico Temperature (F)':'Max temp'}).drop('Moving avg (6)', axis=1)
df_day_min =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).min().rename(columns={'Pi Pico Temperature (F)':'Min temp'}).drop('Moving avg (6)', axis=1)
df_day = pd.concat([df_day_min, df_day_max], axis=1).sort_index(ascending=False)
df_day.index.rename('Date', inplace= True)

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
        #alt.Tooltip('Date', format='%m/%d/%y', title='Date'),
        alt.Tooltip('Date:T', format='%m/%d/%y'),
        alt.Tooltip('Max temp', format='.1f', title='Max Temp (F)'),
        alt.Tooltip('Min temp', format='.1f', title='Min Temp (F)'),
    ]    
#    ),
)
st.altair_chart(chart2, use_container_width=True)

#df_day_index['Date'] = df_day_index['Date']
#df_day_index['Min temp'] = df_day_index['Min temp'].round(2)

df_day.index = df_day.index.date
df_day.index.rename('Date', inplace= True)
st.write(df_day.round(2))

#.format(subset=['mean'], decimal=',', precision=2).bar(subset=['mean'], align="mid")

#st.write(df_day_index[['Date','Min temp','Max temp']])

df_date_index = df
df_date_index = df_date_index.set_index('Datetime (Pacific Time)')
df_date_index = df_date_index.sort_index(ascending=False)
df_date_index.index = df_date_index.index.strftime('%Y-%m-%d  %H:%M')
df_date_index.index.rename('Timestamp', inplace= True)
df_date_index = df_date_index.rename(columns={"Pi Pico Temperature (F)": "     Temp F", "Moving avg (6)": "Moving avg"})
#df_day_index.index = df_day_index.index.date
st.write(df_date_index.round(2))

st.write('**Data Flow**')
st.write('Sensor > Pi Pico > MQTT > HiveMQ.cloud > MQTT > Rasberry Pi Node Red > Google API > Google Sheets > Streamlit.io Python visualization')
link="**Code [repo](https://github.com/JamesByers/streamlit_test_mqtt/blob/main/code/mqtt_test1/google_sheet_001_read/google_sheet_001_read.py)**"
st.markdown(link,unsafe_allow_html=True)






