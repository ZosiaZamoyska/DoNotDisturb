import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from datetime import datetime
import plotly.express as px
import pandas as pd
import os

dash.register_page(__name__, path="/schedule")

layout = html.Div(
    className="row",
    children=html.Div(
        id="Schedule-Input",
        className="card",
        children=[
            html.Div(
                className="card-body",
                children=[
                    html.H1(
                        id="titleText",
                        className="card-title",
                        children=["Schedule Input"],
                    ),
                    html.Div(
                        id="DateScheduleInput",
                        children=[
                            html.H6(children="Date:  ", style={"margin-bottom": "0em"}),
                            dcc.DatePickerSingle(
                                id="my-date-picker-single",
                                date=datetime.now().date(),
                            ),
                        ],
                        style={"margin-bottom": "1em"},
                    ),
                    html.H6(children=["Choose a category:"]),
                    dcc.RadioItems(
                        id="scheduleCategory",
                        options=["Sleep", "Work", "Leisure"],
                        value="Sleep",
                        inline=True,
                        style={"margin-bottom": "1em"},
                    ),
                    html.Div(
                        id="TimeScheduleInput",
                        children=[
                            html.P("From", style={"margin-bottom": "0em"}),
                            dcc.Dropdown(
                                id="fromHour",
                                options=[
                                    {"label": "00", "value": "00"},
                                    {"label": "01", "value": "01"},
                                    {"label": "02", "value": "02"},
                                    {"label": "03", "value": "03"},
                                    {"label": "04", "value": "04"},
                                    {"label": "05", "value": "05"},
                                    {"label": "06", "value": "06"},
                                    {"label": "07", "value": "07"},
                                    {"label": "08", "value": "08"},
                                    {"label": "09", "value": "09"},
                                    {"label": "10", "value": "10"},
                                    {"label": "11", "value": "11"},
                                    {"label": "12", "value": "12"},
                                    {"label": "13", "value": "13"},
                                    {"label": "14", "value": "14"},
                                    {"label": "15", "value": "15"},
                                    {"label": "16", "value": "16"},
                                    {"label": "17", "value": "17"},
                                    {"label": "18", "value": "18"},
                                    {"label": "19", "value": "19"},
                                    {"label": "20", "value": "20"},
                                    {"label": "21", "value": "21"},
                                    {"label": "22", "value": "22"},
                                    {"label": "23", "value": "23"},
                                ],
                                clearable=False,
                                value="00",
                            ),
                            html.P(":", style={"margin-bottom": "0em"}),
                            dcc.Dropdown(
                                id="fromMins",
                                options=[
                                    {"label": "00", "value": "00"},
                                    {"label": "01", "value": "01"},
                                    {"label": "02", "value": "02"},
                                    {"label": "03", "value": "03"},
                                    {"label": "04", "value": "04"},
                                    {"label": "05", "value": "05"},
                                    {"label": "06", "value": "06"},
                                    {"label": "07", "value": "07"},
                                    {"label": "08", "value": "08"},
                                    {"label": "09", "value": "09"},
                                    {"label": "10", "value": "10"},
                                    {"label": "11", "value": "11"},
                                    {"label": "12", "value": "12"},
                                    {"label": "13", "value": "13"},
                                    {"label": "14", "value": "14"},
                                    {"label": "15", "value": "15"},
                                    {"label": "16", "value": "16"},
                                    {"label": "17", "value": "17"},
                                    {"label": "18", "value": "18"},
                                    {"label": "19", "value": "19"},
                                    {"label": "20", "value": "20"},
                                    {"label": "21", "value": "21"},
                                    {"label": "22", "value": "22"},
                                    {"label": "23", "value": "23"},
                                    {"label": "24", "value": "24"},
                                    {"label": "25", "value": "25"},
                                    {"label": "26", "value": "26"},
                                    {"label": "27", "value": "27"},
                                    {"label": "28", "value": "28"},
                                    {"label": "29", "value": "29"},
                                    {"label": "30", "value": "30"},
                                    {"label": "31", "value": "31"},
                                    {"label": "32", "value": "32"},
                                    {"label": "33", "value": "33"},
                                    {"label": "34", "value": "34"},
                                    {"label": "35", "value": "35"},
                                    {"label": "36", "value": "36"},
                                    {"label": "37", "value": "37"},
                                    {"label": "38", "value": "38"},
                                    {"label": "39", "value": "39"},
                                    {"label": "40", "value": "40"},
                                    {"label": "41", "value": "41"},
                                    {"label": "42", "value": "42"},
                                    {"label": "43", "value": "43"},
                                    {"label": "44", "value": "44"},
                                    {"label": "45", "value": "45"},
                                    {"label": "46", "value": "46"},
                                    {"label": "47", "value": "47"},
                                    {"label": "48", "value": "48"},
                                    {"label": "49", "value": "49"},
                                    {"label": "50", "value": "50"},
                                    {"label": "51", "value": "51"},
                                    {"label": "52", "value": "52"},
                                    {"label": "53", "value": "53"},
                                    {"label": "54", "value": "54"},
                                    {"label": "55", "value": "55"},
                                    {"label": "56", "value": "56"},
                                    {"label": "57", "value": "57"},
                                    {"label": "58", "value": "58"},
                                    {"label": "59", "value": "59"},
                                ],
                                clearable=False,
                                value="00",
                            ),
                            html.P("to", style={"margin-bottom": "0em"}),
                            dcc.Dropdown(
                                id="toHour",
                                options=[
                                    {"label": "00", "value": "00"},
                                    {"label": "01", "value": "01"},
                                    {"label": "02", "value": "02"},
                                    {"label": "03", "value": "03"},
                                    {"label": "04", "value": "04"},
                                    {"label": "05", "value": "05"},
                                    {"label": "06", "value": "06"},
                                    {"label": "07", "value": "07"},
                                    {"label": "08", "value": "08"},
                                    {"label": "09", "value": "09"},
                                    {"label": "10", "value": "10"},
                                    {"label": "11", "value": "11"},
                                    {"label": "12", "value": "12"},
                                    {"label": "13", "value": "13"},
                                    {"label": "14", "value": "14"},
                                    {"label": "15", "value": "15"},
                                    {"label": "16", "value": "16"},
                                    {"label": "17", "value": "17"},
                                    {"label": "18", "value": "18"},
                                    {"label": "19", "value": "19"},
                                    {"label": "20", "value": "20"},
                                    {"label": "21", "value": "21"},
                                    {"label": "22", "value": "22"},
                                    {"label": "23", "value": "23"},
                                ],
                                clearable=False,
                                value="00",
                            ),
                            html.P(":", style={"margin-bottom": "0em"}),
                            dcc.Dropdown(
                                id="toMins",
                                options=[
                                    {"label": "00", "value": "00"},
                                    {"label": "01", "value": "01"},
                                    {"label": "02", "value": "02"},
                                    {"label": "03", "value": "03"},
                                    {"label": "04", "value": "04"},
                                    {"label": "05", "value": "05"},
                                    {"label": "06", "value": "06"},
                                    {"label": "07", "value": "07"},
                                    {"label": "08", "value": "08"},
                                    {"label": "09", "value": "09"},
                                    {"label": "10", "value": "10"},
                                    {"label": "11", "value": "11"},
                                    {"label": "12", "value": "12"},
                                    {"label": "13", "value": "13"},
                                    {"label": "14", "value": "14"},
                                    {"label": "15", "value": "15"},
                                    {"label": "16", "value": "16"},
                                    {"label": "17", "value": "17"},
                                    {"label": "18", "value": "18"},
                                    {"label": "19", "value": "19"},
                                    {"label": "20", "value": "20"},
                                    {"label": "21", "value": "21"},
                                    {"label": "22", "value": "22"},
                                    {"label": "23", "value": "23"},
                                    {"label": "24", "value": "24"},
                                    {"label": "25", "value": "25"},
                                    {"label": "26", "value": "26"},
                                    {"label": "27", "value": "27"},
                                    {"label": "28", "value": "28"},
                                    {"label": "29", "value": "29"},
                                    {"label": "30", "value": "30"},
                                    {"label": "31", "value": "31"},
                                    {"label": "32", "value": "32"},
                                    {"label": "33", "value": "33"},
                                    {"label": "34", "value": "34"},
                                    {"label": "35", "value": "35"},
                                    {"label": "36", "value": "36"},
                                    {"label": "37", "value": "37"},
                                    {"label": "38", "value": "38"},
                                    {"label": "39", "value": "39"},
                                    {"label": "40", "value": "40"},
                                    {"label": "41", "value": "41"},
                                    {"label": "42", "value": "42"},
                                    {"label": "43", "value": "43"},
                                    {"label": "44", "value": "44"},
                                    {"label": "45", "value": "45"},
                                    {"label": "46", "value": "46"},
                                    {"label": "47", "value": "47"},
                                    {"label": "48", "value": "48"},
                                    {"label": "49", "value": "49"},
                                    {"label": "50", "value": "50"},
                                    {"label": "51", "value": "51"},
                                    {"label": "52", "value": "52"},
                                    {"label": "53", "value": "53"},
                                    {"label": "54", "value": "54"},
                                    {"label": "55", "value": "55"},
                                    {"label": "56", "value": "56"},
                                    {"label": "57", "value": "57"},
                                    {"label": "58", "value": "58"},
                                    {"label": "59", "value": "59"},
                                ],
                                clearable=False,
                                value="00",
                            ),
                        ],
                        style={"margin-bottom": "1em"},
                    ),
                    html.Div(
                        html.Button(
                            "Submit",
                            id="submit-schedule",
                            className="btn btn-primary",
                            n_clicks=0,
                            style={"margin-bottom": "1em"},
                        )
                    ),
                    html.Div(
                        html.P(
                            children=[
                                "Note: This schedule is used to rate your phone usage in day-in-review and week-in-review"
                            ]
                        )
                    ),
                    html.Div(id="return", children=[]),
                ],
            ),
        ],
    ),
)


