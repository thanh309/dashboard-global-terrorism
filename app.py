import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# df = pd.read_csv('assets/data.csv', encoding='ISO-8859-1')
df = pd.read_pickle('assets/cleaned_data.pkl')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, 'assets/gtd.css'], use_pages=True)
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
    'background-image':'url("assets/dark_bg3.PNG")',
    'background-size':'cover',
    'background-repeat':'no-repeat',
    'background-position':'center',
    # 'background-attachment': 'fixed',
    'height': '100vh', # Ensure the background covers the full height of the viewport
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'z-index': -1
})

if __name__ == '__main__':
    app.run(debug=True)