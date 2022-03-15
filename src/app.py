import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State, no_update
from pyproj import Transformer
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import os

alt.data_transformers.disable_max_rows()

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
            title_y=0.98,
            title_yanchor="top",
            title_font_family="Sans-Serif",
            title_font_color="white",
            plot_bgcolor="#010915",
            paper_bgcolor="#010915",
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
            title_font_color="white",
            plot_bgcolor="#010915",
            paper_bgcolor="#010915",
            showlegend=False,
        )
    return fig.to_html()


# bar-plot function


def plot_altair(crime_category, neighbourhood, crime_type):
    """
    Function that makes the bar chart on crime incidences by crime categories
    and neighborhoods.

    Parameters:
    ----------
    crime_category: {"All", "Violent crimes", "Property crimes", "Vehicle collision"}
        category of crimes reported in Vancouver
    neighbourhood: str
        different neighbourhoods in Vancouver

    Returns:
    ----------
    altair chart
    """
    # Set the crime type to be highlighted to a separate value in a new column
    crime["highlight"] = False
    crime.loc[crime["TYPE"] == crime_type, "highlight"] = True
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
                color=alt.Color("highlight", legend=None),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=18, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(fontSize=18, color="#FFFFFF")
            # .configure_header(titleColor="#FFFFFF", titleFontSize=14)
            .configure_view(strokeWidth=0)
            .properties(width=650, height=500)
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
                y=alt.Y("TYPE", sort="-x", title="Crime types"),
                x=alt.X(
                    "count()", title="Number of crime cases", axis=alt.Axis(grid=False)
                ),
                color=alt.Color("highlight", legend=None),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=18, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(fontSize=18, color="#FFFFFF")
            .configure_view(strokeWidth=0)
            .properties(width=625, height=475)
        )
    return chart.to_html()


def plot_histogram(weekday, neighbourhood):
    """
    Function that makes the bar chart on crime incidences for each crime
    category by days of a week and neighborhoods.

    Parameters:
    ----------
    weekday: str
        including "All" and seven days of a week - "Monday", "Tuesday", etc.
    neighbourhood: str
        different neighbourhoods in Vancouver

    Returns:
    ----------
    altair chart
    """
    if weekday == "All":
        chart = (
            alt.Chart(
                crime.loc[crime["NEIGHBOURHOOD"] == neighbourhood],
                title=alt.TitleParams(text=f"Total Reported Crimes in {neighbourhood}"),
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "crime_category",
                    sort="-y",
                    title="Crime Category",
                    axis=alt.Axis(labelAngle=-45),
                ),
                y=alt.Y(
                    "count()", title="Number of crime cases", axis=alt.Axis(grid=False)
                ),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=16, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(fontSize=15, color="#FFFFFF")
            .configure_view(strokeWidth=0)
            .properties(width=250, height=310)
        )
    else:
        chart = (
            alt.Chart(
                crime.loc[
                    (crime["NEIGHBOURHOOD"] == neighbourhood)
                    & (crime["day_of_week"] == weekday)
                ],
                title=alt.TitleParams(
                    text=f"Total Reported Crimes on {weekday}s in {neighbourhood}"
                ),
            )
            .mark_bar()
            .encode(
                x=alt.X(
                    "crime_category",
                    sort="-y",
                    title="Crime Category",
                    axis=alt.Axis(labelAngle=-45),
                ),
                y=alt.Y(
                    "count()", title="Number of crime cases", axis=alt.Axis(grid=False)
                ),
                tooltip="count()",
            )
            .interactive()
            .configure(background="#010915")
            .configure_axis(
                titleFontSize=16, titleColor="#FFFFFF", labelColor="#FFFFFF"
            )
            .configure_title(fontSize=15, color="#FFFFFF")
            .configure_view(strokeWidth=0)
            .properties(width=250, height=310)
        )

    return chart.to_html()


# ---------------------------------------------------------------------------------------------------#


app = Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# collapse button for about section

toast = html.Div(
    [
        dbc.Button(
            "About",
            id="simple-toast-toggle",
            color="#010915",
            className="mb-3",
            n_clicks=0,
        )
    ]
)

app.title = "Safe Vancity"

server = app.server
# ---------------------------------------------------------------------------------------------------# create app layout

tab_style = {
    "borderBottom": "1px solid #d6d6d6",
    "color": "white",
    "padding": "6px",
    "backgroundColor": "#010915",
    # 'fontWeight': 'bold'
}
tab_selected_style = {
    "borderTop": "4px solid #d6d6d6",
    "borderBottom": "4px solid #d6d6d6",
    "borderLeft": "4px solid #d6d6d6",
    "borderRight": "4px solid #d6d6d6",
    "backgroundColor": "#010915",
    "color": "white",
    "padding": "6px",
    "fontWeight": "bold",
    "fontSize": 20,
}


