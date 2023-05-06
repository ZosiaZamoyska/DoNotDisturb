from dash import html
from usagePage.util import capitalize


class UsagePageView:
    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model
        self._html_component = self._build_html_component()

    def get_html_component(self) -> html.Div:
        return self._html_component

    def _build_html_component(self) -> html.Div:
        notification_widget = self._build_notification_widget()
        pickup_widget = self._build_pickup_widget()
        unlock_widget = self._build_unlock_widget()

        usage_stat_container = html.Div(
            id="stat-container",
            children=[notification_widget, pickup_widget, unlock_widget],
        )

        emotion_emojis_widget = self._build_emotion_emojis_widget()

        page = html.Div(
            id="stat-page-container",
            children=[usage_stat_container, emotion_emojis_widget],
        )

        return page

    def _build_notification_widget(self):
        try:
            notification_percent = int(
                self.get_model().get_notification_count()
                * 100
                / self.get_model().get_all_notification_count()
            )

            widget = self._build_usage_widget(
                "notification-widget",
                f"{capitalize(self.get_time_granularity())}, {self.get_current_app_name()} has notified you",
                self.get_model().get_notification_count(),
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
                f"{capitalize(self.get_time_granularity())}, {self.get_current_app_name()} has made you pick up the phone",
                self.get_model().get_pickup_count(),
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
                f"{capitalize(self.get_time_granularity())}, {self.get_current_app_name()} has made you unlock the phone",
                self.get_model().get_unlock_count(),
                f"That is {unlock_percent}% of the time it has made you pick up the phone.",
            )

            return widget
        except Exception:
            return self._build_no_data_usage_widget()

    def _build_usage_widget(
        id: str, title: str, number_times_occured: int, description: str
    ) -> html.Div:
        div = html.Div(
            id=id,
            children=[
                html.H2(title),
                html.H3(number_times_occured),
                html.P(description),
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
            [
                html.H2(
                    f"You feel these emotions while using {self.get_model().get_current_app_name()}"
                ),
                html.Div(
                    id="emoji-widget",
                    children=list(
                        map(lambda e: html.P(e), self.get_model().get_emotion_emojis())
                    ),
                ),
            ]
        )
        return div

    def update(self):
        self._html_component = self._build_html_component()
