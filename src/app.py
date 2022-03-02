import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from pyproj import Transformer
import pandas as pd
import altair as alt
import os

# alt.data_transformers.enable("data_server")


# ---------------------------------------------------------------------------------------------------#

crime = pd.read_csv("data/processed/crime_clean.csv")


# ---------------------------------------------------------------------------------------------------#
# Dropdown lists for Neighbourhood and crime types

neighbourhood_l = (
    crime.loc[crime["NEIGHBOURHOOD"].notna(), "NEIGHBOURHOOD"].unique().tolist()
)

comp = crime.loc[crime["TYPE"].notna(), "TYPE"].unique().tolist()

week_l = crime.loc[crime["day_of_week"].notna(), "day_of_week"].unique().tolist()

# ---------------------------------------------------------------------------------------------------#
# front-end functions
# map-chart

# Pivot table for map-chart plotting
crime_plot = crime.pivot(columns="TYPE", values="LONG")
crime_map = pd.concat((crime, crime_plot), axis=1)


def plot(crime_type, neighbourhood, month_name):
    """
    Function that makes the map chart on crime density on the landing page of the dashboard
    Parameters:
    ----------
    crime_type: str
        types of crime reported in Vancouver
    neighbourhood: str
        different neighbourhoods in Vancouver
    month_name: str
        Abbreviated month names from Jan - Dec
    Returns:
    ----------
    fig
        the html map plot
    """
    if month_name == "All":

        fig = px.scatter_mapbox(
            crime_map.loc[crime_map["NEIGHBOURHOOD"] == neighbourhood],
            lat="LAT",
            lon=crime_type,
            color="TYPE",
            title=f"<b>{crime_type} Crime Density in {neighbourhood}<b>",
            color_continuous_scale="RdYlGn_r",
            center={"lat": 49.246292, "lon": -123.116226},
            zoom=11,
            mapbox_style="carto-darkmatter",
            hover_name="NEIGHBOURHOOD",
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=10),
            title_font_size=20,
            title_xanchor="center",
            title_x=0.5,
            title_y=0.97,
            title_yanchor="top",
            title_font_family="Sans-Serif",
            showlegend=False,
        )
    else:
        fig = px.scatter_mapbox(
            crime_map.loc[
                (crime_map["NEIGHBOURHOOD"] == neighbourhood)
                & (crime_map["month_name"] == month_name)
            ],
            lat="LAT",
            lon=crime_type,
            color="TYPE",
            title=f"<b>{crime_type} Crime Density in {neighbourhood}<b>",
            color_continuous_scale="RdYlGn_r",
            center={"lat": 49.246292, "lon": -123.116226},
            zoom=11,
            mapbox_style="carto-darkmatter",
            hover_name="NEIGHBOURHOOD",
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=10),
            title_font_size=20,
            title_xanchor="center",
            title_x=0.5,
            title_y=0.97,
            title_yanchor="top",
            title_font_family="Sans-Serif",
            showlegend=False,
        )
    return fig.to_html()


# bar-plot function


