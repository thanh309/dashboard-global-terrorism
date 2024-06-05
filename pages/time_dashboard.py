import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

# Load the data
df = pd.read_pickle('assets/cleaned_data.pkl')

# Check and print column names
# print(df.columns)
# print(df.dtypes)

# Replace all -99 in 'prorperty_damage' column with 0
df['prorperty_damage'] = df['prorperty_damage'].apply(lambda x: max(x, 0))
# print(df['prorperty_damage'])

# Replace 'iyear' and 'country' with the actual column names
year_column = 'year'  # Adjust this if the actual column name is different
country_column = 'region_txt'  # Adjust this if the actual column name is different

# Preprocess the data
df[year_column] = pd.to_datetime(df[year_column], format='%Y').dt.year  # Ensure the year column is in integer format
df_grouped_attacks = df.groupby([year_column, country_column]).size().reset_index(name='total_attacks')
df_grouped = df.groupby([year_column, country_column]).agg({'total_killed':'sum', 
                                                           'total_wounded':'sum',
                                                           'prorperty_damage':'sum'}).reset_index()

# Create a DataFrame that includes all years within the range
all_years = pd.DataFrame({year_column: range(df[year_column].min(), df[year_column].max() + 1)})

# Merge with the grouped data to include all years for each country
df_merged_attacks = df_grouped_attacks.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown', 'total_attacks': 0})
# print(df_merged_attacks)
df_merged = df_grouped.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown', 
                                                                            'total_killed': 0, 
                                                                            'total_wounded': 0,
                                                                            'prorperty_damage': 0})
# print(df_merged)
merged_df = pd.merge(df_merged_attacks, df_merged, on=[year_column, country_column], how='outer')
# print(merged_df)
# Pivot the table to get years as rows and countries as columns
df_pivot = merged_df.pivot(index=year_column, columns=country_column, values=['total_attacks', 
                                                                              'total_killed', 
                                                                             'total_wounded', 
                                                                             'prorperty_damage']).fillna(0)
# print(df_pivot)

# Create the Plotly figures
fig_attacks = px.area(df_pivot['total_attacks'], 
                      x=df_pivot.index, 
                      y=df_pivot['total_attacks'].columns, 
                      title='Number of Terrorist Attacks per Year by Region')

fig_fatalities = px.area(df_pivot['total_killed'], 
                         x=df_pivot.index, 
                         y=df_pivot['total_killed'].columns, 
                         title='Number of Fatalities per Year by Region')

fig_injuries = px.area(df_pivot['total_wounded'], 
                       x=df_pivot.index, 
                       y=df_pivot['total_wounded'].columns, 
                       title='Number of Injuries per Year by Region')

fig_damage = px.area(df_pivot['prorperty_damage'], 
                     x=df_pivot.index, 
                     y=df_pivot['prorperty_damage'].columns, 
                     title='Property Damage in USD per Year by Region')

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

@callback(
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
                                 y='total_killed', 
                                 title=f'Number of Fatalities per Year in {region}')
        
        fig_injuries = px.area(filtered_data, 
                               x=year_column, 
                               y='total_wounded', 
                               title=f'Number of Injuries per Year in {region}')
        
        fig_damage = px.area(filtered_data, 
                             x=year_column, 
                             y='prorperty_damage', 
                             title=f'propvalue per Year in {region}')
        
        return fig_fatalities, fig_injuries, fig_damage
    
    return fig_fatalities, fig_injuries, fig_damage

# if __name__ == '__main__':
#     app = Dash(__name__)
#     app.layout = layout
#     app.run_server(debug=True)