app.layout = html.Div(
    [
        html.Div(
            [
                dbc.Button(
                    "About",
                    id="simple-toast-toggle",
                    color="white",
                    className="mb-3",
                    n_clicks=0,
                    style={"position": "fixed", "right": 90},
                ),
                dbc.Toast(
                    [
                        html.A(
                            "GitHub",
                            href="https://github.com/UBC-MDS/safe_vancity",
                            style={"color": "orange", "text-decoration": "underline"},
                        ),
                        html.P(
                            "The dashboard was created by Arlin Cherian, Victor Francis, Wanying Ye. It is licensed under MIT license. Please visit GitHub for more information.",
                            style={"color": "white"},
                        ),
                        html.A(
                            "Dashboard description",
                            style={"color": "orange", "text-decoration": "underline"},
                        ),
                        html.P(
                            """This dashboard allows you to see crime incidence in 2021 in Vancouver neighbourhoods. By selecting a neighbourhood from the drop down menu, all the plots in the app will display metrics related to that neighbourhood. The map will display crime density by 'neighbourhood', 'crime type' and by 'month'. You can zoom into the neighbourhood to see specific streets where the crimes have happened. You can use the toggle options on the top right corner of the map to zoom in or out, pan the map and reset axes. The top-right bar plot shows the total reported crimes in a selected neighbourhood by 'day of the week' (default all days). This plot can be filtered using the 'neighbourhood' and 'day of the week' options. Finally, the bottom bar plot shows total reported crimes by crime category in each neighbourhood. Here crime types are grouped by crime categories (Violent, Property and Vehicle Collision). Default view shows the total cases for all crime categories. You can toggle through the tab options. From this plot you can see the top crimes in each neighbourhood in 2021. Some summary stats of overall reported crimes in Vancouver in 2021, total property, violent and vehicle collision crimes are reported at the very top.""",
                            style={"color": "white"},
                        ),
                    ],
                    id="simple-toast",
                    header="About",
                    icon="primary",
                    dismissable=True,
                    is_open=False,
                ),
            ],
            className="row flex-display",
        ),
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
                                "margin-bottom": "10px",
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
                                html.H2(
                                    "Vancouver Crime Incidence Dashboard",
                                    style={
                                        "margin-bottom": "0px",
                                        "color": "white",
                                        "textalign": "right",
                                    },
                                ),
                                html.H4(
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
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            children="Total crimes",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            f" 32,007",
                            style={
                                "textAlign": "center",
                                "color": "#4C78A8",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children="Total property crimes",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            f" 21,853",
                            style={
                                "textAlign": "center",
                                "color": "#4C78A8",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children="Total violent crimes",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            f" 9,114",
                            style={
                                "textAlign": "center",
                                "color": "#4C78A8",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
                html.Div(
                    [
                        html.H6(
                            children=" Total vehical collision",
                            style={"textAlign": "center", "color": "white"},
                        ),
                        html.P(
                            f" 1,040",
                            style={
                                "textAlign": "center",
                                "color": "#4C78A8",
                                "fontSize": 40,
                            },
                        ),
                    ],
                    className="card_container three columns",
                ),
            ],
            className="row flex-display",
            style={"margin-bottom": "25px", "margin-top": "25px"},
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
                                "height": "475px",
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
                        html.Iframe(
                            id="hist",
                            style={
                                "border-width": "0",
                                "width": "400px",  # "100%",
                                "height": "475px",
                            },
                        )
                    ],
                    className="create_container five columns",
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
                            style={
                                "color": "orange",
                                "textAlign": "center",
                                "fontSize": 20,
                            },
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
                                    value="All",
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
                            [
                                "Select the weekday",
                                dcc.Dropdown(
                                    id="weekday",
                                    value="All",
                                    options=[
                                        {"label": col, "value": col}
                                        for col in [
                                            "Sunday",
                                            "Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
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
                            ["Data Source: "],
                            className="fix_label",
                            style={
                                "color": "orange",
                                "textAlign": "center",
                                "margin-top": "80px",
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
                        html.Label(
                            "Last Updated: "
                            + str(
                                pd.to_datetime("now", utc=True)
                                .tz_convert("US/Pacific")
                                .strftime("%m/%d/%Y, %H:%M:%S")
                            ),
                            style={"color": "orange", "margin-top": "25px", "textAlign": "center",},
                        ),
                    ],
                    className="create_container three columns",
                ),
                html.Div(
                    [
                        dcc.Tabs(
                            id="crime_category-widget",
                            value="All",
                            children=[
                                dcc.Tab(
                                    label="All",
                                    value="All",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Violent crimes",
                                    value="Violent crimes",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Property crimes",
                                    value="Property crimes",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Vehicle collision",
                                    value="Vehicle collision",
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                        ),
                        html.Iframe(
                            id="histogram",
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "600px",
                            },
                        ),
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
    Input("crime_type", "value"),
)
def update_altair(crime_category, neighbourhood, crime_type):
    return plot_altair(crime_category, neighbourhood, crime_type)


@app.callback(
    Output("hist", "srcDoc"), Input("weekday", "value"), Input("neighbourhood", "value"),
)
def update_histogram(weekday, neighbourhood):
    return plot_histogram(weekday, neighbourhood)


@app.callback(
    Output("simple-toast", "is_open"),
    [Input("simple-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n == 0:
        return no_update
    return True


if __name__ == "__main__":
    app.run_server(debug=True)
