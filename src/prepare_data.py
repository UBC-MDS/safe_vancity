# author: Arlin Cherian, Wanying Ye, Victor Francis
# date: 2022-02-25
# Cleans, preps, and pre-process VPD data and saves to csv files.

#--------------------------------------------------------------------------------------------------------#
# Import packages required for data wrangling 
import pandas as pd
import numpy as np
from pyproj import Transformer

#--------------------------------------------------------------------------------------------------------#
# read in crime data from VPD open data for 2021, additional datasets downloaded from VPD GEOdash for 
# missing X and Y coordinates specific to "Homicide" and "Offence against a Person" crime type rows within the `crime` dataset.
crime = pd.read_csv("data/raw/crimedata_csv_AllNeighbourhoods_2021.csv")
homicide = pd.read_csv("data/raw/homicide.csv")
oaap = pd.read_csv("data/raw/offenceaap.csv")

#--------------------------------------------------------------------------------------------------------#
# deleting homicide and offence against a person rows since they are missing X and Y coordinates
crime.drop(crime.index[crime['TYPE'] == 'Homicide'], inplace = True)
crime.drop(crime.index[crime['TYPE'] == 'Offence Against a Person'], inplace = True)

#--------------------------------------------------------------------------------------------------------#
# data wrangling for `homicide` dataset
homicide[['x', 'X', 'y', 'Y', 'z', 'Z']] = homicide['geometry'].str.split(':|,', 5, expand=True)
homicide = homicide.drop(['x', 'y', 'z', 'Z', 'geometry', 'City:'], axis=1)

# renaming columns
homicide = homicide.rename(columns={"Crime Type:": "TYPE", "Occurrence Date/Time:": "DATE", 
                                    "Location:": "HUNDRED_BLOCK", "Neighbourhood:": "NEIGHBOURHOOD"})

#split dates
homicide['DATE']= pd.to_datetime(homicide['DATE'])
homicide['YEAR'] = homicide.DATE.dt.year
homicide['MONTH'] = homicide.DATE.dt.month
homicide['DAY'] = homicide.DATE.dt.day
homicide['HOUR'] = homicide.DATE.dt.hour
homicide['MINUTE'] = homicide.DATE.dt.minute
homicide = homicide.drop(['DATE'], axis=1)
homicide

# merge `homicide` and `crime` datasets
crime = pd.concat((crime, homicide), axis=0, ignore_index=True)

#--------------------------------------------------------------------------------------------------------#
# data wrangling for `oaap` dataset

oaap[['x', 'X', 'y', 'Y', 'z', 'Z']] = oaap['geometry'].str.split(':|,', 5, expand=True)
oaap = oaap.drop(['x', 'y', 'z', 'Z', 'geometry', 'City:'], axis=1)
oaap

# renaming columns
oaap = oaap.rename(columns={"Crime Type:": "TYPE", "Occurrence Date/Time:": "DATE", 
                            "Location:": "HUNDRED_BLOCK", "Neighbourhood:": "NEIGHBOURHOOD"})

# split datetime
oaap['DATE']= pd.to_datetime(oaap['DATE'])
oaap['YEAR'] = oaap.DATE.dt.year
oaap['MONTH'] = oaap.DATE.dt.month
oaap['DAY'] = oaap.DATE.dt.day
oaap['HOUR'] = oaap.DATE.dt.hour
oaap['MINUTE'] = oaap.DATE.dt.minute
oaap = oaap.drop(['DATE'], axis=1)
oaap

# concat df
crime = pd.concat((crime, oaap), axis=0, ignore_index=True)

#--------------------------------------------------------------------------------------------------------#
# Convert X and Y coordinates from UTM 10N form to Longitude and Latitude for mapping 
trans = Transformer.from_crs(
    "+proj=utm +zone=10 +ellps=WGS84",
    "epsg:4326",
    always_xy=True,
)
xx, yy = trans.transform(crime["X"].values, crime["Y"].values)
crime["LONG"] = xx
crime["LAT"] = yy


#--------------------------------------------------------------------------------------------------------#
# Adding a column for crime categories based on crime type
crime.loc[
    crime["TYPE"] == "Offence Against a Person",
    "crime_category",
] = "Violent crimes"
crime.loc[
    crime["TYPE"] == "Mischief",
    "crime_category",
] = "Violent crimes"
crime.loc[
    crime["TYPE"] == "Homicide",
    "crime_category",
] = "Violent crimes"

crime.loc[
    crime["TYPE"] == "Theft from Vehicle",
    "crime_category",
] = "Property crimes"
crime.loc[
    crime["TYPE"] == "Break and Enter Commercial",
    "crime_category",
] = "Property crimes"
crime.loc[
    crime["TYPE"] == "Break and Enter Residential/Other",
    "crime_category",
] = "Property crimes"
crime.loc[
    crime["TYPE"] == "Theft of Bicycle",
    "crime_category",
] = "Property crimes"
crime.loc[
    crime["TYPE"] == "Theft of Vehicle",
    "crime_category",
] = "Property crimes"
crime.loc[
    crime["TYPE"] == "Other Theft",
    "crime_category",
] = "Property crimes"

crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Injury)",
    "crime_category",
] = "Vehicle collision"
crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Fatality)",
    "crime_category",
] = "Vehicle collision"


#--------------------------------------------------------------------------------------------------------#
## Renaming crime types for plot fit and formatting 
crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Fatality)",
    "TYPE",
] = "Vehicle collision, Injured"
crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Injury)",
    "TYPE",
] = "Vehicle collision, Fatal"

#--------------------------------------------------------------------------------------------------------#
# Further data wrangling
crime['month_name'] = crime['MONTH'].apply(lambda x: calendar.month_abbr[x])
crime['date'] = pd.to_datetime(crime[['YEAR', 'MONTH', 'DAY']])
crime = crime.assign(day_of_week = crime['date'].dt.day_name())
#--------------------------------------------------------------------------------------------------------#
# save cleaned dataset to data folder 
crime.to_csv('data/processed/crime_clean.csv', index=False) 






