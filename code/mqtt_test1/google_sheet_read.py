# streamlit_app.py

import pandas as pd
import streamlit as st
import numpy as np
import time

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vScVe-xEahJ_RDa2y4l_-NlOLGg1qFUWL0jsQwVVwq-5KzAkNDdIBlye9W7h-iNkn7nX1HsTWqtAOUC/pub?gid=0&single=true&output=csv")
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df = df[~(df['Datetime (Pacific Time)'] < '2023-03-15 12:51')]
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%d/%m/%Y %H:%M')

st.title('My garage temperature (F)')
st.write('As measured by a Pi Pico W running Micro Python')
st.line_chart(df, x='Datetime (Pacific Time)')


df_date_index = df
df_date_index.set_index('Datetime (Pacific Time)', inplace=True) 
df_date_index = df_date_index.sort_values(by='Datetime (Pacific Time)', ascending=False)
st.write(df_date_index.round(2))
