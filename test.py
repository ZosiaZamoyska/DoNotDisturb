import dash
from dash import html

from usagePage.usagePageModel import UsagePageModel
from usagePage.usagePageView import UsagePageView

app = dash.Dash(__name__)

USAGE_PAGE_MODEL = UsagePageModel()
USAGE_PAGE_VIEW = UsagePageView()

USAGE_PAGE_MODEL.set_view(USAGE_PAGE_VIEW)
USAGE_PAGE_VIEW.set_model(USAGE_PAGE_MODEL)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dash"),
        USAGE_PAGE_VIEW.get_html_component(),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
