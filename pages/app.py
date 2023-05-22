import dash
from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output, State
from goalAndScreenTime.goalAndScreenTimeView import GoalAndScreenTimeView

from header import Header
import numpy as np
import pandas as pd
import plotly.express as px
from usagePage.enum import UsageTimeGranularity
from usagePage.usagePageModel import UsagePageModel
from usagePage.usagePageView import UsagePageView

dash.register_page(__name__, path="/")

HEADER = Header()
header = HEADER.get_html_component()

###
# Usage Page
###

USAGE_PAGE_MODEL = UsagePageModel()
USAGE_PAGE_VIEW = UsagePageView()

USAGE_PAGE_MODEL.set_view(USAGE_PAGE_VIEW)
USAGE_PAGE_VIEW.set_model(USAGE_PAGE_MODEL)

GOAL_AND_SCREEN_TIME_VIEW = GoalAndScreenTimeView()

###
# Screen Time Monitoring Page
###
df = pd.read_csv("data2.csv")

### Code begin

# current_page = GOAL_AND_SCREEN_TIME_VIEW.get_html_component()

layout = html.Div(
    children=[
        # header,
        html.Div(
            className="body-wrapper",
            children=[
                html.Div(
                    className="container-fluid",
                    children=[
                        html.Div(
                            id="page-container",
                            className="row",
                            children=[
                                GOAL_AND_SCREEN_TIME_VIEW.get_html_component(),
                                USAGE_PAGE_VIEW.get_html_component(),
                            ],
                        )
                    ],
                )
            ],
        )
    ]
)