@callback(
    Output("return", "children"),
    [Input("submit-schedule", "n_clicks")],
    [
        dash.dependencies.State("my-date-picker-single", "date"),
        dash.dependencies.State("scheduleCategory", "value"),
        dash.dependencies.State("fromHour", "value"),
        dash.dependencies.State("fromMins", "value"),
        dash.dependencies.State("toHour", "value"),
        dash.dependencies.State("toMins", "value"),
    ],
)
def save_schedule(n_clicks, date, category, from_hour, from_min, to_hour, to_min):
    from_hour = int(from_hour)
    from_min = int(from_min)
    to_hour = int(to_hour)
    to_min = int(to_min)
    if n_clicks > 0:
        data = {
            "Date": [date],
            "Category": [category],
            "From Hour": [from_hour],
            "From Min": [from_min],
            "To Hour": [to_hour],
            "To Min": [to_min],
        }
        df_new = pd.DataFrame(data)

        # Check if the schedule.csv file exists
        if os.path.isfile("schedule.csv"):
            df_existing = pd.read_csv("schedule.csv")

            # Find rows with matching values for Date, From Hour, From Min, To Hour, and To Min
            matching_rows = df_existing[
                (df_existing["Date"] == date)
                & (df_existing["From Hour"] == from_hour)
                & (df_existing["From Min"] == from_min)
                & (df_existing["To Hour"] == to_hour)
                & (df_existing["To Min"] == to_min)
            ]

            # Update the existing row if a match is found, otherwise append the new data
            if not matching_rows.empty:
                matching_indices = matching_rows.index

                # Update the values using the matching indices
                df_existing.loc[matching_indices] = df_new.values
            else:
                df_new = pd.concat([df_existing, df_new], ignore_index=True)

        df_new.to_csv("schedule.csv", index=False)
    return html.Div()
