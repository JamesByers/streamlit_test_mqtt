# streamlit_app.py

import pandas as pd
import streamlit as st
import numpy as np

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

# Print results.
#for row in df.itertuples():
#    st.write(f"{row.name} has a :{row.pet}:")
#    st.write(f"{row}")


#chart_data = pd.DataFrame(
#    np.random.randn(20, 3),
#    columns=['a', 'b', 'c'])

#st.line_chart(df)
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)
