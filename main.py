import pandas as pd
import altair as alt
import streamlit as st
import pydeck as pdk
import numpy as np

alt.data_transformers.disable_max_rows()

st.markdown("<h1 style='text-align: center;'>NYC Taxi Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: gray;'>Made by Ihor and Yuan</h3>", unsafe_allow_html=True)
st.write("## Project Overview")
st.markdown("It is well-know that the traffic in New York City can be quite troublesome. In this project, we are trying to find how taxi moves around New York City across different times and how it is related to collision accidents. This information is useful not only for city planners to prevent traffic congestion but also for individuals who could better plans ahead when needs to take a taxi. Data is filtered to be in January of 2015 for taxis data and the same for collisions data.")
st.markdown("The data is from the [**Kaggle website**](https://www.kaggle.com). The datasets are [**taxis data**](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data?select=train.csv) and [**collisions data**](https://www.kaggle.com/nypd/vehicle-collisions).")

 
# -------------------------------------------
# TAXIS PART

def load_taxi_by_time():
    return pd.read_csv("./taxi_by_hour.csv")

def load_taxi_map_pickup_dropoff():
    return pd.read_csv("./taxi_map_pickup_dropoff.csv")

taxi_map_pickup_dropoff = load_taxi_map_pickup_dropoff()
taxi_by_hour = load_taxi_by_time()


st.write("## How taxi moves around NYC over time")  
st.markdown("This plot below shows the pickup locations and the drop off locations of taxis in New York City as well as the total number of taxi rides across different hours.")   
st.markdown("Here are some motivation questions for you to discover: Where did people from downtown Manhattan go? Is there a difference between different hours?")     
st.markdown("What did you find? Let's play with it! Off-Course, you can discover more interesting findings.")
st.markdown("**Instructions for use**:")
st.markdown("-Select a region in one of the locations plots on the top row")
st.markdown("-Select a range of hours in the bar plot on the second row")
st.markdown("-Move the hours you selected across the bar plot")
st.markdown("-Observe the changes on the other location plot (points are highlighted in blue)")
st.markdown("-You can filter by weekday or weekend if needed")
st.markdown("-If you find a location that interests you,  check out the map on the left to dive in for more details")
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
    max_zoom=12,
    pitch=0,
    bearing=0)

# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], initial_view_state=view_state, mapbox_key = "pk.eyJ1IjoieXVhbnl1YTQiLCJhIjoiY2tnaDN2ODNuMHFjdTM3cXQ1cjZ4ZjZ1bSJ9.7Rc5ptwp4PBKWFHC8iwPWg",
             map_style="mapbox://styles/mapbox/light-v9")
st.sidebar.write("## NYC map for reference")
st.sidebar.write("If you find a location on the main plots that interest you, you can use the map below to dive in for more details.")
st.sidebar.write(r)

with st.spinner(text="Loading..."):
    selector_pick = alt.selection_interval(empty='none', encodings=['x', 'y'])
    selector_drop = alt.selection_interval(empty='none', encodings=['x', 'y'])
    binding_weekend = alt.binding_checkbox(name="weekend")
    weekend = alt.selection_single(name=None, fields=['weekend'], bind=binding_weekend, init={'weekend': True})
    binding_weekday = alt.binding_checkbox(name="weekday")
    weekday = alt.selection_single(name=None, fields=['weekday'], bind=binding_weekday, init={'weekday': True})
    
    taxi_map_dropoff_chart = alt.Chart(taxi_map_pickup_dropoff, title="Taxi Dropoffs (selectable)").mark_square(size=5).encode(
        alt.Y('dropoff_latitude', title='dropoff latitude', scale=alt.Scale(zero=False, domain=[40.6, 40.9])),
        alt.X('dropoff_longitude', title='dropoff longitude', scale=alt.Scale(zero=False, domain=[-74.05, -73.75])),
        color=alt.condition(selector_drop, alt.value('blue'), alt.value('grey')),
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
        alt.Y('pickup_latitude', title='pickup latitude', scale=alt.Scale(zero=False, domain=[40.6, 40.9])),
        alt.X('pickup_longitude', title='pickup longitude', scale=alt.Scale(zero=False, domain=[-74.05, -73.75])),
        color=alt.condition(selector_pick, alt.value('red'), alt.value('grey')),
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
    ).add_selection(
        selector_hour
    )
    
    st.write((taxi_map_pickup_chart | taxi_map_dropoff_chart).transform_filter(
        selector_hour
        ) & hour_chart
    )
 
# -------------------------------------------
# COLLISIONS PART
    
def load_collisions():
    return pd.read_csv("./collisions.csv")
def load_collisions_by_time():
    return pd.read_csv("./collisions_counts_by_time.csv")

collisions_count = load_collisions()

collisions_counts_by_time = load_collisions_by_time()
st.write("## How taxi-related collisions change over time") 
st.markdown("The plot below shows the location of collisions and the total number of collisions in New York City. The taxi-related collisions are highlighted in orange color.") 
st.markdown("Here are some motivation questions for you to discover : Where did most of the taxi-related collision accidents happen? Did they happen more during rush hours?")   
st.markdown("What did you find? Let's play with it! Off-Course, you can explore more questions.") 
st.markdown("Instructions for use") 
st.markdown("- Select a range of hours in the bar plot on the right")  
st.markdown("- Move the hours you selected across the bar plot") 
st.markdown("- Observe the changes in the location plot on the left ") 
st.markdown("- You can filter by weekday or weekend if needed") 
st.markdown("- If you find a location that interests you, check out the map on the left to dive in for more details.") 
  
         
with st.spinner(text="Loading..."):
    
    binding_weekend = alt.binding_checkbox(name="weekend")
    weekend = alt.selection_single(name=None, fields=['weekend'], bind=binding_weekend, init={'weekend': True})
    binding_weekday = alt.binding_checkbox(name="weekday")
    weekday = alt.selection_single(name=None, fields=['weekday'], bind=binding_weekday, init={'weekday': True})
    selector_hour = alt.selection_interval(empty='all', encodings=['x'])
    selection = alt.selection_single(fields=['is_taxi_related'], bind='legend', nearest=True)
    
    collisions_map_plot = alt.Chart(collisions_count).mark_square(size=5).encode(
        alt.Y('LATITUDE', title='latitude', scale=alt.Scale(zero=False, domain=[40.45, 40.955])),
        alt.X('LONGITUDE', title='longitude',scale=alt.Scale(zero=False, domain=[-74.3, -73.65])),
        alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
        tooltip=[alt.Tooltip('TIME', title='Total number of collisions')],
        # opacity=alt.condition(selection, 'TIME', alt.value(0.05), title='Number of collisions', legend=None)
        opacity=alt.condition(selection, alt.value(1), alt.value(0.05), legend=None)
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
    ).transform_filter(
        selector_hour
    )
    
    
    collisions_hour_plot = alt.Chart(collisions_counts_by_time).mark_bar().encode(
        alt.X('hour', scale=alt.Scale(zero=False), title='Hour (selectable)'),
        alt.Y('sum(DATE)', scale=alt.Scale(domain=[0,1150]), title='Total number of collisions'),
        alt.Color('is_taxi_related', title='Is taxi related (clickable)', scale=alt.Scale(scheme='set2')),
        tooltip=[alt.Tooltip('DATE', title='Number of collisions')],
        opacity=alt.condition(selection, alt.value(1), alt.value(0.1)), 
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
    ).add_selection(
        selector_hour
    )

    st.write((collisions_map_plot | collisions_hour_plot).configure_legend(
        labelFontSize=15
    ))