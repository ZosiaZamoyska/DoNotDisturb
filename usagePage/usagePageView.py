from dash import html, dcc
from usagePage.data import UsageData
from usagePage.emotion import to_emoji
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import matplotlib

class UsagePageView:
    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model
        self._html_component = self._build_html_component()

    def get_html_component(self) -> html.Div:
        return self._html_component

    def _build_html_component(self) -> html.Div:
        controller_widget = self._build_controller()

        review = self._build_review_widget()
        notification_widget = self._build_notification_widget()
        pickup_widget = self._build_pickup_widget()
        unlock_widget = self._build_unlock_widget()
        emotion_emojis_widget = self._build_emotion_emojis_widget()

        usage_stat_container = html.Div(
            id="stat-container",
            children=[
                review,
                notification_widget,
                pickup_widget,
                unlock_widget,
                emotion_emojis_widget,
            ],
        )

        page = html.Div(
            id="stat-page-container",
            children=[controller_widget, usage_stat_container],
        )

        return page

    def _build_controller(self):
        div = html.Div(
            id="controller-container",
            children=[
                html.H1("Usage Statistics", className="controller-title"),
                dcc.Dropdown(
                    id="app-dropdown",
                    options=UsageData.get_all_app_names(),
                    value=self.get_model().get_current_app_name(),
                ),
                dcc.Dropdown(
                    id="time-granularity-dropdown",
                    options=["week", "month"],
                    value=self.get_model().get_time_granularity().value,
                ),
            ],
        )

        return div

    def _build_review_widget(self):
        day = ["monday"]*7 + ["tuesday"]*7 + ["wednesday"]*7 + ["thursday"]*7 + ["friday"] *7 + ["saturday"]*7 + ["sunday"]*7
        time = [[6, 2, 2, 3, 4, 3, 4], [2, 6, 2, 3, 4, 5, 2], [6, 1, 2, 4, 4, 2, 5], [8, 2, 3, 2, 1, 4, 4], [7, 3, 1, 2, 4, 5, 2], [9, 2, 2, 4, 3, 4], [6, 2, 2, 3, 4, 3, 4]]
        #colors = ['r', 'g', 'b', 'g', 'b', 'g', 'r']
        colors = [[0, 2, 3, 1, 3, 1, 0], [1, 0, 3, 0, 3, 2, 1], [0, 2, 3, 1, 3, 2, 1], [0, 3, 2, 1, 2, 3, 1], [0, 2, 1, 2, 3, 2, 0], [0, 2, 3, 2, 3, 1], [0, 2, 1, 2, 3, 2, 1]]
        df = pd.DataFrame(list(zip(day, time, colors)), columns =['day', 'time', 'colors'])
        #fig = px.bar(df, x=time, y=day, color=colors, width=1000, height=300)
        z = [[], [], [], [], [], [], []]
        color_map = matplotlib.cm.get_cmap('Paired_r', 10)
        color_scale = [[0, '#D9D9D9'], [0.33, '#E16060'], [0.66, "#FBD167"], [1, "#65C089"]]
        #print(z)
        for days in range(7):
            for i in range(len(colors[days])):
                for j in range(time[days][i]):
                    z[days].append(colors[days][i])
        #print(z)


        fig = px.imshow(z, text_auto=False, color_continuous_scale=color_scale)
        fig.layout.coloraxis.showscale = False
        #fig.update_layout(width=1000, height=200)

        #fig.update_layout(xaxis_range=[0,24])
        return dcc.Graph(id='graph', figure=fig)

    def _build_notification_widget(self):
        try:
            notification_percent = int(
                self.get_model().get_notification_count()
                * 100
                / self.get_model().get_all_notification_count()
            )

            widget = self._build_usage_widget(
                "notification-widget",
                f"notified you",
                f"{self.get_model().get_notification_count()} times",
                f"That is {notification_percent}% of all notifications.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_pickup_widget(self):
        try:
            pickup_percent = int(
                self.get_model().get_pickup_count()
                * 100
                / self.get_model().get_notification_count()
            )

            widget = self._build_usage_widget(
                "pickup-widget",
                f"made you pick up the phone",
                f"{self.get_model().get_pickup_count()} times",
                f"That is {pickup_percent}% of the time it has notified you.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_unlock_widget(self):
        try:
            unlock_percent = int(
                self.get_model().get_unlock_count()
                * 100
                / self.get_model().get_pickup_count()
            )

            widget = self._build_usage_widget(
                "unlock-widget",
                f"made you unlock the phone",
                f"{self.get_model().get_unlock_count()} times",
                f"That is {unlock_percent}% of the time it has made you pick up the phone.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_usage_widget(
        self, id: str, title: str, number_times_occured: int, description: str
    ) -> html.Div:
        div = html.Div(
            id=id,
            className="usage-widget",
            children=[
                html.P(title, className="usage-widget-title"),
                html.P(number_times_occured, className="usage-widget-number"),
                html.P(description, className="usage-widget-desc"),
            ],
        )
        return div

    def _build_no_data_usage_widget(self) -> html.Div:
        div = html.Div(
            className="no-data-usage-widget",
            children=[html.H2("Something went wrong")],
        )
        return div

    def _build_emotion_emojis_widget(self) -> html.Div:
        div = html.Div(
            id="emotion-emojis-widget",
            children=[
                html.P(
                    f"While you are using {self.get_model().get_current_app_name()}, you felt..."
                ),
                html.Div(
                    id="emojis-container",
                    children=list(
                        map(
                            lambda e: html.Div(
                                className="emoji-container",
                                children=[
                                    html.P(className="emoji", children=to_emoji(e)),
                                    html.P(className="emotion", children=e.value),
                                ],
                            ),
                            self.get_model().get_emotions(),
                        )
                    ),
                ),
            ],
        )
        return div

    def update(self):
        self._html_component = self._build_html_component()
