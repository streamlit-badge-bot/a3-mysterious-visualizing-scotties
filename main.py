import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import streamlit as st

alt.data_transformers.disable_max_rows()

st.write("# Beatiful title will be here!")
st.write("### Made by Ihor and Yuan")
         
@st.cache
def load_taxi():
    return pd.read_csv("./taxi_cleaned_m1.csv")

taxi = load_taxi()
st.write("## Taxi")
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

taxi_map_pickup_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Pickups").mark_circle(size=2).encode(
    alt.X('dropoff_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.9])),
    alt.Y('dropoff_longitude', scale=alt.Scale(zero=False, domain=[-74.2, -73.65])),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
#    tooltip=[alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_pick)

taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Dropoffs").mark_circle(size=2).encode(
    alt.X('pickup_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.9])),
    alt.Y('pickup_longitude', scale=alt.Scale(zero=False, domain=[-74.2, -73.65])),
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

st.write((taxi_map_dropoff_chart | taxi_map_pickup_chart).transform_filter(
    selector_hour
    ) & hour_chart)


@st.cache
def load_collisions():
    return pd.read_csv("./collisions.csv")

collisions = load_collisions()
collisions.loc[:,'month'] = pd.to_datetime(collisions.DATE).dt.month
st.write("## Collisions")
st.write(collisions.head())

collisions_count_month = collisions.copy()
collisions_count_month.LATITUDE = collisions_count_month.LATITUDE.round(3)
collisions_count_month.LONGITUDE = collisions_count_month.LONGITUDE.round(3)
collisions_count_month = collisions_count_month.groupby(['LATITUDE', 'LONGITUDE', 'month']).count().TIME.reset_index()

slider = alt.binding_range(min=1, max=5, step=1, name="month")
month = alt.selection_single(name=None, fields=['month'], bind=slider, init={'month': 1})

collisions_map_plot = alt.Chart(collisions_count_month).mark_circle(size=2).encode(
    alt.X('LATITUDE', scale=alt.Scale(zero=False, domain=[40.45, 40.955])),
    alt.Y('LONGITUDE', scale=alt.Scale(zero=False, domain=[-74.3, -73.65])),
    alt.Color('TIME', title='Number of collisions', scale=alt.Scale(zero=False, domain=[0,20])),
    tooltip=[alt.Tooltip('TIME', title='Number of collisions')]
).add_selection(
    month
).transform_filter(
    month
)

collisions_counts_by_time = collisions.groupby(['month', 'TIME']).count().DATE.reset_index()
collisions_counts_by_time.TIME = collisions_counts_by_time.TIME.apply(lambda x: pd.Timestamp(x))
collisions_counts_by_time.TIME = pd.cut(collisions_counts_by_time.TIME, 24)
collisions_counts_by_time.TIME = pd.IntervalIndex(collisions_counts_by_time.TIME).left
collisions_counts_by_time.TIME = collisions_counts_by_time.TIME.dt.hour

collisions_hour_plot = alt.Chart(collisions_counts_by_time).mark_bar().encode(
    alt.X('TIME', scale=alt.Scale(zero=False), title='Hour'),
    alt.Y('DATE', scale=alt.Scale(zero=False)),
    tooltip=[alt.Tooltip('DATE', title='Number of collisions')]
).add_selection(
    month
).transform_filter(
    month
).properties(
    height=300,
    width=300
)

st.write(collisions_map_plot | collisions_hour_plot)