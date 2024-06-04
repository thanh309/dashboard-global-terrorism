import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_pickle('assets/cleaned_data.pkl')

# Initialize the Dash app
app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=[dbc.themes.COSMO])

app.title = "Global Terrorism Dashboard"

app.layout = html.Div([
    html.H1(
        children= app.title,
        style={"text-align": "center", "font-weight": "bold", 'color':'red'}),
    
    html.Div(children=[
            dbc.Button(
                children=f"{page['name']}", 
                href=page["relative_path"],
                style={"margin": "2px", "font-size": "1.25rem", "font-weight": "bold", "background-color": "red"})
        for page in dash.page_registry.values()
        ],
    ),
    
    dash.page_container
    
], style={"width": "80%", "margin": "auto"})

if __name__ == '__main__':
    app.run(debug=True)
    


#Add custom.css to assets
#custom.css: 
'''
body {
    background-color: #20232a !important;
    color: #c60c0c !important;
}

.btn-primary {
    background-color: #c60c0c !important;
    border-color: #c60c0c !important;
}
'''