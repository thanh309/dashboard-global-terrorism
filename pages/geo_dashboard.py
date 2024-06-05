import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import numpy as np

dash.register_page(__name__)

data: pd.DataFrame = pd.read_pickle('assets/cleaned_data.pkl')
kill_data = data[['year', 'country_code', 'country_txt', 'total_casualties']]
kill_data = kill_data.groupby(['year', 'country_code', 'country_txt'])['total_casualties'].sum().reset_index()
kill_data = kill_data.rename(columns={'country_txt': 'Country'})

all_countries = kill_data['country_code'].unique()
all_years = all_years = np.arange(1970, 2021)


all_combinations = pd.MultiIndex.from_product([all_years, all_countries], names=['year', 'country_code']).to_frame(index=False)
complete_data = pd.merge(all_combinations, kill_data, on=['year', 'country_code'], how='left')

complete_data['total_casualties'] = complete_data['total_casualties'].fillna(0)

country_names = kill_data[['country_code', 'Country']].drop_duplicates()
complete_data = pd.merge(complete_data, country_names, on='country_code', how='left')

complete_data = complete_data.sort_values(['year', 'country_code']).reset_index(drop=True)
complete_data.drop_duplicates(inplace=True)
complete_data.drop(['Country_x'], axis=1,  inplace=True)
complete_data.rename(columns={'Country_y': 'Country'}, inplace=True)

log_bin_edges = [0, 3, 10, 30, 100, 300, 1000, 3000, 10000, 30000000]
log_bin_labels = ['0-3', '3-10', '10-30', '30-100', '100-300', '300-1000', '1000-3000', '3000-10000', '>10000']
complete_data['total_casualties_cat'] = pd.cut(complete_data['total_casualties'], bins=log_bin_edges, labels=log_bin_labels, include_lowest=True)

complete_data.sort_values(['year', 'total_casualties'], inplace=True)
complete_data.reset_index(drop=True, inplace=True)


fig = px.choropleth(complete_data,
                    locations='country_code',
                    color='total_casualties',
                    hover_data={'Country': True, 'total_casualties': True, 'country_code': False, 'year': False, 'total_casualties_cat': False},
                    range_color=(0, np.max(complete_data['total_casualties'])),
                    animation_frame='year',
                    color_continuous_scale='hot',
                    color_discrete_sequence=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],
                    labels={'total_casualties':'Total number of casualties'},
                    template='plotly_dark'
)

sliders=[{
    "active": 0,
    "currentvalue": {"prefix": "Year "},
    "steps": fig.layout.sliders[0].steps,
}]


fig.update_layout(
    plot_bgcolor='black',
    margin={"r":0,"t":10,"l":0,"b":0},
    sliders=sliders,
)


# fig.update_geos(
#     showcoastlines=True, coastlinecolor="white",
#     showland=True, landcolor="gray",
#     showocean=True, oceancolor="gray",
#     showlakes=True, lakecolor="gray",
#     showrivers=True, rivercolor="gray"
# )
fig.update_layout(
    coloraxis_colorbar=dict(
        yanchor="top",
        y=0.9,
        # xanchor="left",
        # x=0.89
    )
)


fig.update_traces(marker_line_width=0)

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 120
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 30


layout = html.Div([
    html.H1('Geographical Dashboard'),
    dcc.Graph(id='total_casualties_map', figure=fig)
])