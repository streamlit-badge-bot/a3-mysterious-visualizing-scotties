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
    alt.X('dropoff_latitude', scale=alt.Scale(zero=False)),
    alt.Y('dropoff_longitude', scale=alt.Scale(zero=False)),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
    tooltip=[alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_pick)

taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff).mark_circle(size=2).encode(
    alt.X('pickup_latitude', scale=alt.Scale(zero=False)),
    alt.Y('pickup_longitude', scale=alt.Scale(zero=False)),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_pick, alt.value('red'), alt.value('grey')),
    tooltip=[alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_drop)

slider = alt.binding_range(min=1, max=5, step=1)
hour = alt.selection_single(name="Slider", fields=['hour'], bind=slider)

st.write((taxi_map_pickup_chart | taxi_map_dropoff_chart).add_selection(
    hour
).transform_filter(
    hour
))