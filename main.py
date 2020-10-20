import pandas as pd
import altair as alt
import streamlit as st
import pydeck as pdk
import numpy as np

alt.data_transformers.disable_max_rows()

st.markdown("<h1 style='text-align: center;'>NYC Taxi analysis</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: gray;'>Made by Ihor and Yuan</h3>", unsafe_allow_html=True)
st.markdown("PLACEHOLDER. RESEARCH QUESTIONS AND GENERAL DESCRIPTION WOULD GO HERE.")
st.markdown("Data used can be found here: [taxis data](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data?select=train.csv) and [collisions data](https://www.kaggle.com/nypd/vehicle-collisions).")
st.markdown("Data is filtered to be from January 2015 to July 2015 for collisions and for January 2015 for taxis.")
 
 
# -------------------------------------------
# TAXIS PART

def load_taxi_by_time():
    return pd.read_csv("./taxi_by_hour.csv")

def load_taxi_map_pickup_dropoff():
    return pd.read_csv("./taxi_map_pickup_dropoff.csv")

taxi_map_pickup_dropoff = load_taxi_map_pickup_dropoff()
taxi_by_hour = load_taxi_by_time()
st.write("## Taxi")

st.markdown("PLACEHOLDER. TAXI-RELATED DESCRIPTION AND INSTRUCTIONS ON USAGE.")         
         

# -------------------------------------------
# MAP PART
layer = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    taxi_map_pickup_dropoff,
    get_position=['pickup_longitude', 'pickup_latitude'],
   # auto_highlight=True,
    get_radius=200,          # Radius is given in meters
    get_fill_color=[77, 5, 232, 1],  # blue rgba(31, 58, 147, 1)
    #pickable=True
    )


view_state = pdk.ViewState(
    longitude= -74.00,
    latitude= 40.75,
    zoom=9.5,
    min_zoom=8,
    max_zoom=11,
    pitch=0,
    bearing=0)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], initial_view_state=view_state, mapbox_key = "pk.eyJ1IjoieXVhbnl1YTQiLCJhIjoiY2tnaDN2ODNuMHFjdTM3cXQ1cjZ4ZjZ1bSJ9.7Rc5ptwp4PBKWFHC8iwPWg",
             map_style="mapbox://styles/mapbox/light-v9")
st.sidebar.write("NYC map for reference:")
st.sidebar.write(r)

with st.spinner(text="Loading..."):
    selector_pick = alt.selection_interval(empty='none', encodings=['x', 'y'])
    selector_drop = alt.selection_interval(empty='none', encodings=['x', 'y'])
    binding_weekend = alt.binding_checkbox(name="weekend")
    weekend = alt.selection_single(name=None, fields=['weekend'], bind=binding_weekend, init={'weekend': True})
    binding_weekday = alt.binding_checkbox(name="weekday")
    weekday = alt.selection_single(name=None, fields=['weekday'], bind=binding_weekday, init={'weekday': True})
    
    
    taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Dropoffs (selectable)").mark_square(size=5).encode(
        alt.X('dropoff_latitude', title='dropoff latitude', scale=alt.Scale(zero=False, domain=[40.6, 40.9])),
        alt.Y('dropoff_longitude', title='dropoff longitude', scale=alt.Scale(zero=False, domain=[-74.05, -73.75])),
        color = alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
        opacity=alt.condition(selector_drop, alt.value(1), alt.value(0.1))
    ).add_selection(
            selector_pick
    ).add_selection(
        weekend
    ).add_selection(
        weekday
    ).transform_calculate(
        selected_weekend = weekend["weekend"],
        selected_weekday = weekday["weekday"]
    ).transform_filter(
        {'or': [
                "toBoolean(datum.weekend) == datum.selected_weekend[0]", 
                "toBoolean(datum.weekday) == datum.selected_weekday[0]"
            ]}
    )
    
    taxi_map_pickup_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Pickups (selectable)").mark_square(size=5).encode(
        alt.X('pickup_latitude', title='pickup latitude', scale=alt.Scale(zero=False, domain=[40.6, 40.9])),
        alt.Y('pickup_longitude', title='pickup longitude', scale=alt.Scale(zero=False, domain=[-74.05, -73.75])),
        color = alt.condition(selector_pick, alt.value('red'), alt.value('grey')),
        opacity=alt.condition(selector_pick, alt.value(1), alt.value(0.1))
    ).add_selection(
            selector_drop
    ).add_selection(
        weekend
    ).add_selection(
        weekday
    ).transform_calculate(
        selected_weekend = weekend["weekend"],
        selected_weekday = weekday["weekday"]
    ).transform_filter(
        {'or': [
                "toBoolean(datum.weekend) == datum.selected_weekend[0]", 
                "toBoolean(datum.weekday) == datum.selected_weekday[0]"
            ]}
    )
    
    selector_hour = alt.selection_interval(empty='all', encodings=['x'])

    hour_chart = alt.Chart(taxi_by_hour).mark_bar().encode(
        alt.X("hour", scale=alt.Scale(domain=[-0.5, 23.5], nice=False), title='Hour (selectable)'),
        alt.Y("dropoff_latitude", title="Number of rides"),
        color=alt.condition(selector_hour, alt.value('blue'), alt.value('grey')),
        opacity=alt.condition(selector_hour, alt.value(1), alt.value(0.5))
    ).properties(
        width=900,
        height=100
    ).add_selection(selector_hour)
    
    st.write((taxi_map_pickup_chart | taxi_map_dropoff_chart).transform_filter(
        selector_hour
        ) & hour_chart)
 
