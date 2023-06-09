# This program publishes analytics to the web
# Author: JamesByers
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(layout="wide")

st.title('Back porch temperature (F)')
st.write('Measured by a Pi Pico W, a BME280 sensor, and MicroPython')
st.write('Updated every 30 min')
st.write('')

import streamlit as st

# Read in and prep raw data
df = pd.read_csv("https://docs.google.com/spreadsheets/d/1iSZacyhgC-hp35HY-fwOgzEgPoj22BhM49HSh325-8o/gviz/tq?tqx=out:csv&sheet=raw_data")
df['Datetime PT'] = pd.to_datetime(df['Datetime (Pacific Time)'])
df.drop('Datetime (Pacific Time)', axis=1, inplace=True)
df = df[~(df['Datetime PT'] < '2023-03-20 00:00')]
df['Datetime PT'] = pd.to_datetime(df['Datetime PT'],format='%-d/%-m/%-y %H:%M')
df['Moving avg (3)'] = df["BME Temp (F)"].rolling(3).mean() 

# Publish chart of temperature over time
df2 = df[['Datetime PT','BME Temp (F)']]
df2['Datetime PT'] = df2['Datetime PT'] + pd.DateOffset(hours=7) 
df2['hot_flag'] = df2['BME Temp (F)'] >=75
temperature_chart = alt.Chart(df2, title= "Temperature").transform_calculate(
    hot = 'datum["BME Temp (F)"] >=75.0'
).mark_line().encode(  #filled=True, size=20

#temperature_chart = alt.Chart(df2, title= "Temperature").mark_line().encode(
    x=alt.X('Datetime PT:T', axis=alt.Axis(format="%-m/%-d/%y", tickCount="day", title=None)),
    y=alt.Y('BME Temp (F):Q', title= "Degrees F", impute={'value': 'np.nan'}),
#    color = ('hot:N'), #, alt.Legend=None},
    color = ('hot_flag'),
    tooltip=[
       alt.Tooltip('Datetime PT', format="%-m/%-d/%-y %-I:%-M %p", title="Time PT"),
       alt.Tooltip('BME Temp (F)', format=".1f", title="Temp (F)"),
    ],
#    color=alt.Color('BME Temp (F):Q',
#            scale=alt.Scale(
 #              domain=[0,75], 
 #               range=['blue','red'], 
 #               interpolate=None
#                ),

#    color = alt.condition('datum["BME Temp (F)"] >70', 
 #                          alt.value('red'), 
 #                          alt.value('green')
 #   ),
 ).configure_range(
        category={'scheme': 'category10'}
 ).configure_legend(
    disable=True
)
st.altair_chart(temperature_chart, use_container_width=True)

#alt.Chart(df).transform_calculate(
#    negative='datum.y < 0'
#).mark_area().encode(
#    x='x',
#    y=alt.Y('y', impute={'value': 0}),
#    color='negative:N'
#)
st.markdown("""<!---

# Chart temp and humidity together
df_temp = df[['Datetime PT','BME Temp (F)', 'Humidity']]
base = alt.Chart(df_temp).encode(
    alt.X('Datetime PT:T')#.axis(title=None) #'Temperature and Humidity'))
)
temperature_values = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y('BME Temp (F):Q')#.title('Temperature (F)', titleColor='#57A44C'),
)

humidity_values = base.mark_line(stroke='#5276A7', interpolate='monotone').encode(
    alt.Y2('Humidity:Q'), titleColor='#5276A7',)

alt.layer(temperature_values, humidity_values).resolve_scale(
     y='independent'
)
#st.altair_chart(chart3) #.resolve_scale(y='independent'))temperature_values + humidity_values

#st.altair_chart(chart3, use_container_width=True)
--->
""", unsafe_allow_html= True)

#st.altair_chart(temperature_chart,humidity_chart.resolve_scale(y='independent')) #temperature_values + humidity_values

