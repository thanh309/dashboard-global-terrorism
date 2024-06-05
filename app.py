import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# df = pd.read_csv('assets/data.csv', encoding='ISO-8859-1')
df = pd.read_pickle('assets/cleaned_data.pkl')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, 'assets/gtd.css'], use_pages=True)
app.title = "Global Terrorism Dashboard"
app.layout = html.Div([
    html.H1(
        children='Global Terrorism Dashboard',className='title',
        style={'textAlign':'center'}),
    html.Div([
        html.Div(
            dbc.Button(
                children=f"{page['name']}", 
                href=page["relative_path"],className='page-button',
                style={'margin-right':'10px'}) # Padding between buttons
        ) for page in dash.page_registry.values()
    ], style={'display':'flex', 'justifyContent':'center', 'flexWrap':'wrap'}),
    dash.page_container
], style={
    'background-image':'url("assets/main_background.jpg")',
    'background-size':'stretch',
    'background-repeat':'no-repeat',
    'background-position':'center',
    'height': '100vh'  # Ensure the background covers the full height of the viewport
})

if __name__ == '__main__':
    app.run(debug=True)