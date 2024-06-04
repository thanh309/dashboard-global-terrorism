import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

# dash.register_page(__name__)

layout = html.Div([
    html.H1('Time Dashboard')
])