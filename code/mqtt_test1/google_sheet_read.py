# streamlit_app.py

import pandas as pd
import streamlit as st
import numpy as np
import time

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=60)
st.runtime.legacy_caching.clear_cache()
#@st.cache_data(ttl=10)

#def load_data(sheets_url):
    #csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
#    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vScVe-xEahJ_RDa2y4l_-NlOLGg1qFUWL0jsQwVVwq-5KzAkNDdIBlye9W7h-iNkn7nX1HsTWqtAOUC/pub?gid=0&single=true&output=csv"
#    return pd.read_csv(csv_url)

#df = load_data(st.secrets["public_gsheets_url"])
df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vScVe-xEahJ_RDa2y4l_-NlOLGg1qFUWL0jsQwVVwq-5KzAkNDdIBlye9W7h-iNkn7nX1HsTWqtAOUC/pub?gid=0&single=true&output=csv")

#df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],infer_datetime_format=True).dt.time
#df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%d/%m/%Y %H:%M')
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df['Datetime (Pacific Time)'] = pd.to_datetime(df['Datetime (Pacific Time)'],format='%d/%m/%Y %H:%M')
df = df.sort_values(by='Datetime (Pacific Time)', ascending=False)

st.title('Pi Pico W temperature')
st.write('My garage temperature F')
st.write(df)
st.line_chart(df, x='Datetime (Pacific Time)')

#print(df.columns)
#print(df)
#st.write(df.dtypes)
#st.write(df.shape[0])
#st.write(df.columns)
#st.write(df.shape[0])
#time.sleep(5)
#st.line_chart(chart_data)

#st.title('Pi Pico W temperature')
#st.write('My garage temperature F')
#dataframe = pd.DataFrame(np.random.randn(10, 20),
#  columns = ('col %d' % i
#    for i in range(20)))
#st.write(df)

#chart_data = pd.DataFrame(
#    np.random.randn(20, 3),
#    columns=['a', 'b', 'c'])



# Print results.

#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")
#    st.write(f"{row}")


#st.line_chart(df)
# chart_data = pd.DataFrame(
#    np.random.randn(20, 3),
#    columns=['a', 'b', 'c'])
#
#st.line_chart(chart_data)
