import pandas as pd
from dash import dcc, html

df_time_limit = pd.DataFrame(columns=["TimeLimit"])
processed_df = pd.read_csv("merged_data.csv")
column_names = processed_df.columns.tolist()
column_names.remove('Index')



class GoalAndScreenTimeView:
    def get_html_component(self) -> html.Div:
        return self._build_html_component()

    def _build_html_component(self) -> html.Div:
        goal_time_input_container = self._build_goal_time_input_container()
        goal_app_input_container = self._build_goal_app_input_container()
        goal_tracking_graph_div = self._build_goal_graph_div()
        screen_time_monitor_help = self.build_screen_time_monitor_help()
        screen_time_monitor = self._build_screen_time_monitor()

        page = html.Div(
            id="goal-st-container",
            className="col-lg-6",
            children=[
                self._wrap_to_card(
                    "goal-container",
                    [
                        goal_time_input_container,
                        goal_app_input_container,
                        goal_tracking_graph_div,
                    ],
                ),
                html.Div(
                    id="stm-container",
                    children=[
                        html.Div(
                            id="stm-help-container", children=[screen_time_monitor_help]
                        ),
                        screen_time_monitor,
                    ],
                ),
            ],
        )

        return page

    def _build_goal_time_input_container(self) -> html.Div:
        div = html.Div(
            id="goal-time-input-container",
            # put item in flexbox and align the mvertically centered
            className="card-title d-flex align-items-center flex-wrap",
            children=[
                html.P(
                    id="goal-time-input-text-1",
                    className="text text-nowrap",
                    style={"margin-right": "1em", "margin-bottom": "0em"},
                    children="I want to reduce usage by :",
                ),
                dcc.Input(
                    id="goal-time-value-input",
                    className="d-inline-block",
                    value=5,
                    type="number",
                    style={
                        "width": "5em",
                        "margin-right": "0.4em",
                    },
                ),
                dcc.Dropdown(
                    id="goal-time-input-unit-dropdown",
                    className="d-inline-block",
                    options=[
                        {"label": "min(s)", "value": "min(s)"},
                        {"label": "hr(s)", "value": "hr(s)"},
                    ],
                    value="min(s)",
                    clearable=False,
                    searchable=False,
                    style={
                        "width": "6em",
                        "margin-right": "0.4em",
                    },
                ),
                html.P(
                    id="goal-time-input-text-granularity",
                    className="d-inline-block text-nowrap",
                    style={"margin-right": "0.4em", "margin-bottom": "0em"},
                    children="every day",
                ),
                html.P(
                    id="goal-time-input-text-2",
                    className="d-inline-block text-nowrap",
                    style={"margin-right": "0.4em", "margin-bottom": "0em"},
                    children="in a",
                ),
                dcc.Dropdown(
                    id="goal-time-input-granularity-dropdown",
                    className="d-inline-block",
                    options=[
                        {"label": "Week", "value": "Week"},
                        {"label": "Month", "value": "Month"},
                    ],
                    value="Week",
                    clearable=False,
                    searchable=False,
                    style={"width": "7em"},
                ),
            ],
        )

        return div

    def _build_goal_app_input_container(self) -> html.Div:
        div = html.Div(
            id="goal-app-input-container",
            className="d-flex align-items-center",
            style={"height": "5em"},
            children=[
                dcc.Dropdown(
                    id="goal-app-input-dropdown",
                    style={
                        "width": "20em",
                    },
                    options=self._get_list_of_apps(),
                    multi=False,
                    value="Total Usage",
                    clearable=False,
                    searchable=False,
                ),
            ],
        )

        return div

    def _build_goal_graph_div(self) -> html.Div:
        div = html.Div(id="goal-graph", children=[])

        return div

    def build_screen_time_monitor_help(self) -> html.Div:
        div = html.Div(
            id="stm-help",
            className="card",
            children=[
                html.Div(
                    className="card-body bg-dark",
                    children=[
                        html.H5(
                            id="stm-help-text-1",
                            className="card-title text-light",
                            children="Not sure how much time limit to set?",
                        ),
                        html.H6(
                            id="stm-help-text-2",
                            className="text-light",
                            children=["Try screen time monitoring below!"],
                        ),
                        html.Button(
                            id="info-button",
                            className="btn btn-primary  btn-sm",
                            children="Read more",
                        ),
                    ],
                ),
                html.Button(id="go-back-button", style={"display": "none"}),
            ],
        )

        return div

    def build_screen_time_monitor_explanation(self) -> html.Div:
        explanation = """The data visualization represents the maximum time limit a user
has set for their app usage and the actual duration of app usage
after the time limit has been set. The purpose of this visualization
is to determine the optimal duration for app usage limits, which
is the duration the users are mostly likely to adhere to. """

        div = html.Div(
            id="stm-exp",
            className="card",
            children=[
                html.Div(
                    className="card-body bg-dark",
                    children=[
                        html.P(
                            id="stm-exp-text",
                            className="text-light text-justify",
                            children=explanation,
                        ),
                        html.Button(
                            id="go-back-button",
                            className="btn btn-primary  btn-sm",
                            children="Go Back",
                        ),
                        html.Button(id="info-button", style={"display": "none"}),
                    ],
                )
            ],
        )

        return div

    def _build_screen_time_monitor(self) -> html.Div:
        div = self._wrap_to_card(
            "stm",
            [
                html.Div(
                    id="stm-time-limit",
                    className="card-title d-flex align-items-center flex-wrap",
                    children=[
                        html.P(
                            style={
                                "margin-right": "1em",
                                "margin-bottom": "0em",
                            },
                            children="Time Limit:",
                        ),
                        dcc.Input(
                            id="stm-input",
                            style={
                                "width": "5em",
                                "margin-right": "0.4",
                            },
                            type="number",
                            placeholder="",
                        ),
                        dcc.Dropdown(
                            id="stm-time-dropdown",
                            style={
                                "width": "6em",
                                "margin-right": "0.4",
                            },
                            options=[
                                {"label": "min(s)", "value": "min(s)"},
                                {"label": "hr(s)", "value": "hr(s)"},
                            ],
                            multi=False,
                            value="min(s)",
                            clearable=False,
                            searchable=False,
                        ),
                        html.Button(
                            id="add-value-button",
                            className="btn btn-primary btn-sm",
                            children="+",
                        ),
                    ],
                ),
                dcc.Dropdown(
                    id="stm-app-dropdown",
                    options=self._get_list_of_apps(),
                    value="Total Usage",
                    clearable=False,
                    searchable=False,
                ),
                html.Div(id="stm-output-container", children=[]),
            ],
        )

        return div

    def _get_list_of_apps(self) -> list:
        # TODO: Replace this with actual list of app from model class
        # return self.getModel().getListOfApps()
        return [
            {'label': col, 'value': col} for col in column_names                 
        ]

    def _wrap_to_card(self, id, divs) -> html.Div:
        return html.Div(
            id=id,
            className="card",
            children=[
                html.Div(
                    className="card-body",
                    children=divs,
                )
            ],
        )
