# streamlit_app.py

import pandas as pd
import streamlit as st
import altair as alt
#import numpy as np
#import time

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vScVe-xEahJ_RDa2y4l_-NlOLGg1qFUWL0jsQwVVwq-5KzAkNDdIBlye9W7h-iNkn7nX1HsTWqtAOUC/pub?gid=0&single=true&output=csv")
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df = df[~(df['Datetime (Pacific Time)'] < '2023-03-16 00:00')]
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%d/%m/%Y %H:%M')
df['Temperature moving avg'] = df.rolling(window=6).mean() 

st.title('My garage temperature (F)')
st.write('As measured by a Pi Pico W running Micro Python')
df2 = df[['Datetime (Pacific Time)','Temperature moving avg']]
st.line_chart(df2,x='Datetime (Pacific Time)')

df_day_max =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).max().rename(columns={'Pi Pico Temperature (F)':'Max temperature'}).drop('Temperature moving avg', axis=1)

df_day_min =  df.groupby(pd.Grouper(key='Datetime (Pacific Time)', axis=0, 
                      freq='1D', sort=True)).min().rename(columns={'Pi Pico Temperature (F)':'Min temperature'}).drop('Temperature moving avg', axis=1)
df_day = pd.concat([df_day_min, df_day_max], axis=1).sort_index(ascending=False)
df_day.index = df_day.index.strftime('%m/%d/%Y')
st.line_chart(df_day)

df_day_index = df_day.reset_index()
df_day_index['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'], format="$D/%M/%Y")
st.write(df_day_index)
df_day_index.dtypes

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
base = alt.Chart(df_day_index).encode(x='Datetime (Pacific Time)')

chart = alt.layer(
    base.mark_line(color='red').encode(y='Min temperature'),
    base.mark_line(color='blue').encode(y='Max temperature')
    )
#chart = alt.Chart(df_day_index).transform_fold(
 #   ['Max temperature', 'Min temperature'], as_=['Temperature (F)']
#).mark_line().encode(
#    x='Datetime (Pacific Time):T',
#    y='Temperature (F):Q',
 #   color='key:N'
#)

st.altair_chart(chart)




df_date_index = df
df_date_index.set_index('Datetime (Pacific Time)', inplace=True) 
df_date_index = df_date_index.sort_values(by='Datetime (Pacific Time)', ascending=False)
df_date_index.index = df_date_index.index.strftime('%m/%d/%Y  %I:%M %p')

#st.write(df_day_min.sort_index(ascending=False).round(2))
#st.write(df_day_max.sort_index(ascending=False).round(2))

st.write(df_day)

st.write(df_date_index.round(2))