# NYC Taxi Analysis

## Abstract

[!APP Screenshot- Taxi Gif](taxi.gif)

It is well-know that the traffic in New York City can be quite troublesome. Generally, people are encouraged to take the subway rather than ordering a taxi. In this project, we are trying to find how taxi moves around New York City across different time and how it is related to collision accidents. This information is useful not only for city planners to prevent traffic congestion but also for individuals who could better plans ahead when needs to take a taxi.

To answer the questions we have,  we used data from the [**Kaggle website**](https://www.kaggle.com). The datasets are [**taxis data**](https://www.kaggle.com/c/new-york-city-taxi-fare-prediction/data?select=train.csv) and [**collisions data**](https://www.kaggle.com/nypd/vehicle-collisions).  Data is filtered to be in January of 2015 for **taxis data** and the same for **collisions data**.

Data analysis is performed and several interactive plots are presented in the App. We first made an interactive plot for people to explore the changes in taxi pick up locations and taxi drop off locations across different hours.  We then made an interactive plot for people to discover how taxi-related collision accidents change across time and locations. What's more, we also provided an interactive map for reference in case people are interested in diving into the details of the locations. 


## Project Goals

 The goal of this project is to build interactive tools to enable users to discover how taxi moves around New York City across different time and how it is related to collision accidents.  Both city planners and individuals can benefit from this information for better planning.

 Specifically, we have broken down the high-level questions into two series of research questions:

- [ ]  **Question 1**: How taxi moved around New York City across different hours? Where did people from downtown Manhattan go?  Where did people from outside of Manhattan go? Is there a difference between weekdays and weekends? 

- [ ] **Question 2**: Where did taxi-related collision accidents happen?  Did they happen more on rush hours?  Is there a difference between weekdays and weekends?


These questions are important. City planners can use this information to find the congestion areas and improve traffic control and infrastructure accordingly. Taxi Passengers could know when and where to avoid heavy traffic.

With the importance of the goals bearing in mind, how to effectively design the visualization tools to answer those questions is our main task.


## Design

To explain our key design decisions,  rationales, and approaches for solutions are discussed in the order of research questions.

### Design decisions for Question 1 

To answer the question of "How taxi moved around New York City across different time",  we focused on these key features:

-  **Interactions**: we provide users an interactive plot with three sub-plots: Taxi Pickups location plot,  Taxi Drop off location plot, and bar plots for the number of total rides across 24 hours. Users can select a specific region they are interested in one of the location plots, the corresponding locations are highlighted in blue in the other plots.  What's more, users can then choose a range of hours and move the slider on the bar plots to observe how the pickups and drop-offs change across different time. 

-  **Filter for weekdays and weekend**: To enable users to compare the difference between weekdays and weekends,  we also provide a checkbox as a filter.

This interactive plot enable uses to discover how taxi from a specific region moved across the city and how it changed across 
different hours and across weekdays and weekends. 

A lot of interesting findings can be discovered through this interaction plot.  For example, there are more people who took a taxi in downtown Manhattan went outside of Manhattan Island  in the evening time (8:00 pm to 11:00 pm)  than those in the morning time (7:00 am to 10:00 am).  


### Design decisions for Question 2

To answer the question of  how the movement of a taxi is related to collision accidents,  we focused on these key features:

  **Interactions**: we provide users an interactive plot with two sub-plots: Collisions location plot and bar plot for the number of total collisions across 24 hours. Users can choose the range of hours on the bar plot, the corresponding collision locations are highlighted on the location plot

**Selection on the Map and project to the Bar plot**: We initially tried to add another interaction between Collisions location plot and bar plot for the number of total collisions across 24 hours so that users can select an area and the corresponding statistics will be shown on the bar plot. However, due to the existing Vega bug,  it was not possible to implement and we had to forgo this design idea.

**Color Encoding**: To differentiate whether the collision is taxi-related or not, we use the orange color to represent taxi-related collisions while the green color for no-taxi-related-collisions.

 **Filter for weekdays and weekend**: To enable users to compare the difference between weekdays and weekends,  we also provide a checkbox as a filter.

This interactive plot enable uses to discover how the taxi-related collisions changed across different hours and across weekdays and weekends.  Also, by combining this interactive plot with the previous one, one can identify where the taxi-related collisions are mostly located.

A lot of interesting findings can be discovered through this interaction plot.  For example, overall there are more taxi-related collisions from 10:00 am to 5:00 pm and most of the collisions are located in the downtown Manhattan area.


### Design decisions for the Map 

Since the main part of the data is location-related data,  how to use a map to represent the location information is one major feature we spent a lot of time on. 

 **Layering vs Using the map for reference**: At first, we tried to use the Pydeck package to directly plot the data on the map. It's good in a way that users can see exactly where the location is and can zoom in or zoom out to explore the pattern. The biggest drawback of this approach is that the plot created by Pydeck package can not have interactions with other plots. So there is no way for users to select a specific region they are interested in and observe the corresponding locations change in the other plot.  Since we think the interaction for selection is one of the key features, we have to compromise. The final design decision we have made is plotting the map plot as a reference on the sidebar while keeping the main plots as they are. In this way,  If users find a location on the main plots that interest them, they can use the map on the sidebar to dive in for more details. 

**Zoom in and Zoom out**:  The map is interactive.  If users find a location on the main plots that interest them, they can use the map to find where is this location and  zoom-in to find details or zoom-out to get the ideal of the big picture.


### Design decisions for the size of the data
**Half-a-year data vs one-month data**:  Initially, we planned to use half-a-year data in 2015 for both taxi data and collisions data. However, we deployed to the Streamlit, we found the loading takes too much time and the response for the webpage is very slow. This created a bad user experience when the selection features are used since everything on the plot was slow. To improve the user experience, we have to cut the size of the data. After several experiments, we finally decided on the size of the data as one month.


## Development

 The whole development process is divided into four stages:
 
 - **EDA**
> Both of the team members did the EDA work on their own and discussed their findings.  Data cleaning and data aggregation were performed in this stage. Initial draft plots were performed as well.  In total,  15 hours were spent on the EDA part.

- **Set Research Questions and Key Design Features**
> Both of the team members discussed the research questions together and decided on the key design features. In total, 6 hours were spent on this part.


- **Implementation on Streamlit**
> The team member Ihor did most of the implementations for the main plots on Streamlit. The team member Yuan explored options for map interaction and implemented the map plot. In total, 20 hours were spent on this part. This is the most challenging part. Since we experienced serval Veg bugs when making the interactive plots. We had to learn how to deal with these bugs and adjusted the design idea accordingly. For example, Streamlit always interprets booleans as integers and we needed to learn Vega expressions. The data was too big to visualize it all together and we had to cut the size. And it was conceptually challenging to implement plots showing connections between pickup locations and drop off locations without making charts too messy.

- **Narratives and Write-ups**:
> Team member Yuan did most of the narratives and write-ups. In total, 7 hours were spent on this part. 

,