# Create Max/Min by day dataframe
df3 = df
df3['Datetime PT'] = df3['Datetime PT'] + pd.DateOffset(hours=0)
df3 = df3.set_index(pd.DatetimeIndex(df['Datetime PT']))
df_day_max = df3.resample('D').max().rename(columns={'BME Temp (F)':'Max temp'}).drop(['Datetime PT','Pico Temp (F)','Moving avg (3)', 'Pressure', 'Humidity'], axis=1)
df_day_min = df3.resample('D').min().rename(columns={'BME Temp (F)':'Min temp'}).drop(['Datetime PT','Pico Temp (F)','Moving avg (3)', 'Pressure', 'Humidity'], axis=1)
df_day = pd.concat([df_day_min, df_day_max], axis=1).sort_index(ascending=False)
df_day.index.rename('Date', inplace= True)
df_day.sort_index()

# Publish Max/Min by day chart
df_day_index = df_day.reset_index()
df_day_index['Date'] = df_day_index['Date'] + pd.DateOffset(days=1) # This correction was needed for correct tooltip date but not clear why.
chart2 = alt.Chart(df_day_index, title= "Temperature Max/Min by day").mark_line().transform_fold(
    fold=['Max temp','Min temp'], 
    as_=['variable', 'value']
).encode(
    x=alt.X('Date:T', axis=alt.Axis(format="%-m/%-d/%y", tickCount="day", title=None)), #tickCount="day", tickBand = 'extent', bandPosition = 0.5 , 
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

#Chart of humidity over time
df_temp= df[['Datetime PT','Humidity']]
df_temp['Datetime PT'] = df_temp['Datetime PT'] + pd.DateOffset(hours=7)  
humidity_chart = alt.Chart(df_temp, title= "Humidity").mark_line().encode(
    x=alt.X('Datetime PT:T', axis=alt.Axis(format="%-m/%-d/-%y", tickCount="day", title=None)),
    y=alt.Y('Humidity:Q', title= "Humidity"),
    color = alt.value('green'),
    tooltip=[
       alt.Tooltip('Datetime PT', format="%-m/%-d/%-y %-I:%-M %p", title="Time PT"),
       alt.Tooltip('Humidity', format=".1f", title="Humidity"),
    ]
)
st.altair_chart(humidity_chart, use_container_width=True)
#
# Write table of daily Max/Min values
df4 = df_day
df4.index = df4.index.date
df4.index += pd.Timedelta('0 hours')
df4.index.rename('Date', inplace= True)
df4.rename(columns={'BME Temp (F)':'Temp (F)'}, inplace=True)
st.write(df4.round(1))

# Write table of readings
df5 = df
df5['Datetime PT'] = df5['Datetime PT'] + pd.DateOffset(hours=-0)
df_date_index = df5.set_index('Datetime PT')
df_date_index = df_date_index.sort_index(ascending=False)
df_date_index.index = df_date_index.index.strftime('%Y-%m-%d  %H:%M')
df_date_index.index.rename('Timestamp', inplace= True)
df_date_index['Pressure'] = df_date_index['Pressure']*0.029529983071445
df_date_index = df_date_index.rename(columns={"Pi Pico Temperature (F)": '     Temp F', 'Moving avg (6)': 'Moving avg', 'Pressure':'Pressure (inHg)', 'Humidity':'Humidity (Rel.)'})
df_temp = df_date_index[['BME Temp (F)', 'Pressure (inHg)', 'Humidity (Rel.)']]
df_temp['Humidity (Rel.)'] = df_temp['Humidity (Rel.)']*.01

df_temp = df_temp.style.format({'BME Temp (F)':'{:.1f}', 'Pressure (inHg)': '{:.1f}', 'Humidity (Rel.)': '{:.1%}'})
st.write(df_temp)

st.write('**Data Flow**')
st.write('Sensor > Pi Pico > MQTT > HiveMQ.cloud > MQTT > Rasberry Pi with Node Red > Google API > Google Sheets > Streamlit.io Python visualization')
link="**Code [repo](https://github.com/JamesByers/streamlit_test_mqtt/blob/main/code/mqtt_test1/google_sheet_read_bme/google_sheet_read_bme.py)**"
st.markdown(link,unsafe_allow_html=True)






