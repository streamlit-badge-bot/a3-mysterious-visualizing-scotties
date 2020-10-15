import pandas as pd
import altair as alt
import streamlit as st

alt.data_transformers.disable_max_rows()

st.markdown("<h1 style='text-align: center;'>NYC Taxi analysis</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: gray;'>Made by Ihor and Yuan</h3>", unsafe_allow_html=True)
st.write("")
 
@st.cache
def load_taxi():
    return pd.read_csv("./taxi_cleaned_m1.csv").drop(columns="Unnamed: 0")
@st.cache
def load_taxi_map_pickup_dropoff():
    return pd.read_csv("./taxi_map_pickup_dropoff.csv")

taxi_map_pickup_dropoff = load_taxi_map_pickup_dropoff()
taxi = load_taxi()
st.write("## Taxi")
st.write(taxi.head())

selector_pick = alt.selection_interval(empty='none', encodings=['x', 'y'])
selector_drop = alt.selection_interval(empty='none', encodings=['x', 'y'])

taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Dropoffs").mark_square(size=5).encode(
    alt.X('dropoff_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.955])),
    alt.Y('dropoff_longitude', scale=alt.Scale(zero=False, domain=[-74.2, -73.65])),
#     alt.Color('time', title='Number of dropoffs'),
    color = alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
#    tooltip=[alt.Tooltip('fare_amount', title='Number of dropoffs')]
).add_selection(selector_pick)

taxi_map_pickup_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Pickups").mark_square(size=5).encode(
    alt.X('pickup_latitude', scale=alt.Scale(zero=False, domain=[40.5, 40.955])),
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

st.write((taxi_map_pickup_chart | taxi_map_dropoff_chart).transform_filter(
    selector_hour
    ) & hour_chart)
 

@st.cache
def load_collisions():
    return pd.read_csv("./collisions.csv").drop(columns="Unnamed: 0")

collisions = load_collisions()
collisions.loc[:,'month'] = pd.to_datetime(collisions.DATE).dt.month
st.write("## Collisions")
st.write(collisions.head())

collisions_count = collisions.copy()    

collisions_count.LATITUDE = pd.cut(collisions_count.LATITUDE, 100)
collisions_count.LONGITUDE = pd.cut(collisions_count.LONGITUDE, 100)
collisions_count.LATITUDE = pd.IntervalIndex(collisions_count.LATITUDE).left
collisions_count.LONGITUDE = pd.IntervalIndex(collisions_count.LONGITUDE).left
collisions_count = collisions_count.groupby(['LATITUDE', 'LONGITUDE', 'month', 'hour', 'is_taxi_related']).count().TIME.reset_index()

slider = alt.binding_range(min=1, max=5, step=1, name="month")
month = alt.selection_single(name=None, fields=['month'], bind=slider, init={'month': 1})

selection = alt.selection_single(fields=['is_taxi_related'], bind='legend', nearest=True)

collisions_map_plot = alt.Chart(collisions_count).mark_square(size=5).encode(
    alt.X('LATITUDE', scale=alt.Scale(zero=False, domain=[40.45, 40.955])),
    alt.Y('LONGITUDE', scale=alt.Scale(zero=False, domain=[-74.3, -73.65])),
   alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
#     color=alt.condition('datum.is_taxi_related', alt.ColorValue('red'), alt.ColorValue('green'), title='Is taxi related'),
    tooltip=[alt.Tooltip('TIME', title='Number of collisions')],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.05))
).add_selection(
    month
).transform_filter(
    month
).add_selection(
    selection
).properties(
    title="Collisions"
)

collisions_counts_by_time = collisions.groupby(['month', 'hour', 'is_taxi_related']).count().DATE.reset_index()

collisions_hour_plot = alt.Chart(collisions_counts_by_time).mark_bar().encode(
    alt.X('hour', scale=alt.Scale(zero=False), title='Hour'),
    alt.Y('DATE', scale=alt.Scale(zero=False)),
    alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
    tooltip=[alt.Tooltip('DATE', title='Number of collisions')],
    opacity=alt.condition(selection, alt.value(1), alt.value(0.1))
).add_selection(
    month
).transform_filter(
    month
).properties(
    height=300,
    width=300
)

st.write((collisions_map_plot.transform_filter(selector_hour) | collisions_hour_plot.add_selection(selector_hour)).configure_legend(
    labelFontSize=15
) )