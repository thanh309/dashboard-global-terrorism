import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

layout = html.Div([
    html.H1('Geographical Dashboard'),
    html.Div([
        "Select a city: ",
        dcc.RadioItems(
            options=['New York City', 'Montreal', 'San Francisco'],
            value='Montreal',
            id='analytics-input'
        )
    ]),
    html.Br(),
    html.Div(id='analytics-output'),
])

@callback(
    Output('analytics-output', 'children'),
    Input('analytics-input', 'value')
)
def update_city_selected(input_value):
    return f'You selected: {input_value}'