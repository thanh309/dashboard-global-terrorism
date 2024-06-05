import dash
from dash import html, dcc
from dash import dash_table
import plotly.express as px
import pandas as pd
from PIL import Image
import pandas as pd

dash.register_page(__name__, path='/')

df = pd.read_pickle('assets/cleaned_data.pkl')


unknowngroup_filtered_df = df[df['te_group'] != 'Unknown']
grouped_df = unknowngroup_filtered_df.groupby('te_group')['civ_killed'].sum().reset_index()
top_5_groups = grouped_df.sort_values(by='civ_killed', ascending=False).head(5)
top_5_groups = top_5_groups.sort_values(by='civ_killed', ascending=True)

unknownweapon_filtered_df = df[df['weapon_type'] != 'Unknown']
top_5_weapons = unknownweapon_filtered_df['weapon_type'].value_counts().head(5).sort_values(ascending=True)

top_group_icons = ['liber_tiger.png', 'shining_path.png', 'boko_haram.png', 'taliban.png', 'isil.png']
top_group_icons = ['assets/top_group_icons/'+image_path for image_path in top_group_icons]
fig_top_groups = px.bar(top_5_groups, 
             x='civ_killed', 
             y='te_group',
             title='Top 5 Terrorist Groups by Civilians Killed',
             labels={'te_group':'Terrorist Group', 'civ_killed':'Civilians Killed'},
             orientation='h',
            )
fig_top_groups.update_yaxes(visible=True, showticklabels=False)
fig_top_groups.update_layout(
    # margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(showline=True, linecolor='white', linewidth=2),
    yaxis=dict(showline=True, linecolor='white', linewidth=2),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial',size=18, color='gray')
)
fig_top_groups.update_traces(
    marker_color='#FF0000'
)
c=-1
for x,y, png in zip(fig_top_groups.data[0].x, fig_top_groups.data[0].y, top_group_icons):
    c+=1
    fig_top_groups.add_layout_image(
        x=x,
        y=y,
        source=Image.open(png),
        xref="x",
        yref="y",
        sizex=5000,
        sizey=5000,
        xanchor="center",
        yanchor="middle",  
    )

fig_top_weapons = px.bar(top_5_weapons, 
             x=top_5_weapons.values, 
             y=top_5_weapons.index,
             title='Top 5 Weapons by Number of Attacks',
             labels={'x':'Number of Attacks', 'weapon_type':'Weapon Types'},
             orientation='h',
            )
fig_top_weapons.update_yaxes(visible=True, showticklabels=False)
fig_top_weapons.update_layout(
    # margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(showline=True, linecolor='white', linewidth=2),
    yaxis=dict(showline=True, linecolor='white', linewidth=2),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial',size=18, color='gray')
)
fig_top_weapons.update_traces(
    marker_color='#FF0000'
)



layout = html.Div([
    html.Div(
        [
            html.Div('209.7K',className='index'),
            html.Div('585.6K',className='index'),
            html.Div('479.3K',className='index'),
            html.Div('1064.9K',className='index'),
            html.Div('Attacks',className='index'),
            html.Div('Wounded',className='index'),
            html.Div('Killed',className='index'),
            html.Div('Casualties',className='index')
        ],
        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr 1fr', 'gap': '10px'}
    ),
    html.Div(
        [
            dcc.Graph(figure=fig_top_groups),
            dcc.Graph(figure=fig_top_weapons),
            # dcc.Graph(figure=fig),
            # dcc.Graph(figure=fig)
        ],
        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '1px'}
    )
])