def plot_altair(crime_category, neighbourhood):
    if crime_category == "All":
        chart = (
            alt.Chart(
                crime.loc[crime["NEIGHBOURHOOD"] == neighbourhood],
                title=f"Total Reported Cases by Crime Types in {neighbourhood}",
            )
            .mark_bar()
            .encode(
                y=alt.Y("TYPE", sort="-x", title="Type of crime"),
                x=alt.X(
                    "count()", title="Number of crime cases", axis=alt.Axis(grid=False)
                ),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=12, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(color="#FFFFFF")
            # .configure_header(titleColor="#FFFFFF", titleFontSize=14)
            .configure_view(strokeWidth=0)
            .properties(width=700, height=500)
        )
    else:
        chart = (
            alt.Chart(
                crime.loc[
                    (crime["crime_category"] == crime_category)
                    & (crime["NEIGHBOURHOOD"] == neighbourhood)
                ],
                title=f"{crime_category}: Total Crime Reports by Crime Types in {neighbourhood}",
            )
            .mark_bar()
            .encode(
                y=alt.Y("TYPE", sort="-x", title="Type of crime"),
                x=alt.X(
                    "count()", title="Number of crime cases", axis=alt.Axis(grid=False)
                ),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=12, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(color="#FFFFFF")
            # .configure_header(titleColor="#FFFFFF", titleFontSize=14)
            .configure_view(strokeWidth=0)
            .properties(width=700, height=500)
        )
    return chart.to_html()


# ---------------------------------------------------------------------------------------------------#


app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

server = app.server
# ---------------------------------------------------------------------------------------------------#
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo-1.jpg"),
                            id="logo_image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                                "padding-left": 0,
                            },
                        )
                    ],
                    className="one column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H1(
                                    "Vancouver Crime Incidence Dashboard",
                                    style={
                                        "margin-bottom": "0px",
                                        "color": "white",
                                        "textalign": "right",
                                    },
                                ),
                                html.H3(
                                    "Incidence for 2021",
                                    style={
                                        "margin-top": "0px",
                                        "color": "white",
                                        "textalign": "right",
                                    },
                                ),
                            ]
                        )
                    ],
                    className="six column",
                    id="title",
                ),
                html.Div(
                    [
                        html.H6(
                            "Last Updated: "
                            + str(
                                pd.to_datetime("now", utc=True)
                                .tz_convert("US/Pacific")
                                .strftime("%m/%d/%Y")
                            ),
                            style={"color": "orange"},
                        )
                    ],
                    className="one-third column",
                    id="title1",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Iframe(
                            id="map-chart",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "300px",
                            },
                            srcDoc=plot(
                                crime_type="Break and Enter Commercial",
                                neighbourhood="West End",
                                month_name="All",
                            ),
                        )
                    ],
                    className="create_container ten columns",
                ),
                html.Div(
                    [
                        # need to add a chart/table by Victor
                    ],
                    className="create_container four columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            ["FILTERS"],
                            className="fix_label",
                            style={"color": "orange", "textAlign": "center"},
                        ),
                        html.Label(
                            [
                                "Select the crime type",
                                dcc.Dropdown(
                                    id="crime_type",
                                    value="Break and Enter Commercial",
                                    options=[{"label": i, "value": i} for i in comp],
                                    searchable=True,
                                    # placeholder='Select a crime type..',
                                    clearable=False,
                                    className="dcc_compon",
                                ),
                            ],
                            className="fix_label",
                            style={"color": "white"},
                        ),
                        html.Label(
                            [
                                "Select the neighborhood",
                                dcc.Dropdown(
                                    id="neighbourhood",
                                    value="West End",
                                    options=[
                                        {"label": col, "value": col}
                                        for col in neighbourhood_l
                                    ],
                                    searchable=True,
                                    # placeholder='Please select...',
                                    clearable=False,
                                    className="dcc_compon",
                                ),
                            ],
                            className="fix_label",
                            style={"color": "white"},
                        ),
                        html.Label(
                            [
                                "Select the month",
                                dcc.Dropdown(
                                    id="month_name",
                                    value="All",  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": col, "value": col}
                                        for col in [
                                            "All",
                                            "Nov",
                                            "Dec",
                                            "Jul",
                                            "Jun",
                                            "Sep",
                                            "Aug",
                                            "Mar",
                                            "Feb",
                                            "Oct",
                                            "May",
                                            "Apr",
                                            "Jan",
                                        ]
                                    ],
                                    searchable=True,
                                    # placeholder='Please select...',
                                    clearable=False,
                                    className="dcc_compon",
                                ),
                            ],
                            className="fix_label",
                            style={"color": "white"},
                        ),
                        html.Label(
                            ["---------------------"],
                            className="fix_label",
                            style={"color": "white", "textAlign": "center"},
                        ),
                        html.Label(
                            [
                                "Select crime category for total cases",
                                dcc.Dropdown(
                                    id="crime_category-widget",
                                    value="All",  # REQUIRED to show the plot on the first page load
                                    options=[
                                        {"label": col, "value": col}
                                        for col in [
                                            "All",
                                            "Violent crimes",
                                            "Property crimes",
                                            "Vehicle collision",
                                        ]
                                    ],
                                    searchable=True,
                                    # placeholder='Please select...',
                                    clearable=False,
                                ),
                            ],
                            className="fix_label",
                            style={"color": "white"},
                        ),
                        html.Label(
                            ["Data Source: "],
                            className="fix_label",
                            style={
                                "color": "orange",
                                "textAlign": "center",
                                "margin-top": "30px",
                            },
                        ),
                        html.Label(
                            [
                                html.A(
                                    "VPD Open Source",
                                    href="https://geodash.vpd.ca/opendata/#",
                                )
                            ],
                            className="fix_label",
                            style={
                                "color": "white",
                                "textAlign": "center",
                                "margin-top": "0px",
                            },
                        ),
                    ],
                    className="create_container three columns",
                ),
                html.Div(
                    [
                        html.Iframe(
                            id="histogram",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "600px",
                            },
                        )
                    ],
                    className="create_container nine columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# ---------------------------------------------------------------------------------------------------#
# backend


@app.callback(
    Output("map-chart", "srcDoc"),
    Input("crime_type", "value"),
    Input("neighbourhood", "value"),
    Input("month_name", "value"),
)
def update_output(crime_type, neighbourhood, month_name):
    return plot(crime_type, neighbourhood, month_name)


@app.callback(
    Output("histogram", "srcDoc"),
    Input("crime_category-widget", "value"),
    Input("neighbourhood", "value"),
)
def update_altair(crime_category, neighbourhood):
    return plot_altair(crime_category, neighbourhood)


if __name__ == "__main__":
    app.run_server(debug=True)