@callback(
    Output("stat-page-container", "children", allow_duplicate=True),
    Input("app-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_app(value):
    USAGE_PAGE_MODEL.set_current_app_name(value)
    return USAGE_PAGE_VIEW.get_html_component().children


@callback(
    Output("stat-page-container", "children", allow_duplicate=True),
    Input("time-granularity-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_time_granularity(value):
    if value == "week":
        USAGE_PAGE_MODEL.set_time_granularity(UsageTimeGranularity.WEEK)
    else:
        USAGE_PAGE_MODEL.set_time_granularity(UsageTimeGranularity.MONTH)
    return USAGE_PAGE_VIEW.get_html_component().children


@callback(
    Output("goal-graph", "children"),
    Output("goal-time-input-text-granularity", "children"),
    Input("goal-time-value-input", "value"),
    Input("goal-time-input-unit-dropdown", "value"),
    Input("goal-time-input-granularity-dropdown", "value"),
    Input("goal-app-input-dropdown", "value"),
)
def update(timeInput, time, granularity, app):
    granularity_Text = "every day"
    if granularity == "Month":
        granularity_Text = "every week"

    if timeInput is None:
        return (
            html.Div(
                id="errorDiv",
                children=[
                    html.Img(
                        id="errorImg",
                        className="img-fluid",
                        src="https://img.freepik.com/premium-vector/hourglass-icon-comic-style-sandglass-cartoon-vector-illustration-white-isolated-background-clock-splash-effect-business-concept_157943-6412.jpg?w=2000",
                    ),
                    html.H1(id="errorText", children=["WAITING..."]),
                ],
            ),
            granularity_Text,
        )
    elif isinstance(timeInput, int) or timeInput.isnumeric():
        timeInput = float(timeInput)
    else:
        return (
            html.Div(
                id="errorDiv",
                children=[
                    html.Img(
                        id="errorImg",
                        className="img-fluid",
                        src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                    ),
                    html.H1(id="errorText", children=["TIME IS NOT APPROPRIATE!"]),
                ],
            ),
            granularity_Text,
        )

    if timeInput == 0:
        return (
            html.Div(
                id="errorDiv",
                children=[
                    html.Img(
                        id="errorImg",
                        className="img-fluid",
                        src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                    ),
                    html.H1(id="errorText", children=["TIME SHOULD NOT BE 0!"]),
                ],
            ),
            granularity_Text,
        )

    if time == "hr(s)":
        timeInput = timeInput * 60
    if granularity == "Week":
        df_graph = df[["Index", app]]
        df_graph[app] = df_graph[app].fillna(0)
        df_graph = pd.concat(
            [
                df_graph,
                pd.DataFrame(
                    {
                        "Index": [
                            "Goal1",
                            "Goal2",
                            "Goal3",
                            "Goal4",
                            "Goal5",
                            "Goal6",
                            "Goal7",
                        ],
                        app: [
                            df.loc[df["Index"] == "Day1", app].values[0],
                            df.loc[df["Index"] == "Day1", app].values[0] - timeInput,
                            df.loc[df["Index"] == "Day1", app].values[0]
                            - 2 * timeInput,
                            df.loc[df["Index"] == "Day1", app].values[0]
                            - 3 * timeInput,
                            df.loc[df["Index"] == "Day1", app].values[0]
                            - 4 * timeInput,
                            df.loc[df["Index"] == "Day1", app].values[0]
                            - 5 * timeInput,
                            df.loc[df["Index"] == "Day1", app].values[0]
                            - 6 * timeInput,
                        ],
                    }
                ),
            ],
            ignore_index=True,
        )
        if (df_graph[app] < 0).any().any():
            return (
                html.Div(
                    id="errorDiv",
                    children=[
                        html.Img(
                            id="errorImg",
                            className="img-fluid",
                            src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                        ),
                        html.H1(id="errorText", children=["GOAL SET TOO LARGE"]),
                    ],
                ),
                granularity_Text,
            )
        df_days = df_graph.loc[
            (df_graph["Index"] >= "Day1") & (df_graph["Index"] <= "Day7")
        ]
        df_goals = df_graph.loc[
            (df_graph["Index"] >= "Goal1") & (df_graph["Index"] <= "Goal7")
        ].reset_index(drop=True)
        df_days.loc[:, "Goal"] = df_goals[app]
        df_days["Rating"] = np.where(
            df_days[app] <= df_days["Goal"],
            "Good",
            np.where(df_days[app] <= 1.1 * df_days["Goal"], "Ok", "Bad"),
        )
        if df_days[app].min() > 60 or df_days["Goal"].min() > 60:
            df_days[app] = df_days[app] / 60
            df_days["Goal"] = df_days["Goal"] / 60
            timeInput = timeInput / 60
        color_map = {"Good": "#65C089", "Ok": "#FBD167", "Bad": "#E16060"}
        fig = px.bar(
            df_days,
            x="Index",
            y=app,
            color="Rating",
            color_discrete_map=color_map,
            category_orders={
                "Index": ["Day1", "Day2", "Day3", "Day4", "Day5", "Day6", "Day7"],
                "Rating": ["Good", "Ok", "Bad"],
            },
        )
        fig.add_scatter(
            x=df_days["Index"],
            y=df_days["Goal"],
            mode="markers",
            marker=dict(color="black", size=15, symbol="line-ew-open"),
            name="Goal",
        )
        fig.add_annotation(
            x="Day1",
            y=df_days.loc[df_days["Index"] == "Day1", app].iloc[0],
            text="You start here",
            showarrow=True,
            font=dict(size=8, color="black"),
        )
        min_val = df_days.loc[df_days[app] > 0, app].min()
        min_y_axis = min(min_val, df_days["Goal"].min()) - timeInput
        if min_y_axis < 0:
            min_y_axis = 0
        fig.update_yaxes(
            range=[
                min_y_axis,
                max(df_days[app].max(), df_days["Goal"].max()) + timeInput,
            ]
        )
        fig.update_layout(height=403)
        fig.update_layout(yaxis_title="Usage", xaxis_title=None)
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_layout(legend=dict(title=""))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        graph = dcc.Graph(id="graph", figure=fig)
    elif granularity == "Month":
        df_graph = df[["Index", app]]
        df_graph[app] = df_graph[app].fillna(0)
        df_graph = pd.concat(
            [
                df_graph,
                pd.DataFrame(
                    {
                        "Index": ["Goal1", "Goal2", "Goal3", "Goal4"],
                        app: [
                            df.loc[df["Index"] == "Week1", app].values[0],
                            df.loc[df["Index"] == "Week1", app].values[0] - timeInput,
                            df.loc[df["Index"] == "Week1", app].values[0]
                            - 2 * timeInput,
                            df.loc[df["Index"] == "Week1", app].values[0]
                            - 3 * timeInput,
                        ],
                    }
                ),
            ],
            ignore_index=True,
        )
        if (df_graph[app] < 0).any().any():
            return (
                html.Div(
                    id="errorDiv",
                    children=[
                        html.Img(
                            id="errorImg",
                            className="img-fluid",
                            src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                        ),
                        html.H1(id="errorText", children=["GOAL SET TOO LARGE"]),
                    ],
                ),
                granularity_Text,
            )
        df_weeks = df_graph.loc[
            (df_graph["Index"] >= "Week1") & (df_graph["Index"] <= "Week4")
        ].reset_index(drop=True)
        df_goals = df_graph.loc[
            (df_graph["Index"] >= "Goal1") & (df_graph["Index"] <= "Goal4")
        ].reset_index(drop=True)
        df_weeks.loc[:, "Goal"] = df_goals[app]
        df_weeks["Rating"] = np.where(
            df_weeks[app] <= df_weeks["Goal"],
            "Good",
            np.where(df_weeks[app] <= 1.1 * df_weeks["Goal"], "Ok", "Bad"),
        )
        if df_weeks[app].min() > 60 or df_weeks["Goal"].min() > 60:
            df_weeks[app] = df_weeks[app] / 60
            df_weeks["Goal"] = df_weeks["Goal"] / 60
            timeInput = timeInput / 60
        color_map = {"Good": "#65C089", "Ok": "#FBD167", "Bad": "#E16060"}
        fig = px.bar(
            df_weeks,
            x="Index",
            y=app,
            color="Rating",
            color_discrete_map=color_map,
            category_orders={
                "Index": ["Week1", "Week2", "Week3", "Week4"],
                "Rating": ["Good", "Ok", "Bad"],
            },
        )
        fig.add_scatter(
            x=df_weeks["Index"],
            y=df_weeks["Goal"],
            mode="markers",
            marker=dict(color="black", size=30, symbol="line-ew-open"),
            name="Goal",
        )
        fig.add_annotation(
            x="Week1",
            y=df_weeks.loc[df_weeks["Index"] == "Week1", app].iloc[0],
            text="You start here",
            showarrow=True,
            font=dict(size=8, color="black"),
        )
        min_val = df_weeks.loc[df_weeks[app] > 0, app].min()
        min_y_axis = min(min_val, df_weeks["Goal"].min()) - timeInput
        if min_y_axis < 0:
            min_y_axis = 0
        fig.update_yaxes(
            range=[
                min_y_axis,
                max(df_weeks[app].max(), df_weeks["Goal"].max()) + timeInput,
            ]
        )
        fig.update_layout(height=403)
        fig.update_layout(yaxis_title="Usage", xaxis_title=None)
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_layout(legend=dict(title=""))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        graph = dcc.Graph(id="graph", figure=fig)
    return graph, granularity_Text


@callback(
    Output("stm-help-container", "children"),
    Input("info-button", "n_clicks"),
    Input("go-back-button", "n_clicks"),
)
def display_page(info_clicks, back_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return GOAL_AND_SCREEN_TIME_VIEW.build_screen_time_monitor_help()
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "info-button":
            return GOAL_AND_SCREEN_TIME_VIEW.build_screen_time_monitor_explanation()
        elif button_id == "go-back-button":
            return GOAL_AND_SCREEN_TIME_VIEW.build_screen_time_monitor_help()


@callback(
    Output("stm-output-container", "children"),
    [
        Input("add-value-button", "n_clicks"),
        Input("stm-time-dropdown", "value"),
        Input("stm-app-dropdown", "value"),
    ],
    [State("stm-input", "value")],
)
def add_value_to_dataframe(n_clicks, time_stm, app, value):
    prev_clicks = (
        add_value_to_dataframe.prev_clicks
        if hasattr(add_value_to_dataframe, "prev_clicks")
        else 0
    )
    df_timeLimit_ori = pd.read_csv("stm_data.csv")
    df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
    if value is None:
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        if df_timeLimit.empty:
            return html.Div(
                id="errorDiv",
                children=[
                    html.Img(
                        id="errorImg",
                        className="img-fluid",
                        src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                    ),
                    html.H1(id="errorText", children=["NOTHING YET"]),
                ],
            )
        df_timeLimit["x_values"] = range(1, len(df_timeLimit) + 1)
        fig = px.bar(
            df_timeLimit,
            x="x_values",
            y=["TimeLimit(mins)", "RealUsage"],
            barmode="group",
            color_discrete_sequence=["#636EFA", "#EF553B"],
        )
        fig.update_layout(height=403)
        fig.update_layout(yaxis_title="Time (mins)", xaxis_title="Trial")
        fig.update_layout(
            legend=dict(
                title=None,
            )
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        fig.for_each_trace(
            lambda trace: trace.update(
                name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace(
                    "RealUsage", "Real Usage"
                )
            )
        )
        return dcc.Graph(id="graph_stm", figure=fig)
    elif isinstance(value, int) or value.isnumeric():
        value = float(value)
    if value == 0:
        return html.Div(
            id="errorDiv",
            children=[
                html.Img(
                    id="errorImg",
                    className="img-fluid",
                    src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                ),
                html.H1(id="errorText", children=["TIME SHOULD NOT BE 0!"]),
            ],
        )

    if n_clicks != prev_clicks and value is not None:
        if time_stm == "hr(s)":
            value *= 60
        add_value_to_dataframe.prev_clicks = n_clicks
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        new_row = pd.DataFrame({"App": [app], "TimeLimit(mins)": [value]})
        df_timeLimit = pd.concat([df_timeLimit, new_row], ignore_index=True)
        df_timeLimit_ori.loc[len(df_timeLimit_ori), ["App", "TimeLimit(mins)"]] = [
            app,
            value,
        ]
        df_timeLimit_ori.to_csv("stm_data.csv", index=False)
        df_timeLimit = df_timeLimit.fillna(0)
        df_timeLimit_ori = df_timeLimit_ori.fillna(0)
        df_timeLimit["x_values"] = range(1, len(df_timeLimit) + 1)
        fig = px.bar(
            df_timeLimit,
            x="x_values",
            y=["TimeLimit(mins)", "RealUsage"],
            barmode="group",
            color_discrete_sequence=["#636EFA", "#EF553B"],
        )
        fig.update_layout(height=403)
        fig.update_layout(yaxis_title="Time (mins)", xaxis_title="Trial")
        fig.update_layout(
            legend=dict(
                title=None,
            )
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        fig.for_each_trace(
            lambda trace: trace.update(
                name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace(
                    "RealUsage", "Real Usage"
                )
            )
        )
        graph = dcc.Graph(id="graph_stm", figure=fig)
        return graph
    elif n_clicks == prev_clicks:
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        if df_timeLimit.empty:
            return html.Div(
                id="errorDiv",
                children=[
                    html.Img(
                        id="errorImg",
                        className="img-fluid",
                        src="https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000",
                    ),
                    html.H1(id="errorText", children=["NOTHING YET"]),
                ],
            )
        df_timeLimit["x_values"] = range(1, len(df_timeLimit) + 1)
        fig = px.bar(
            df_timeLimit,
            x="x_values",
            y=["TimeLimit(mins)", "RealUsage"],
            barmode="group",
            color_discrete_sequence=["#636EFA", "#EF553B"],
        )
        fig.update_layout(height=403)
        fig.update_layout(yaxis_title="Time (mins)", xaxis_title="Trial")
        fig.update_layout(
            legend=dict(
                title=None,
            )
        )
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white")
        fig.for_each_trace(
            lambda trace: trace.update(
                name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace(
                    "RealUsage", "Real Usage"
                )
            )
        )
        return dcc.Graph(id="graph_stm", figure=fig)
