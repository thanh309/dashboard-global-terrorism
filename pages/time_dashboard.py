import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

# Load the data
df = pd.read_pickle('assets/cleaned_data.pkl')

# Check and print column names
print(df.columns)

# Replace 'iyear' and 'country' with the actual column names
year_column = 'year'  # Adjust this if the actual column name is different
country_column = 'region_txt'  # Adjust this if the actual column name is different

# Preprocess the data
df[year_column] = pd.to_datetime(df[year_column], format='%Y').dt.year  # Ensure the year column is in integer format
df_grouped = df.groupby([year_column, country_column]).agg({'nkill':'sum', 
                                                           'nwound':'sum', 
                                                           'propvalue':'sum'}).reset_index()

# Create a DataFrame that includes all years within the range
all_years = pd.DataFrame({year_column: range(df[year_column].min(), df[year_column].max() + 1)})

# Merge with the grouped data to include all years for each country
df_merged = df_grouped.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown', 
                                                                            'nkill': 0, 
                                                                            'nwound': 0, 
                                                                            'propvalue': 0})

# Pivot the table to get years as rows and countries as columns
df_pivot = df_merged.pivot(index=year_column, columns=country_column, values=['nkill', 
                                                                             'nwound', 
                                                                             'propvalue']).fillna(0)

# Create the Plotly figures
fig_attacks = px.area(df_pivot['Total Number of Attacks'], 
                      x=df_pivot.index, 
                      y=df_pivot['Total Number of Attacks'].columns, 
                      title='Number of Terrorist Attacks per Year by Region')

fig_fatalities = px.area(df_pivot['nkill'], 
                         x=df_pivot.index, 
                         y=df_pivot['nkill'].columns, 
                         title='Number of Fatalities per Year by Region')

fig_injuries = px.area(df_pivot['nwound'], 
                       x=df_pivot.index, 
                       y=df_pivot['nwound'].columns, 
                       title='Number of Injuries per Year by Region')

fig_damage = px.area(df_pivot['propvalue'], 
                     x=df_pivot.index, 
                     y=df_pivot['propvalue'].columns, 
                     title='propvalue per Year by Region')

# Layout of the Dash app
layout = html.Div([
    html.H1('Time Dashboard'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='graph-attacks', figure=fig_attacks)
        ], className='six columns'),
        
        html.Div([
            dcc.Graph(id='graph-fatalities', figure=fig_fatalities)
        ], className='six columns'),
    ], className='row'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='graph-injuries', figure=fig_injuries)
        ], className='six columns'),
        
        html.Div([
            dcc.Graph(id='graph-damage', figure=fig_damage)
        ], className='six columns'),
    ], className='row'),
])

@app.callback(
    [Output('graph-fatalities', 'figure'),
     Output('graph-injuries', 'figure'),
     Output('graph-damage', 'figure')],
    Input('graph-attacks', 'clickData')
)
def update_graphs(clickData):
    if clickData:
        region = clickData['points'][0]['curveNumber']
        filtered_data = df_grouped[df_grouped[country_column] == region]
        
        fig_fatalities = px.area(filtered_data, 
                                 x=year_column, 
                                 y='nkill', 
                                 title=f'Number of Fatalities per Year in {region}')
        
        fig_injuries = px.area(filtered_data, 
                               x=year_column, 
                               y='nwound', 
                               title=f'Number of Injuries per Year in {region}')
        
        fig_damage = px.area(filtered_data, 
                             x=year_column, 
                             y='propvalue', 
                             title=f'propvalue per Year in {region}')
        
        return fig_fatalities, fig_injuries, fig_damage
    
    return fig_fatalities, fig_injuries, fig_damage

# if __name__ == '__main__':
#     app = Dash(__name__)
#     app.layout = layout
#     app.run_server(debug=True)
