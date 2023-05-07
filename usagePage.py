import dash
from dash import html, Input, Output
from usagePage.enum import UsageTimeGranularity

from usagePage.usagePageModel import UsagePageModel
from usagePage.usagePageView import UsagePageView

app = dash.Dash(__name__)

USAGE_PAGE_MODEL = UsagePageModel()
USAGE_PAGE_VIEW = UsagePageView()

USAGE_PAGE_MODEL.set_view(USAGE_PAGE_VIEW)
USAGE_PAGE_VIEW.set_model(USAGE_PAGE_MODEL)

app.layout = html.Div(
    children=[
        USAGE_PAGE_VIEW.get_html_component(),
    ]
)


@app.callback(
    Output("stat-page-container", "children", allow_duplicate=True),
    Input("app-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)
def update_app(value):
    USAGE_PAGE_MODEL.set_current_app_name(value)
    return USAGE_PAGE_VIEW.get_html_component().children

#@app.callback(
#    Output('graph', 'figure'),
#    Input('Granularity', 'value'))

@app.callback(
    Output("stat-page-container", "children", allow_duplicate=True),
    Input("time-granularity-dropdown", "value"),
    prevent_initial_call="initial_duplicate",
)

##def update_graph(Granularity):
 #   if ()

def update_time_granularity(value):
    if value == "week":
        USAGE_PAGE_MODEL.set_time_granularity(UsageTimeGranularity.WEEK)
    elif value == "month":
        USAGE_PAGE_MODEL.set_time_granularity(UsageTimeGranularity.MONTH)
    else:
        USAGE_PAGE_MODEL.set_time_granularity(UsageTimeGranularity.DAY)
    return USAGE_PAGE_VIEW.get_html_component().children


if __name__ == "__main__":
    app.run_server(debug=True)
