import dash
from dash import html, Input, Output
from header import Header, Page
from usagePage.enum import UsageTimeGranularity

from usagePage.usagePageModel import UsagePageModel
from usagePage.usagePageView import UsagePageView

app = dash.Dash(__name__)

HEADER = Header()
USAGE_PAGE_MODEL = UsagePageModel()
USAGE_PAGE_VIEW = UsagePageView()

USAGE_PAGE_MODEL.set_view(USAGE_PAGE_VIEW)
USAGE_PAGE_VIEW.set_model(USAGE_PAGE_MODEL)


header = HEADER.get_html_component()
current_page = USAGE_PAGE_VIEW.get_html_component()

app.layout = html.Div(
    children=[header, html.Div(id="page-container", children=[current_page])]
)


@app.callback(
    Output("stat-page-container", "children", allow_duplicate=True),
    Input("app-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_app(value):
    USAGE_PAGE_MODEL.set_current_app_name(value)
    return USAGE_PAGE_VIEW.get_html_component().children


@app.callback(
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


@app.callback(
    Output("page-container", "children", allow_duplicate=True),
    Input("page-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_page(value):
    if value == "Goal tracking":
        HEADER.set_current_page(Page.GOAL_TRACKING)
        # TODO: replace this with goal tracking page
        return html.Div("Goal tracking page", style={"background-color": "red"})
    else:
        HEADER.set_current_page(Page.USAGE_STAT)
        return USAGE_PAGE_VIEW.get_html_component()


if __name__ == "__main__":
    app.run_server(debug=True)
