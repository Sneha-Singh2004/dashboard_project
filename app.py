import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

airline_data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding="ISO-8859-1",
    dtype={
        'Div1Airport': str,
        'Div1TailNum': str,
        'Div2Airport': str,
        'Div2TailNum': str
    }
)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        'Airline Performance Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 40}
    ),
    html.Div([
        "Input Year: ",
        dcc.Input(
            id='input-year',
            value=2010,
            type='number',
            style={'height': '50px', 'fontSize': 35}
        )
    ], style={'fontSize': 40}),
    html.Br(),
    html.Br(),
    dcc.Graph(id='line-plot')
])

@app.callback(
    Output('line-plot', 'figure'),
    Input('input-year', 'value')
)
def get_graph(entered_year):

    if entered_year is None:
        return go.Figure()

    df = airline_data[airline_data['Year'] == int(entered_year)]

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No data available for selected year",
            xaxis_title="Month",
            yaxis_title="Average Arrival Delay"
        )
        return fig

    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()

    fig = go.Figure(
        go.Scatter(
            x=line_data['Month'],
            y=line_data['ArrDelay'],
            mode='lines',
            marker=dict(color='green')
        )
    )

    fig.update_layout(
        title='Month vs Average Flight Delay Time',
        xaxis_title='Month',
        yaxis_title='Average Arrival Delay'
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)
