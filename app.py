import dash 
from dash import dcc
from dash import html
from dash.dependencies import Input, Output 
import plotly.express as px 
import plotly.graph_objects as go
import pandas as pd 
import numpy as np 

df = pd.read_csv("data2.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(className='goalInput', 
            children=[html.P(id='text1', children=["I want to reduce usage by "]),
                      dcc.Input(id='timeInput', value=5, type='number', style={
                               'display': 'inline-block',
                               'verticalAlign': 'middle',
                               'width': '30px',
                               'margin-left': '5px'
                           }),
                      dcc.Dropdown(
                        id = 'time',
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
                                'font-family': 'Helvetica'
                           }
                      ), html.P(id='granularityText', children=["every day"]),
                      html.P(id='text2', children=["in a"]),
                         dcc.Dropdown(
                        id = 'granularity',
                        options = [
                            {'label': 'Week', 'value': 'Week'},
                            {'label': 'Month', 'value': 'Month'},
                        ],
                        multi = False,
                        value = 'Week',
                        clearable = False,
                        searchable = False,
                        style={
                               'width': '70px',
                               'border-radius': '15px', 
                               'background': 'linear-gradient(to bottom right, #D1D5FA 0%, #A9DFE2 100%)',
                               'font-size': '10px',
                               'font-weight': '600',
                               'font-family': 'Helvetica'
                           }
                      ),
    ]),
    html.Div(className ="chooseApp", children=[
                    dcc.Dropdown(
                        id = 'App',
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
    html.Div(id="graphDiv", children=[
    ])
])

@app.callback(
    Output('graphDiv', 'children'),
    Output('granularityText', 'children'),
    Input('timeInput', 'value'),
    Input('time', 'value'),
    Input('granularity', 'value'),
    Input('App', 'value')  
)

def update(timeInput, time, granularity, app): 
    granularity_Text = "every day"
    if granularity == 'Month':
        granularity_Text = "every week"

    if timeInput is None:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/premium-vector/hourglass-icon-comic-style-sandglass-cartoon-vector-illustration-white-isolated-background-clock-splash-effect-business-concept_157943-6412.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["WAITING..."])]), granularity_Text
    elif isinstance(timeInput, int) or timeInput.isnumeric():
        timeInput = float(timeInput)
    else:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["TIME IS NOT APPROPRIATE!"])]), granularity_Text
    
    if timeInput == 0:
        return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["TIME SHOULD NOT BE 0!"])]), granularity_Text

    if time == "hr(s)":
        timeInput = timeInput * 60
    if granularity == 'Week':
        df_graph = df[["Index", app]]
        df_graph[app] = df_graph[app].fillna(0)
        df_graph = pd.concat([df_graph,
                      pd.DataFrame({"Index": ["Goal1", "Goal2", "Goal3", "Goal4", "Goal5", "Goal6", "Goal7"],
                                    app: [df.loc[df['Index'] == "Day1", app].values[0],
                                          df.loc[df['Index'] == "Day1", app].values[0] - timeInput,
                                          df.loc[df['Index'] == "Day1", app].values[0] - 2*timeInput,
                                          df.loc[df['Index'] == "Day1", app].values[0] - 3*timeInput,
                                          df.loc[df['Index'] == "Day1", app].values[0] - 4*timeInput,
                                          df.loc[df['Index'] == "Day1", app].values[0] - 5*timeInput,
                                          df.loc[df['Index'] == "Day1", app].values[0] - 6*timeInput]})],
                     ignore_index=True)
        if (df_graph[app] < 0).any().any():
            return html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["GOAL SET TOO LARGE"])]), granularity_Text
        df_days = df_graph.loc[(df_graph['Index'] >= 'Day1') & (df_graph['Index'] <= 'Day7')]
        df_goals = df_graph.loc[(df_graph['Index'] >= 'Goal1') & (df_graph['Index'] <= 'Goal7')].reset_index(drop=True)
        df_days.loc[:, "Goal"] = df_goals[app]
        df_days['Rating'] = np.where(df_days[app] <= df_days['Goal'], 'Good',
                        np.where(df_days[app] <= 1.1*df_days['Goal'], 'Ok', 'Bad'))
        if df_days[app].min() > 60 or df_days["Goal"].min() > 60:
            df_days[app] = df_days[app]/60
            df_days["Goal"] = df_days["Goal"]/60
            timeInput = timeInput / 60
        color_map = {'Good': '#65C089', 'Ok': '#FBD167', 'Bad': '#E16060'}
        fig = px.bar(df_days, x="Index", y=app, color="Rating", color_discrete_map=color_map, category_orders={'Index': ['Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7'], 'Rating': ['Good', 'Ok', 'Bad']})
        fig.add_scatter(x=df_days['Index'], y=df_days['Goal'], mode='markers',  marker=dict(color='black', size=15, symbol='line-ew-open'), name='Goal')
        fig.add_annotation(x="Day1", y=df_days.loc[df_days["Index"] == "Day1", app].iloc[0], text="You start here", showarrow=True, font=dict(size=8, color='black'))
        min_val = df_days.loc[df_days[app] > 0, app].min()
        min_y_axis = min(min_val, df_days['Goal'].min()) - timeInput
        if min_y_axis < 0:
            min_y_axis = 0
        fig.update_yaxes(range=[min_y_axis, max(df_days[app].max(), df_days['Goal'].max())+timeInput])
        fig.update_layout(width=372, height=403)
        fig.update_layout(yaxis_title='Usage', xaxis_title=None)
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_layout(legend=dict(title=''))
        graph = dcc.Graph(id='graph', figure=fig)
    elif granularity == 'Month':
         df_graph = df[["Index", app]]
         df_graph[app] = df_graph[app].fillna(0)
         df_graph = pd.concat([df_graph,
                      pd.DataFrame({"Index": ["Goal1", "Goal2", "Goal3", "Goal4"],
                                    app: [df.loc[df['Index'] == "Week1", app].values[0],
                                          df.loc[df['Index'] == "Week1", app].values[0] - timeInput,
                                          df.loc[df['Index'] == "Week1", app].values[0] - 2*timeInput,
                                          df.loc[df['Index'] == "Week1", app].values[0] - 3*timeInput]})],
                     ignore_index=True)
         if (df_graph[app] < 0).any().any():
            return  html.Div(id='errorDiv', children=[html.Img(id = 'errorImg', src='https://img.freepik.com/free-vector/page-found-concept-illustration_114360-1869.jpg?w=2000'),
                                                  html.H1(id='errorText', children=["GOAL SET TOO LARGE"])]), granularity_Text
         df_weeks = df_graph.loc[(df_graph['Index'] >= 'Week1') & (df_graph['Index'] <= 'Week4')].reset_index(drop=True)
         df_goals = df_graph.loc[(df_graph['Index'] >= 'Goal1') & (df_graph['Index'] <= 'Goal4')].reset_index(drop=True)
         df_weeks.loc[:, "Goal"] = df_goals[app]
         df_weeks['Rating'] = np.where(df_weeks[app] <= df_weeks['Goal'], 'Good',
                        np.where(df_weeks[app] <= 1.1*df_weeks['Goal'], 'Ok', 'Bad'))
         if df_weeks[app].min() > 60 or df_weeks["Goal"].min() > 60:
            df_weeks[app] = df_weeks[app]/60
            df_weeks["Goal"] = df_weeks["Goal"]/60
            timeInput = timeInput / 60
         color_map = {'Good': '#65C089', 'Ok': '#FBD167', 'Bad': '#E16060'}
         fig = px.bar(df_weeks, x="Index", y=app, color="Rating", color_discrete_map=color_map, category_orders={'Index': ['Week1', 'Week2', 'Week3', 'Week4'], 'Rating': ['Good', 'Ok', 'Bad']})
         fig.add_scatter(x=df_weeks['Index'], y=df_weeks['Goal'], mode='markers',  marker=dict(color='black', size=30, symbol='line-ew-open'), name='Goal')
         fig.add_annotation(x="Week1", y=df_weeks.loc[df_weeks["Index"] == "Week1", app].iloc[0], text="You start here", showarrow=True, font=dict(size=8, color='black'))
         min_val = df_weeks.loc[df_weeks[app] > 0, app].min()
         min_y_axis = min(min_val, df_weeks['Goal'].min()) - timeInput
         if min_y_axis < 0:
            min_y_axis = 0
         fig.update_yaxes(range=[min_y_axis, max(df_weeks[app].max(), df_weeks['Goal'].max())+timeInput])
         fig.update_layout(width=372, height=403)
         fig.update_layout(yaxis_title='Usage', xaxis_title=None)
         fig.update_layout(xaxis_tickangle=-45)
         fig.update_layout(legend=dict(title=''))
         graph = dcc.Graph(id='graph', figure=fig)
    return graph,granularity_Text

if __name__ == '__main__':
    app.run_server(debug=True)