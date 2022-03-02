## Milestone 2 Reflection: Foundation Shades Across the Globe

### 1. What we have implemented

We have made implementations that we proposed in our Milestone 1 proposal. These implementations include:

1. Map of `Crime Density by Neighbourhood, Crime Type, and  Month`;

2. Bar Chart of `Crime Type and corresponding Total Reported Cases by Neighbourhood`;

3. Bar Chart of `Crime Category and corresponding Total Reported Cases by Weekday`;

### 2. What we decided not to implement

We decided not to include the `date range` and `time range` filters in our dashboard because:

* it allows for too much granularity that may not necessarily be important for a potential end user of our dashboard, instead we implemented other less granular filters that we thought might be more relevant to a regular user;

* Too many filters will lead to clumsiness of the dashboard which may dissuade a potential user; 

### 3. What we think our dashboard does well

Our current dashboard has included all the basic functionalities that we planned to have from Milestone 1, including the capabilities of:

* Ability to show the crime densities in specific neighbourhoods, filterable by crime type and month of the year;

* A crime category filter to ensure groupings of similar crimes in clusters;

* Ability to show the different crime types and the corresponding total number of reported crime incidents, filterable by neighbourhood;

* Ability to show the different crime categories and the corresponding total number of reported crime incidents, filterable by weekday;

### 4. What are the limitations

The limitations of our dashboard include:

* Small dataset. The dataset used was for January to December 2021 as released by Vancouver Police Department. It could have been better if we also used crime dataset for preceeding years.
  
* We did not implement complete reproducibility. That is, for example, this dashboard will not get updated if Vancouver Police Department releases more recent crime data on their website.

### 5. What are potential improvements & additions

If we had more time in the future, we have a couple of potential additions in mind:

* Add more granularities by implementing time and date filters. We would have to also redesign the dashboard so it doesn't look clumsy because of the new additions.

* Implement complete reproducibility. This is most especially important for the underlying dataset so that the dashboard gets updated as soon as the Vancouver Police Department releases new crimes data.

* Also, we would use a larger dataset, probably as much as 10 years of crimes data instead of one year's data that we currently have.