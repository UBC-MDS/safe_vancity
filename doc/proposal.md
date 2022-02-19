
# Motivation and Purpose

**Our role**: Data Science team at VanRealtor

**Target audience**: Real estate customers looking to buy properties in
Vancouver neighborhoods and Real estate agents at VanRealtor looking for
listings in safer neighborhoods to attract more clients.

Being the largest city in British Columbia, Vancouver is an attractive
city to call home for many. Reasons include its vast ethnic diversity,
natural landscape, coastal, foresty, job market and so on. Despite the
vibrant quality of this city, an important factor when deciding to live
in a specific city depends on the safety of its neighborhoods, along
with other factors such as access to essential services, cost of living
etc. Research evidence have shown that crime types have had significant
changes during COVID at neighborhood levels in Vancouver (Anderson and
Hodgkinson 2022). For example, assault cases, arson and robbery have
increased in Vancouver’s Downtown core, Strathcona and Mount Pleasant
areas. At VanRealtor, we wanted to offer our clients the decision to
choose their next neighborhood to move, rent or visit while being aware
of the crimes statistics of the city. This dashboard allows people to
search for crime related information by neighborhoods in Vancouver using
data from 2021. Users can also filter data based on geological location,
most common crime types by neighbourhood, time of the crime event and
crime density by location.

# Data Description

The dataset used in this project was sourced from the Vancouver Police
Department’s website. It is publicly available and accessed from
[here](https://geodash.vpd.ca/opendata/#). We used the 2021 crimes
dataset for all Vancouver neighbourhood to build this dashboard.
Extracted data can be found in the data folder.

The 2021 crimes dataset consists of 32,013 observations. Each
observation has 9 associated relevant variables that determine the type
of crime in various neigbhourhoods in Vancouver. These variables are
`YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, `HUNDRED_BLOCK`,
`NEIGHBOURHOOD`, `X` coordinate, and `Y` coordinate. Depending on what
values the aforementioned variables take, `TYPE` of crime can be one of
*Break and Enter Commercial*, *Break and Enter Residential/Other*,
*Homicide*, *Mischief*, *Offence Against a Person*, *Other Theft*,
*Theft from Vehicle*, *Theft of Bicycle*, *Theft of Vehicle*, *Vehicle
Collision or Pedestrian Struck (with Fatality)*, *Vehicle Collision or
Pedestrian Struck (with Injury)*.

# Research Questions and Usage Scenarios

Let’s take a look at Mary. She recently moved to Vancouver but is not
very familiar with the neighborhoods. She wants to settle down by
renting a place in Vancouver, and now she faces the problem of which
neighborhoods to choose. One important factor she takes into account is
the crime incidents. She wants to compare the safety of neighborhoods in
the aspect of least crime incidents. Moreover, since certain types of
crimes (*e.g.* homicide) are more serious and life-threatening than
others, she is also willing to know the types of crimes that occur most
frequently in a particular neighborhood. In case that she only wants to
accommodate for a short period, it would be helpful to know the specific
crime distribution during that time frame.

When Mary logs on to the “Safe Vancity App,” she can see the summary
statistics (*e.g.* the total crime incidents, the top 3 common crime
types, etc.) in Vancouver in 2021. She can then select the neighborhood
that she wants to know more, and choose a specific range of time using
the slider, she will be able to see the distribution of crime types
within the time range she chooses. For instance, she sees that during
2021-06 to 2021-08, which will be the actual duration of her residence
in Vancouver, “offense against a person” takes place quite often in
Strathcona. With this information, she decides to remove Strathcona from
her candidate list of neighborhoods.

The app also allows her to check the crime incidents in each
neighborhoods according to the crime type she chooses. When she does so,
she finds that although Kitsilano has an overall low number of crime
incidents, several homicides were recorded for this neighborhood in
2021. Thus, she might decide to look into other neighborhoods. She will
also be able to see the crime density in each neighbourhood using the
map functionality.

# References

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-vancrime" class="csl-entry">

Anderson, M., and T. Hodgkinson. 2022. “Andresen MA, Hodgkinson t. In a
World Called Catastrophe: The Impact of COVID-19 on Neighbourhood Level
Crime in Vancouver, Canada \[Published Online Ahead of Print, 2022 Jan
9\]. J Exp Criminol. 2022;1-25. Doi:10.1007/S11292-021-09495-6.”
*Journal of Experimental Criminology*, 1–25.

</div>

</div>
