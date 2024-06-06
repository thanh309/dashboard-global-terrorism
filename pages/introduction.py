import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = html.Div([
    html.Div([
        html.H2(children="Overview of the GTD",
                style={'font-size': '25px', 'color': 'red'}),
        html.P("The Global Terrorism Database™ (GTD) is an open-source database including information on terrorist events around the world from 1970 through 2020 (with additional annual updates planned for the future). Unlike many other event databases, the GTD includes systematic data on domestic as well as transnational and international terrorist incidents that have occurred during this time period and now includes more than 200,000 cases. For each GTD incident, information is available on the date and location of the incident, the weapons used and nature of the target, the number of casualties, and--when identifiable--the group or individual responsible."),
        html.P("Statistical information contained in the Global Terrorism Database is based on reports from a variety of open media sources. Information is not added to the GTD unless and until we have determined the sources are credible. Users should not infer any additional actions or results beyond what is presented in a GTD entry and specifically, users should not infer an individual associated with a particular incident was tried and convicted of terrorism or any other criminal offense. If new documentation about an event becomes available, an entry may be modified, as necessary and appropriate."),
    ], style={"background-color": "#282c34", "color": "white", 'width': '50%', 'margin': 'auto', 'float': 'left', 'padding': '20px'}),

    html.Div([
        html.Img(src='/assets/terrorism.jpg', style={'width': '100%', 'margin': 'auto'}),
    ], style={'width': '50%', 'float': 'right', 'height': '100%', 'padding-top': '20px'}),

    html.Div([
        html.P("The National Consortium for the Study of Terrorism and Responses to Terrorism (START) makes the GTD available via this online interface in an effort to increase understanding of terrorist violence so that it can be more readily studied and defeated."),
        html.H3(children="Characteristics of the GTD", style={'font-size': '20px', 'color': 'red'}),
        html.Ul([
            html.Li("Contains information on over 200,000 terrorist attacks."),
            html.Li("Currently the most comprehensive unclassified database on terrorist attacks in the world."),
            html.Li("Includes information on more than 88,000 bombings, 19,000 assassinations, and 11,000 kidnappings since 1970."),
            html.Li("Includes information on at least 45 variables for each case, with more recent incidents including information on more than 120 variables"),
            html.Li("More than 4,000,000 news articles and 25,000 news sources were reviewed to collect incident data from 1998 to 2017 alone."),
        ]),
        html.A('Follow this link to download the GTD dataset', href='https://www.start.umd.edu/gtd/', style={'font-size': '20px'}),
        html.Br(style={'margin': '30px'}),
        html.H2('About our dashboard', style={'font-size': '25px', 'color': 'red'}),
        html.P(['Our group developed the Global Terrorism Dashboard utilizing ', html.A("Plotly-Dash.", href="https://dash.plotly.com/")]),
        html.P("When the users open the dashboard, first they see the Home page. In the Home page, we have 4 buttons: Introduction, Home, Geo Dashboard, Time Dashboard to switch back and forth between pages. Beneath these buttons lie four indices - Attacks, Wounded, Killed, and Casualties - providing specific numeric data for each criterion. The Home page also hosts various informative charts such as pie charts, bar charts, and treemaps."),
        html.P("The Introduction page provides a concise overview of the project, including details on the dataset, as well as an explanation of the dashboard's features and functionalities."),
        html.P("Navigating to the Geo Dashboard, users will find two choropleth maps positioned at the top, illustrating global casualty trends by year and the aggregate number of casualties. Beneath these maps, there is a pie chart depicting the frequency of attacks across different regions and a bar chart delineating the types of attacks occurring within each region."),
        html.P("Lastly, the Time Dashboard presents line charts showcasing the frequency of terrorist attacks, fatalities, injuries, and property damage (in USD) per year, segmented by region. Users can utilize a dropdown menu to filter data based on attack status (Successful and Unsuccessful Attack)."),
    ], style={"background-color": "#282c34", "color": "white", 'width': '100%', 'margin': 'auto', 'padding': '20px', 'margin-top': '20px'})
])