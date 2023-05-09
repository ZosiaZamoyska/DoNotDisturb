from enum import Enum
from dash import dcc, html


class Page(Enum):
    GOAL_TRACKING = "Goal tracking"
    USAGE_STAT = "Usage statistics"


class Header:
    def __init__(self):
        self._current_page = Page.GOAL_TRACKING
        self._html_component = self._build_html_component()

    def get_current_page(self):
        return self._current_page

    def set_current_page(self, page):
        self._current_page = page

    def get_html_component(self):
        return self._html_component

    def _build_html_component(self):
        controller_widget = self._build_controller()

        header = html.Div(
            id="header",
            children=[controller_widget],
        )

        return header

    def _build_controller(self):
        div = html.Div(
            id="header-controller",
            children=[
                dcc.Dropdown(
                    id="page-dropdown",
                    options=[Page.GOAL_TRACKING.value, Page.USAGE_STAT.value],
                    value=self.get_current_page().value,
                )
            ],
        )

        return div
