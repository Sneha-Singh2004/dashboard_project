import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# ------------------------------------------------
# Load Dataset (IBM Online Source)
# ------------------------------------------------
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv")

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month

year_list = [i for i in range(1980, 2024)]

# ------------------------------------------------
# Create Dash App
# ------------------------------------------------
app = dash.Dash(__name__)

app.layout = html.Div([

    # Title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': '24px'
        }
    ),

    # Report Type Dropdown
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
        ],
        value='Yearly Statistics',
        placeholder='Select a report type',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),

    # Year Dropdown
    dcc.Dropdown(
        id='select-year',
        options=[{'label': i, 'value': i} for i in year_list],
        value=1980,
        placeholder='Select-year',
        style={
            'width': '80%',
            'padding': '3px',
            'font-size': '20px',
            'text-align-last': 'center'
        }
    ),

    html.Br(),

    # Output Container
    html.Div(id='output-container')
])

# ------------------------------------------------
# Callback 1: Enable / Disable Year Dropdown
# ------------------------------------------------
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'


# ------------------------------------------------
# Callback 2: Generate Graphs
# ------------------------------------------------
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, selected_year):

    # ---------------- RECESSION REPORT ----------------
    if selected_statistics == 'Recession Period Statistics':

        recession_data = df[df['Recession'] == 1]

        # Plot 1
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales',
                       title='Average Automobile Sales During Recession')

        # Plot 2
        vehicle_rec = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(vehicle_rec, x='Vehicle_Type', y='Automobile_Sales',
                      title='Average Vehicles Sold by Type During Recession')

        # Plot 3
        ad_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(ad_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                      title='Advertising Expenditure Share During Recession')

        # Plot 4
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        fig4 = px.bar(unemp_data,
                      x='unemployment_rate',
                      y='Automobile_Sales',
                      color='Vehicle_Type',
                      labels={
                          'unemployment_rate': 'Unemployment Rate',
                          'Automobile_Sales': 'Average Automobile Sales'
                      },
                      title='Effect of Unemployment Rate on Vehicle Type and Sales')

    # ---------------- YEARLY REPORT ----------------
    else:

        yearly_data = df[df['Year'] == selected_year]

        # Plot 1
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yas, x='Year', y='Automobile_Sales',
                       title='Average Yearly Automobile Sales')

        # Plot 2
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig2 = px.line(mas, x='Month', y='Automobile_Sales',
                       title=f'Total Monthly Automobile Sales in {selected_year}')

        # Plot 3
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                      title=f'Average Vehicles Sold by Vehicle Type in {selected_year}')

        # Plot 4
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(exp_data,
                      values='Advertising_Expenditure',
                      names='Vehicle_Type',
                      title='Total Advertisement Expenditure for Each Vehicle')

    # 2x2 Layout
    return [
        html.Div([
            html.Div(dcc.Graph(figure=fig1), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=fig2), style={'width': '50%'})
        ], style={'display': 'flex'}),

        html.Div([
            html.Div(dcc.Graph(figure=fig3), style={'width': '50%'}),
            html.Div(dcc.Graph(figure=fig4), style={'width': '50%'})
        ], style={'display': 'flex'})
    ]


# ------------------------------------------------
# Run App
# ------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

