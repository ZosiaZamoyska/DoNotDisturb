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
    html.Div(id='chooseApp_stm', children=[
                    dcc.Dropdown(
                        id = 'App_stm',
                        options = [
                            {'label': 'Total Usage', 'value': 'Total Usage'},
                            {'label': 'Instagram', 'value': 'Instagram'},
                            {'label': 'Facebook', 'value': 'Facebook'},
                            {'label': 'YouTube', 'value': 'YouTube'}
                        ],
                        multi = False,
                        value = 'Total Usage',
                        clearable = False,
                        searchable = False,
                        style={
                               'width': '200px',
                               'border-radius': '15px', 
                               'background': 'linear-gradient(to bottom right, #D1D5FA 0%, #A9DFE2 100%)',
                               'font-size': '10px',
                               'font-weight': '600',
                               'font-family': 'Helvetica',
                           }
                      )
                ]),
    html.Div(id='output-container', children=[]),
   ])

])

@app.callback(
    Output("output-container", "children"),
    [Input("add-value-button", "n_clicks"),
     Input("time_stm", "value"),
     Input("App_stm", "value")],
    [State("input_stm", "value")]
)
def add_value_to_dataframe(n_clicks, time_stm, app, value):
    prev_clicks = add_value_to_dataframe.prev_clicks if hasattr(add_value_to_dataframe, 'prev_clicks') else 0
    df_timeLimit_ori = pd.read_csv("stm_data.csv")
    df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
    if value is None:
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        if df_timeLimit.empty: 
            return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["NOTHING YET"])])
        fig = px.bar(df_timeLimit, y=['TimeLimit(mins)', 'RealUsage'], barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Time (mins)', xaxis_title=None)
        fig.update_layout(legend=dict(title=None,))
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace("RealUsage", "Real Usage")))
        return dcc.Graph(id='graph_stm', figure=fig)
    elif isinstance(value, int) or value.isnumeric():
        value = float(value)
    if value == 0:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["TIME SHOULD NOT BE 0!"])])
    
    if n_clicks != prev_clicks and value is not None:
        if time_stm == 'hr(s)':
            value *= 60
        add_value_to_dataframe.prev_clicks = n_clicks
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        new_row = pd.DataFrame({"App": [app], "TimeLimit(mins)": [value]})
        df_timeLimit = pd.concat([df_timeLimit, new_row], ignore_index=True)
        df_timeLimit_ori.loc[len(df_timeLimit_ori), ["App", "TimeLimit(mins)"]] = [app, value]
        df_timeLimit_ori.to_csv("stm_data.csv", index=False)
        df_timeLimit = df_timeLimit.fillna(0)
        df_timeLimit_ori = df_timeLimit_ori.fillna(0)
        fig = px.bar(df_timeLimit, y=['TimeLimit(mins)', 'RealUsage'], barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Time (mins)', xaxis_title=None)
        fig.update_layout(legend=dict(title=None,))
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace("RealUsage", "Real Usage")))
        graph = dcc.Graph(id='graph_stm', figure=fig)
        return graph
    elif n_clicks == prev_clicks:
        df_timeLimit_ori = pd.read_csv("stm_data.csv")
        df_timeLimit = df_timeLimit_ori.loc[df_timeLimit_ori["App"] == app]
        if df_timeLimit.empty: 
            return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["NOTHING YET"])])
        fig = px.bar(df_timeLimit, y=['TimeLimit(mins)', 'RealUsage'], barmode='group', color_discrete_sequence=['#636EFA', '#EF553B'])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Time (mins)', xaxis_title=None)
        fig.update_layout(legend=dict(title=None,))
        fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("TimeLimit(mins)", "Time Limit").replace("RealUsage", "Real Usage")))
        return dcc.Graph(id='graph_stm', figure=fig)

if __name__ == '__main__':
    app.run_server(debug=True)
