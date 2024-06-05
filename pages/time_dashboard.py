import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd

dash.register_page(__name__)

# Load the data
df = pd.read_pickle('assets/cleaned_data.pkl')

# Replace all -99 in 'prorperty_damage' column with 0
df['prorperty_damage'] = df['prorperty_damage'].apply(lambda x: max(x, 0))

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
df_merged = df_grouped.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown', 
                                                                            'total_killed': 0, 
                                                                            'total_wounded': 0,
                                                                            'prorperty_damage': 0})
merged_df = pd.merge(df_merged_attacks, df_merged, on=[year_column, country_column], how='outer')

# Filter out the "Unknown" region
merged_df = merged_df[merged_df[country_column] != 'Unknown']

# Pivot the table to get years as rows and countries as columns
df_pivot = merged_df.pivot(index=year_column, columns=country_column, values=['total_attacks', 
                                                                                'total_killed', 
                                                                                'total_wounded', 
                                                                                'prorperty_damage']).fillna(0)

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

# Set showlegend=False for fig_fatalities, fig_injuries, and fig_damage
fig_attacks.update_traces(showlegend=False)
fig_fatalities.update_traces(showlegend=False)
fig_injuries.update_traces(showlegend=False)
fig_damage.update_traces(showlegend=False)

# Get the unique regions excluding 'Unknown'
regions = df[country_column].unique()
# regions = [region for region in regions if region != 'Unknown']

# Layout of the Dash app
layout = html.Div([
    html.Label('Select Status:', style={'font-size':'30px', 'font-weight':'bold', 'color': 'crimson'}), 
    dcc.RadioItems(
        id='success-radioitems',
        options=[{'label': '(All)', 'value': '(All)'}, 
                {'label': 'Successful', 'value': 'Successful'}, 
                {'label': 'Unsuccessful', 'value': 'Unsuccessful'}],
        value='(All)',
        labelStyle={'display': 'inline-block', 'margin-right': '10px'},
        inputClassName='radio-items-input',  # Apply the CSS class to hide the default radio button
        labelClassName='radio-items-label'   # Apply the CSS class to style the labels
    ),
    dcc.Checklist(
        id='region-checklist',
        options=[{'label': region, 'value': region} for region in regions],
        value=regions,
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ),
    html.Div([
        dcc.Graph(id='graph-attacks', figure=fig_attacks),
        dcc.Graph(id='graph-fatalities', figure=fig_fatalities),
        dcc.Graph(id='graph-injuries', figure=fig_injuries),
        dcc.Graph(id='graph-damage', figure=fig_damage),
        ],
        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '10px'}),
    ])

@callback(
    Output('graph-attacks', 'figure'),
    Output('graph-fatalities', 'figure'),
    Output('graph-injuries', 'figure'),
    Output('graph-damage', 'figure'),
    Input('region-checklist', 'value'),
    Input('success-radioitems', 'value')
)
def update_graphs(selected_regions, selected_status):
    # Filter the dataframe based on the selected success status
    if selected_status == 'Successful':
        filtered_df = df[df['success'] == 1]  # Assuming 'success' column exists with 1 for successful and 0 for unsuccessful
    elif selected_status == 'Unsuccessful':
        filtered_df = df[df['success'] == 0]
    else:
        filtered_df = df

    # Process data for selected regions and status
    filtered_grouped_attacks = filtered_df.groupby([year_column, country_column]).size().reset_index(name='total_attacks')
    filtered_grouped = filtered_df.groupby([year_column, country_column]).agg({'total_killed': 'sum',
                                                                                'total_wounded': 'sum',
                                                                                'prorperty_damage': 'sum'}).reset_index()
    filtered_merged_attacks = filtered_grouped_attacks.merge(all_years, on=year_column, how='right').fillna(
        {country_column: 'Unknown', 'total_attacks': 0})
    filtered_merged = filtered_grouped.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown',
                                                                                            'total_killed': 0,
                                                                                            'total_wounded': 0,
                                                                                            'prorperty_damage': 0})
    filtered_merged_df = pd.merge(filtered_merged_attacks, filtered_merged, on=[year_column, country_column],
                                    how='outer')
    filtered_merged_df = filtered_merged_df[filtered_merged_df[country_column] != 'Unknown']
    filtered_pivot = filtered_merged_df.pivot(index=year_column, columns=country_column,
                                            values=['total_attacks', 'total_killed', 'total_wounded',
                                                    'prorperty_damage']).fillna(0)

    # Filter the pivot table based on selected regions
    filtered_attacks = filtered_pivot['total_attacks'][selected_regions]
    filtered_fatalities = filtered_pivot['total_killed'][selected_regions]
    filtered_injuries = filtered_pivot['total_wounded'][selected_regions]
    filtered_damage = filtered_pivot['prorperty_damage'][selected_regions]

    fig_attacks = px.area(filtered_attacks,
                        x=filtered_attacks.index,
                        y=filtered_attacks.columns,
                        title='Number of Terrorist Attacks per Year by Region')

    fig_fatalities = px.area(filtered_fatalities,
                            x=filtered_fatalities.index,
                            y=filtered_fatalities.columns,
                            title='Number of Fatalities per Year by Region')

    fig_injuries = px.area(filtered_injuries,
                            x=filtered_injuries.index,
                            y=filtered_injuries.columns,
                            title='Number of Injuries per Year by Region')

    fig_damage = px.area(filtered_damage,
                        x=filtered_damage.index,
                        y=filtered_damage.columns,
                        title='Property Damage in USD per Year by Region')

    fig_attacks.update_traces(showlegend=False)
    fig_fatalities.update_traces(showlegend=False)
    fig_injuries.update_traces(showlegend=False)
    fig_damage.update_traces(showlegend=False)
    
    return fig_attacks, fig_fatalities, fig_injuries, fig_damage
