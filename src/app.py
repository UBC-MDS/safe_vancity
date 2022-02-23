from dash import Dash, html, dcc, Input, Output
import altair as alt
import pandas as pd
alt.data_transformers.enable('data_server')

# Read in global data
crime = pd.read_csv("data/crimedata_csv_AllNeighbourhoods_2021.csv")
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

## These 2 types are too long and won't fit on the chart axis, so we make them shorter
crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Fatality)",
    "TYPE",
] = "With Fatality"
crime.loc[
    crime["TYPE"] == "Vehicle Collision or Pedestrian Struck (with Injury)",
    "TYPE",
] = "With Injury"

# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

server = app.server

app.layout = html.Div([
    html.H1('VANCOUVER CRIME RATE DASHBOARD'),
    html.Iframe(
        id='histogram',
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    dcc.Dropdown(
        id='crime_category-widget',
        value='Violent crimes',  # REQUIRED to show the plot on the first page load
        options=[{'label': col, 'value': col} for col in ["Violent crimes", "Property crimes", "Vehicle collision"]])])

# Set up callbacks/backend
@app.callback(
    Output('histogram', 'srcDoc'),
    Input('crime_category-widget', 'value'))
def plot_altair(crime_category):
    chart = alt.Chart(crime.loc[crime["crime_category"] == crime_category],
                      title=f"{crime_category}: crime cases by crime types",
                      ).mark_bar().encode(
                          y=alt.Y("TYPE", sort="-x", title='Type of crime'),
                          x=alt.X("count()", title='Number of crime cases'),
                          tooltip='count()'
                      ).interactive().properties(height=300)
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)
