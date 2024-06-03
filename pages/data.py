import dash
from dash import dcc, html, Input, Output, dash_table, State
import dash_bootstrap_components as dbc 
import pandas as pd

# Register the page
dash.register_page(__name__)

# Load and prepare the data
df = pd.read_csv('assets/data.csv', encoding='ISO-8859-1')
all_columns = df.columns.tolist()

layout = html.Div([
    html.H2("Global Terrorism Database", style={'text-align': 'center'}), 
    html.Div([
        html.Label('Select columns to display:', style={'display': 'block', 'text-align': 'center'}),  
        dcc.Dropdown(
            id='column-selector',
            options=[{'label': col, 'value': col} for col in all_columns],
            value=all_columns[:5],  
            multi=True,
            style={'width': '500px', 'font-size': '14px', 'margin': 'auto'}  
        ),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '50%'}),  
    html.Div(
        dash_table.DataTable(
            id='table',
            data=df.head(1000).to_dict('records'),
            page_size=10,
            style_table={'height': '350px', 'width': '100%', 'overflowY': 'auto'}, 
            style_cell={
                'textAlign': 'center',  
                'color': 'black',
                'backgroundColor': 'white',
                'fontSize': '14px'  
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(210, 210, 210)',
                'color': 'black',
                'fontWeight': 'bold'
            }
        ),
        style={'margin': 'auto', 'width': '80%'}  
    ),
    html.Div([
        html.H2("Download data example", style={"text-align": "center"}),
        dcc.Download(id="download"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=[
                                {"label": "Excel file", "value": "excel"},
                                {"label": "CSV file", "value": "csv"},
                            ],
                            id="dropdown",
                            placeholder="Choose download file type. Default is CSV format!",
                            style={'width': '500px', 'font-size': '14px', 'margin': 'auto'} 
                        )
                    ],
                    style={'text-align': 'center', 'margin': 'auto', 'width': '50%'} 
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Download Data", id="btn_csv" 
                        ),
                    ],
                    width=12  
                ),
            ]
        ),
    ], style={'text-align': 'center'}) 
])

@dash.callback(
    Output('table', 'columns'),
    [Input('column-selector', 'value')]
)
def update_columns(selected_columns):
    return [{"name": col, "id": col} for col in selected_columns]

@dash.callback(
    Output("download", "data"),
    Input("btn_csv", "n_clicks"),
    State("dropdown", "value"),
    prevent_initial_call=True,
)
def download_data(n_clicks_btn, download_type):
    if download_type == "csv":
        return dcc.send_data_frame(df.to_csv, "assets/data.csv")
    else:
        return dcc.send_data_frame(df.to_excel, "assets/data.xlsx")