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
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%d/%m/%Y %H:%M')
df['Temperature moving avg'] = df.rolling(window=6).mean() 

st.title('My backyard temperature (F)')
st.write('As measured by a Pi Pico W running Micro Python')
df2 = df[['Datetime (Pacific Time)','Temperature moving avg']]
st.line_chart(df2,x='Datetime (Pacific Time)')

df_day_max =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).max().rename(columns={'Pi Pico Temperature (F)':'Max temp'}).drop('Temperature moving avg', axis=1)
df_day_min =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).min().rename(columns={'Pi Pico Temperature (F)':'Min temp'}).drop('Temperature moving avg', axis=1)
df_day = pd.concat([df_day_min, df_day_max], axis=1).sort_index(ascending=False)
df_day.index = df_day.index.strftime('%m/%d/%Y')
df_day.index.names = ['Date']
df_day_index = df_day.reset_index()
st.write(df_day_index)

chart2 = alt.Chart(df_day_index, title="Temperature by date (F)").mark_line().transform_fold(
    fold=['Max temp','Min temp'], 
    as_=['variable', 'value']
).encode(
    x=alt.X('Date:T', axis=alt.Axis(format="%m/%d/%y", tickCount="day"), title = 'Date'),
    y=alt.Y('value:Q', title= "Degrees F"),
    color =alt.Color('variable:N', legend=alt.Legend(
        orient='bottom-right', title=None)
    ),
)
st.altair_chart(chart2, use_container_width=True)


st.write(df_day)

df_date_index = df
df_date_index = df_date_index.set_index('Datetime (Pacific Time)')
df_date_index.index = df_date_index.index.strftime('%m/%d/%Y  %I:%M %p')
df_date_index.index.rename('Date', inplace= True)
df_date_index = df_date_index.rename(columns={"Pi Pico Temperature (F)": "Temp F", "Temperature moving avg": "Moving avg"})
df_date_index = df_date_index.sort_index(ascending=False)


st.write(df_date_index.round(2))


#st.write(df_date_index)
#st.write(df_day_min.sort_index(ascending=False).round(2))
#st.write(df_day_max.sort_index(ascending=False).round(2))
#st.write(df_day_index)
#df_day_index.dtypes

#chart = alt.Chart(df_day_index).mark_line().encode(
#    x='Datetime (Pacific Time)',
#    y='Max temperature',
#    #color='symbol:N',
#)
#chart = alt.Chart(df_day_index).mark_line().encode(
#    x=alt.X(title="Date"),
#    y=alt.Y(title="Temperature (F)"),
#    mark = 'line',   
#    line1 = alt.Chart(df_day_index.reset_index()).encode(x='Datetime (Pacific Time)', y="Max temperature"),
#    )  

    
#st.altair_chart(chart)
#, use_container_width=True)

#chart = alt.Chart(df_day_index).transform_fold(
 #   ['Max temperature', 'Min temperature'], as_=['Temperature (F)']
#).mark_line().encode(
#    x='Datetime (Pacific Time):T',
#    y='Temperature (F):Q',
 #   color='key:N'
#)





