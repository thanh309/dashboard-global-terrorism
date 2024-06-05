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
complete_data.sort_values(['year', 'total_casualties'], inplace=True)
complete_data.reset_index(drop=True, inplace=True)


fig1 = px.choropleth(complete_data,
                    locations='country_code',
                    color='total_casualties',
                    hover_data={'Country': True, 'total_casualties': True, 'country_code': False, 'year': False},
                    range_color=(0, np.max(complete_data['total_casualties'])),
                    animation_frame='year',
                    color_continuous_scale='hot',
                    labels={'total_casualties':'Total number of casualties'},
                    template='plotly_dark'
)
sliders1=[{
    "active": 0,
    "currentvalue": {"prefix": "Year "},
    "steps": fig1.layout.sliders[0].steps,
}]
fig1.update_layout(
    plot_bgcolor='black',
    margin={"r":0,"t":10,"l":0,"b":0},
    sliders=sliders1,
)
fig1.update_layout(
    coloraxis_colorbar=dict(
        yanchor="top",
        y=0.9,
    )
)
fig1.update_traces(marker_line_width=0)
fig1.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 120
fig1.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 30


all_kill_data = complete_data.groupby(['country_code', 'Country'])['total_casualties'].sum().reset_index()
log_bin_edges = [0, 30, 100, 300, 1000, 3000, 10000, 30000, 100000, 300000000]
log_bin_labels = ['0-30', '30-100', '100-300', '300-1000', '1000-3000', '3000-10000', '10000-30000', '30000-100000', '>100000']
all_kill_data['total_casualties_cat'] = pd.cut(all_kill_data['total_casualties'], bins=log_bin_edges, labels=log_bin_labels, include_lowest=True)
all_kill_data.sort_values(['total_casualties'], inplace=True)
all_kill_data.reset_index(drop=True, inplace=True)


fig2 = px.choropleth(all_kill_data,
                    locations='country_code',
                    color='total_casualties_cat',
                    hover_data={'Country': True, 'country_code': False},
                    color_discrete_sequence=['#0d0887', '#46039f', '#7201a8', '#9c179e', '#bd3786', '#d8576b', '#ed7953', '#fb9f3a', '#fdca26', '#f0f921'],
                    labels={'total_casualties_cat':'Total number of casualties'},
                    template='plotly_dark',
)
fig2.update_layout(
    plot_bgcolor='black',
    margin={"r":0,"t":10,"l":0,"b":10},
)
fig2.update_layout(
    legend=dict(
        yanchor="top",
        y=0.9,
        # xanchor="right",
        # x=0.9,
    )
)
fig2.update_traces(marker_line_width=0)


@callback(
    Output(component_id="selected-figure", component_property="figure"),
    Input(component_id="figure-dropdown", component_property="value")
)
def update_figure(selected_value):
    if selected_value == "fig1":
        return fig1
    else:
        return fig2


layout = html.Div(children=[
    dcc.Dropdown(
        id="figure-dropdown",
        options=[
            {"label": "Figure 1", "value": "fig1"},
            {"label": "Figure 2", "value": "fig2"},
        ],
        value="fig1",
    ),
    dcc.Graph(id="selected-figure")
])