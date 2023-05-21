import pandas as pd
from dash import dcc, html

df_time_limit = pd.DataFrame(columns=["TimeLimit"])


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
            children=[
                html.Div(
                    id="goal-container",
                    children=[
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
            children=[
                html.P(
                    id="goal-time-input-text-1", children=["I want to reduce usage by "]
                ),
                dcc.Input(id="goal-time-value-input", value=5, type="number"),
                dcc.Dropdown(
                    id="goal-time-input-unit-dropdown",
                    options=[
                        {"label": "min(s)", "value": "min(s)"},
                        {"label": "hr(s)", "value": "hr(s)"},
                    ],
                    value="min(s)",
                    clearable=False,
                    searchable=False,
                ),
                html.P(id="goal-time-input-text-granularity", children="every day"),
                html.P(id="goal-time-input-text-2", children="in a"),
                dcc.Dropdown(
                    id="goal-time-input-granularity-dropdown",
                    options=[
                        {"label": "Week", "value": "Week"},
                        {"label": "Month", "value": "Month"},
                    ],
                    value="Week",
                    clearable=False,
                    searchable=False,
                ),
            ],
        )

        return div

    def _build_goal_app_input_container(self) -> html.Div:
        div = html.Div(
            id="goal-app-input-container",
            children=[
                html.P(id="goal-app-input-text", children="Choose an app"),
                dcc.Dropdown(
                    id="goal-app-input-dropdown",
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
            children=[
                html.P(
                    id="stm-help-text-1",
                    children=["Not sure how much", html.Br(), "time limit to set?"],
                ),
                html.P(
                    id="stm-help-text-2",
                    children=["Try screen time monitoring"],
                ),
                html.Button(id="info-button"),
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
            children=[
                html.Button(id="go-back-button"),
                html.P(
                    id="stm-exp-text",
                    children=explanation,
                ),
                html.Button(id="info-button", style={"display": "none"}),
            ],
        )

        return div

    def _build_screen_time_monitor(self) -> html.Div:
        div = html.Div(
            id="stm",
            children=[
                html.Div(
                    id="stm-time-limit",
                    children=[
                        "Time Limit:",
                        dcc.Input(id="stm-input", type="number", placeholder=""),
                        dcc.Dropdown(
                            id="stm-time-dropdown",
                            options=[
                                {"label": "min(s)", "value": "min(s)"},
                                {"label": "hr(s)", "value": "hr(s)"},
                            ],
                            multi=False,
                            value="min(s)",
                            clearable=False,
                            searchable=False,
                        ),
                        html.Button(id="add-value-button"),
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
            {"label": "Total Usage", "value": "Total Usage"},
            {"label": "Instagram", "value": "Instagram"},
            {"label": "Facebook", "value": "Facebook"},
            {"label": "YouTube", "value": "YouTube"},
        ]
