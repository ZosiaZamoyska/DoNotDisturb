import dash 
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd 
import numpy as np 

app = dash.Dash(__name__)


app.layout = html.Div(className='stm', children= [html.Div(id='goBackDiv_stm', children=[html.Button(id='goBackToGTP'),
                                                                                     html.Div(id='title_stm', children=[
                                                                                                html.H4("Screen Time Monitoring")
                                                  ]),]),

                                                  html.Div(children=[
    html.H4(id='stm_timeLimit', children=["Time Limit:",
                       dcc.Input(id="input_stm", type="number", placeholder=""),
                       dcc.Dropdown(
                        id = 'time_stm',
                        options = [
                            {'label': 'min(s)', 'value': 'min(s)'},
                            {'label': 'hr(s)', 'value': 'hr(s)'},
                        ],
                        multi = False,
                        value = 'min(s)',
                        clearable = False,
                        searchable = False,
                        style={
                               'width': '70px',
                                'border-radius': '15px', 
                                'background': 'linear-gradient(to bottom right, #D1D5FA 0%, #A9DFE2 100%)',
                                'font-size': '10px',
                                'font-weight': '600',
                                'font-family': 'Helvetica',
                           }
                      ),
    html.Button( id="add-value-button"),]),
    html.Div(id='output-container', children=[]),
   ])

])

@app.callback(
    Output("output-container", "children"),
    [Input("add-value-button", "n_clicks"),
     Input("time_stm", "value")],
    [State("input_stm", "value")]
)
def add_value_to_dataframe(n_clicks, time_stm, value):
    df_timeLimit = pd.read_csv("stm_data.csv")
    if value is None:
        df_timeLimit = pd.read_csv("stm_data.csv")
        fig = px.bar(df_timeLimit, y=['TimeLimit(mins)', 'RealUsage'], barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Time (mins)', xaxis_title=None)
        fig.update_layout(legend=dict(title=None,))
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace("RealUsage", "Real Usage")))
        return dcc.Graph(id='graph_stm', figure=fig)
    elif isinstance(value, int) or value.isnumeric():
        value = float(value)
    else:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["TIME IS NOT APPROPRIATE!"])])
    
    if value == 0:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["TIME SHOULD NOT BE 0!"])])

    if time_stm == 'hr(s)':
        value *= 60
    
    if n_clicks is not None and value is not None:
        df_timeLimit.loc[len(df_timeLimit), "TimeLimit(mins)"] = value
        df_timeLimit.to_csv("stm_data.csv", index=False)
        df_timeLimit = df_timeLimit.fillna(0)
        fig = px.bar(df_timeLimit, y=['TimeLimit(mins)', 'RealUsage'], barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Time (mins)', xaxis_title=None)
        fig.update_layout(legend=dict(title=None,))
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace("RealUsage", "Real Usage")))
        graph = dcc.Graph(id='graph_stm', figure=fig)
        
        return graph


if __name__ == '__main__':
    app.run_server(debug=True)