# -------------------------------------------
# COLLISIONS PART
    
def load_collisions():
    return pd.read_csv("./collisions.csv")
def load_collisions_by_time():
    return pd.read_csv("./collisions_counts_by_time.csv")

collisions_count = load_collisions()

collisions_counts_by_time = load_collisions_by_time()
st.write("## Collisions")

         
st.markdown("PLACEHOLDER. COLLISIONS-RELATED DESCRIPTION AND INSTRUCTIONS ON USAGE.")         
         
with st.spinner(text="Loading..."):
    slider = alt.binding_range(min=1, max=5, step=1, name="month")
    month = alt.selection_single(name=None, fields=['month'], bind=slider, init={'month': 1})
    
    binding_weekend = alt.binding_checkbox(name="weekend")
    weekend = alt.selection_single(name=None, fields=['weekend'], bind=binding_weekend, init={'weekend': True})
    binding_weekday = alt.binding_checkbox(name="weekday")
    weekday = alt.selection_single(name=None, fields=['weekday'], bind=binding_weekday, init={'weekday': True})
    selector_hour = alt.selection_interval(empty='all', encodings=['x'])
    selection = alt.selection_single(fields=['is_taxi_related'], bind='legend', nearest=True)
    
    collisions_map_plot = alt.Chart(collisions_count).mark_square(size=5).encode(
        alt.X('LATITUDE', title='latitude', scale=alt.Scale(zero=False, domain=[40.45, 40.955])),
        alt.Y('LONGITUDE', title='longitude',scale=alt.Scale(zero=False, domain=[-74.3, -73.65])),
        alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
        tooltip=[alt.Tooltip('TIME', title='Total number of collisions')],
        # opacity=alt.condition(selection, 'TIME', alt.value(0.05), title='Number of collisions', legend=None)
        opacity=alt.condition(selection, alt.value(1), alt.value(0.05), legend=None)
    ).add_selection(
        month
    ).transform_filter(
        month
    ).add_selection(
        selection
    ).properties(
        title="Collisions"
    ).add_selection(
        weekend
    ).add_selection(
        weekday
    ).transform_calculate(
        selected_weekend = weekend["weekend"],
        selected_weekday = weekday["weekday"]
    ).transform_filter(
        {'or': [
                "toBoolean(datum.weekend) == datum.selected_weekend[0]", 
                "toBoolean(datum.weekday) == datum.selected_weekday[0]"
            ]}
    )
    
    
    collisions_hour_plot = alt.Chart(collisions_counts_by_time).mark_bar().encode(
        alt.X('hour', scale=alt.Scale(zero=False), title='Hour (selectable)'),
        alt.Y('sum(DATE)', scale=alt.Scale(domain=[0,1200]), title='Total number of collisions'),
        alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
        tooltip=[alt.Tooltip('DATE', title='Number of collisions')],
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)), 
    ).add_selection(
        month
    ).transform_filter(
        month
    ).properties(
        height=300,
        width=300
    ).transform_calculate(
        selected_weekend = weekend["weekend"],
        selected_weekday = weekday["weekday"]
    ).transform_filter(
        {'or': [
                "toBoolean(datum.weekend) == datum.selected_weekend[0]", 
                "toBoolean(datum.weekday) == datum.selected_weekday[0]"
            ]}
    )

    st.write((collisions_map_plot.transform_filter(selector_hour) | collisions_hour_plot.add_selection(selector_hour)).configure_legend(
        labelFontSize=15
    ))