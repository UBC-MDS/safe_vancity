## Milestone 2 Reflection: Safe Vancity Dashboard App

### 1. What we have implemented

We have made most of the implementations that we proposed in our Milestone 1 proposal with some exceptions and additions to the previous proposal. Our current implementations include:

1. An interactive map of `Crime Density by Neighbourhood, Crime Type, and  Month`;

2. An interactive bar chart of `Total Reported Cases by Neighbourhood and Crime Type`;

3. An interactive bar chart of `Total Reported Cases per Crime Category by Weekday`;

### 2. What we decided not to implement

We decided not to include the `date range` and `time range` filters in our dashboard because:

* it allows for too much granularity that may not necessarily be important for a potential end user of our dashboard, instead we implemented other less granular filters that we thought might be more relevant to a regular user like filtering by `month` since we are only including data from 2021.  

* Too many filters will lead to clumsiness of the dashboard which may dissuade a potential user.  

* We also decided not to include the Top 3 crimes table that was mentioned in the proposal becuase this information was evident from the bar chart that reported total cases as we have displated this in descending order. Instead, we replaced this section with a bar plot that looks at total reported cases by crime category and weekday.  

### 3. What we think our dashboard does well

Our current dashboard has included all the basic functionalities that we planned to have from Milestone 1, including the capabilities of:

* Ability to show the crime densities in specific neighbourhoods, filterable by crime type and month of the year.  

* A crime category filter to ensure groupings of similar crimes in clusters.  

* Ability to show the different crime types and the corresponding total number of reported crime incidents, filterable by neighbourhood.  

* Ability to show the different crime categories and the corresponding total number of reported crime incidents, filterable by weekday.  

### 4. What are the limitations

The limitations of our dashboard include:

* Small dataset. The dataset used was for January to December 2021 as released by Vancouver Police Department. It could have been better if we also used crime dataset for preceeding years.
  
* We did not implement complete reproducibility. That is, for example, this dashboard will not get updated if Vancouver Police Department releases more recent crime data on their website.

### 5. What are potential improvements & additions

If we had more time in the future, we have a couple of potential additions in mind:

* Add more granularities by implementing time and date filters when data for additional years are included. We would have to also redesign the dashboard so it doesn't look clumsy because of the new additions.

* Implement complete reproducibility. This is most especially important for the underlying dataset so that the dashboard gets updated as soon as the Vancouver Police Department releases new crimes data.

* Also, we would use a larger dataset, probably as much as 10 years of crimes data instead of one year's data that we currently have.
