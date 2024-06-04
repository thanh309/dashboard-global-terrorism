import dash
from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd


dash.register_page(__name__)

# Load the data
df = pd.read_pickle('assets/cleaned_data.pkl')

# Check and print column names
# print(df.columns)

# Replace 'iyear' and 'country' with the actual column names
year_column = 'year'  # Adjust this if the actual column name is different
country_column = 'region_txt'  # Adjust this if the actual column name is different

# Preprocess the data
df[year_column] = pd.to_datetime(df[year_column], format='%Y').dt.year  # Ensure the year column is in integer format
df_grouped = df.groupby([year_column, country_column]).size().reset_index(name='Counts')

# Create a DataFrame that includes all years within the range
all_years = pd.DataFrame({year_column: range(df[year_column].min(), df[year_column].max() + 1)})

# Merge with the grouped data to include all years for each country
df_merged = df_grouped.merge(all_years, on=year_column, how='right').fillna({country_column: 'Unknown', 'Counts': 0})

# Pivot the table to get years as rows and countries as columns
df_pivot = df_merged.pivot(index=year_column, columns=country_column, values='Counts').fillna(0)

# Create the Plotly figure
fig = px.area(df_pivot, x=df_pivot.index, y=df_pivot.columns, title='Number of Terrorist Attacks per Year by Region')

# Layout of the Dash app
layout = html.Div([
    html.H1('Time Dashboard'),
    dcc.Graph(id='stacked-line-chart', figure=fig)
])

if __name__ == '__main__':
    app = Dash(__name__)
    app.layout = layout
    app.run_server(debug=True)