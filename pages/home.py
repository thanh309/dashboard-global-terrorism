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

top_weapon_icons = ['chemistry.png', 'melee.png', 'incendiary.png', 'gun.png', 'explosive.png']
top_weapon_icons = ['assets/top_weapon_icons/'+image_path for image_path in top_weapon_icons]

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
    font=dict(family='Arial',size=14, color='white')
)
fig_top_groups.update_traces(
    marker_color='#FF0000'
)
c=-1
for x,y, png in zip(fig_top_groups.data[0].x, fig_top_groups.data[0].y, top_group_icons):
    c+=1
    fixed_size = (50, 50)  # Adjust these values as needed
    img = Image.open(png)
    img = img.resize(fixed_size, Image.BICUBIC)
    fig_top_groups.add_layout_image(
        x=x,
        y=y,
        source=img,
        xref="x",
        yref="y",
        sizex=3000,
        sizey=3000,
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
    font=dict(family='Arial',size=14, color='white')
)
fig_top_weapons.update_traces(
    marker_color='#FF0000'
)
c=-1
for x,y, png in zip(fig_top_weapons.data[0].x, fig_top_weapons.data[0].y, top_weapon_icons):
    c+=1
    fixed_size = (50, 50)  # Adjust these values as needed
    img = Image.open(png)
    img = img.resize(fixed_size, Image.BICUBIC)
    fig_top_weapons.add_layout_image(
        x=x,
        y=y,
        source=img,
        xref="x",
        yref="y",
        sizex=10000,
        sizey=10000,
        xanchor="center",
        yanchor="middle",  
    )

# tree map
success_attack = df[df['success'] == 1].groupby('region_txt')['success'].count()
suc_att_df = pd.DataFrame({'region_txt': success_attack.index, 'success': 'success', 'total': success_attack.values})

failure_attack = df[df['success'] == 0].groupby('region_txt')['success'].count()
fal_att_df = pd.DataFrame({'region_txt': failure_attack.index, 'success': 'failure', 'total': failure_attack.values})

tot_att_df =pd.concat([suc_att_df, fal_att_df])

fig_success_by_region = px.treemap(
    data_frame=tot_att_df,
    path=["region_txt",'success'],  # Correct column names for hierarchy
    values="total",
    color='success',
    color_discrete_sequence=["rgb(245, 22, 22)", "rgb(46, 198, 240)",  "rgb(235, 202, 96)"],
    # textinfo = "value",
    title="Total Attacks by Region",  # Update title if needed
    # textposition = 'middle center'
    hover_data=['total']
)
# fig_success_by_region.update_traces(root_color="lightgrey")
fig_success_by_region.update_layout(
    margin=dict(l=50, r=50, t=40, b=20),
)
# fig_success_by_region.update_layout(height=600, width=800,
fig_success_by_region.update_traces(root_color="black")
fig_success_by_region.update_layout(
    title_y = 0.975,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial',size=14, color='white'),
    margin=dict(l=0, r=0, t=0, b=0))
fig_success_by_region.update_traces(hovertemplate='total=%{value}<extra></extra>')


target_type = df.groupby('target_type')['target_type'].count()
tar_type_df = pd.DataFrame({'target_type': target_type.index,
                           'total': target_type.values})
tar_type_df = tar_type_df.sort_values(by='total', ascending=False)

top_5 = tar_type_df.head(5)
others = tar_type_df.iloc[5:]

others_total = others['total'].sum()
others_df = pd.DataFrame({'target_type': 'Others', 'total': others_total}, index=[0])

tar_type_df = pd.concat([top_5, others_df], ignore_index=True)
tar_type_df = tar_type_df.sort_values(by='total', ascending=False)

fig_target_type = px.pie(
    data_frame = tar_type_df,
    names = 'target_type',
    values = 'total',
    hole = 0.5,
    color='target_type',
    color_discrete_sequence=px.colors.sequential.Oryel,
)

fig_target_type.update_layout(
    title_text = "Target type's distribution", 
    title_x = 0.15,
    title_y = 0.975,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial',size=14, color='white'),
    margin=dict(l=0, r=0, t=0, b=0),
    legend={
        "x":0.9,
        "y":0.5,
        "xref":"container",
        "yref":"container"
    })
fig_target_type.update_traces(textinfo='percent', textfont_size=12,
                  marker=dict(line=dict(color='#000000', width=2)))


attack_type = df.groupby('attack_type')['attack_type'].count()
att_type_df = pd.DataFrame({'attack_type': attack_type.index,
                           'total': attack_type.values})
att_type_df = att_type_df.sort_values(by='total', ascending=False)

top_5 = att_type_df.head(5)
others = att_type_df.iloc[5:]
others_total = others['total'].sum()
others_df = pd.DataFrame({'attack_type': 'Others', 'total': others_total}, index=[0])

# Concatenate top_5 and others_df
att_type_df = pd.concat([top_5, others_df], ignore_index=True)
att_type_df = att_type_df.sort_values(by='total', ascending=False)

fig_attack_type = px.pie(
    data_frame = att_type_df,
    names = 'attack_type',
    values = 'total',
    hole = 0.5,
    color='attack_type',
    # color_discrete_sequence=px.colors.sequential.Brwnyl,
    # color_discrete_sequence=px.colors.sequential.YlOrBr,
    # color_discrete_sequence=px.colors.sequential.OrRd,
    color_discrete_sequence=px.colors.sequential.Oryel

    # hovertext='%{names}<br>Number of attacks: %{values}<extra></extra>',
    # hover_name=['target_type'],
    # hover_data= ['target_type']

)


fig_attack_type.update_layout(
    title_text = "Attack type's distribution", 
    title_x = 0.15,
    title_y = 0.975,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Arial',size=14, color='white'),
    margin=dict(l=0, r=0, t=0, b=0),
    legend={
        "x":0.9,
        "y":0.5,
        "xref":"container",
        "yref":"container"
    })
fig_attack_type.update_traces(textinfo='percent', textfont_size=12,
                  marker=dict(line=dict(color='#000000', width=2)))

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
            dcc.Graph(figure=fig_target_type),
            dcc.Graph(figure=fig_attack_type),
            dcc.Graph(figure=fig_success_by_region)
        ],
        style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1fr', 'gap': '1px', 'margin-left': '50px','margin-right': '50px',}
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
