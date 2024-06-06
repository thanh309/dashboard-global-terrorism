import dash
from dash import Dash, dcc, html, Input, Output, State, callback, ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.COSMO, 'assets/gtd.css'], use_pages=True)
app.title = "Global Terrorism Dashboard"

# Define the desired order of the pages
page_order = ['Introduction', 'Home', 'Geo dashboard', 'Time dashboard']
page_dict = {page['name']: page for page in dash.page_registry.values()}
ordered_pages = [page_dict[name] for name in page_order if name in page_dict]

app.layout = html.Div([
    html.H1(
        children='Global Terrorism Dashboard',className='title',
        style={'textAlign':'center'}),
    html.Div([
        html.Div(
            dbc.Button(
                children=f"{page['name']}", 
                id={'type': 'page-button', 'index': page['relative_path']},
                href=page["relative_path"],className='page-button',
                style={'margin-right':'10px', 'borderColor': 'white', 'borderRadius': '10px'}) # Padding between buttons
        ) for page in ordered_pages
    ], style={'display':'flex', 'justifyContent':'center', 'flexWrap':'wrap', 'margin-bottom':'38px'}),
    dash.page_container
], style={
    'background-image':'url("assets/dark_bg1.PNG")',
    'background-size':'cover',
    'background-repeat':'no-repeat',
    'background-position':'center',
    'background-attachment': 'fixed',
    'height': '200vh',
    'top': 0,
    'left': 0,
    'z-index': -1
})

@app.callback(
    Output({'type': 'page-button', 'index': ALL}, 'className'),
    Input({'type': 'page-button', 'index': ALL}, 'n_clicks'),
    [State({'type': 'page-button', 'index': ALL}, 'id')]
)
def update_active_button(n_clicks, button_ids):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ['page-button'] * len(button_ids)

    clicked_button_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
    
    new_classes = []
    for button_id in button_ids:
        if button_id == clicked_button_id:
            new_classes.append('page-button active')
        else:
            new_classes.append('page-button')
    
    return new_classes


if __name__ == '__main__':
    app.run(debug=True)