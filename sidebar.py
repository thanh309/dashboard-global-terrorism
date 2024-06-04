import dash_bootstrap_components as dbc
from dash import html, Dash, dcc, Input, Output

from pages.home import layout as home_layout
from pages.geo_dashboard import layout as geo_layout, register_geo_callback
from pages.time_dashboard import layout as time_layout

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#282c34",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dashboard", className="display-4", style={'font-size':'30px', 'font-weight':'bold'}),
        html.Hr(),
        html.P("Welcome to our dashboard", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Geo Dashboard", href="/page-1", active="exact"),
                dbc.NavLink("Time Dashboard", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    sidebar,
    content,
    html.Div(id='children')
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/page-1":
        return geo_layout
    elif pathname == "/page-2":
        return time_layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Register callbacks for each page
register_geo_callback(app)

if __name__ == '__main__':
    app.run(debug=True, port=3000)
