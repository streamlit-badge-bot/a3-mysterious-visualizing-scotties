import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

alt.data_transformers.disable_max_rows()

@st.cache
def load_taxi():
    return pd.read_csv("./taxi_cleaned_m1.csv")

taxi = load_taxi()
st.write("# Taxi")
st.write(taxi.head())

taxi_map_pickup_dropoff = taxi.copy()
taxi_map_pickup_dropoff.dropoff_latitude = taxi_map_pickup_dropoff.dropoff_latitude.round(3)
taxi_map_pickup_dropoff.dropoff_longitude = taxi_map_pickup_dropoff.dropoff_longitude.round(3)
taxi_map_pickup_dropoff.pickup_latitude = taxi_map_pickup_dropoff.pickup_latitude.round(3)
taxi_map_pickup_dropoff.pickup_longitude = taxi_map_pickup_dropoff.pickup_longitude.round(3)
taxi_map_pickup_dropoff = taxi_map_pickup_dropoff.groupby(['pickup_latitude', 'pickup_longitude', 
                                                           'dropoff_latitude', 'dropoff_longitude', 'hour'])\
                                                 .count().reset_index()

taxi_map_pickup_dropoff = taxi_map_pickup_dropoff.sample(frac=0.1)

selector_pick = alt.selection_interval(empty='none', encodings=['x', 'y'])
selector_drop = alt.selection_interval(empty='none', encodings=['x', 'y'])

taxi_map_pickup_chart = alt.Chart(taxi_map_pickup_dropoff).mark_circle(size=2).encode(
    alt.X('dropoff_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.9])),
    alt.Y('dropoff_longitude', scale=alt.Scale(zero=False, domain=[-74.2, -73.7])),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
#    tooltip=[alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_pick)

taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff).mark_circle(size=2).encode(
    alt.X('pickup_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.9])),
    alt.Y('pickup_longitude', scale=alt.Scale(zero=False, domain=[-74.2, -73.7])),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_pick, alt.value('red'), alt.value('grey')),
#    tooltip = [alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_drop)

selector_hour = alt.selection_interval(empty='all', encodings=['x'])

hour_chart = alt.Chart(taxi.groupby("hour").count().dropoff_latitude.reset_index()).mark_bar().encode(
    alt.X("hour"),
    alt.Y("dropoff_latitude", title="Number of rides"),
    color = alt.condition(selector_hour, alt.value('blue'), alt.value('grey')),
).properties(
    width=900,
    height=100
).add_selection(selector_hour)

((taxi_map_pickup_chart | taxi_map_dropoff_chart).transform_filter(
    selector_hour
) & hour_chart)