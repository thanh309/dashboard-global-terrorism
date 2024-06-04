import dash
from dash import html
import dash_bootstrap_components as dbc

# dash.register_page(__name__, path='/')

layout = html.Div([
    html.Img(src='/assets/terrorism.jpg', style={'width': '100%', 'height': 'auto'}),
    html.Br(),
    dbc.Card(
        dbc.CardBody(
            [
                html.H2(children="Overview of the GTD",
                        style={'font-size': '25px', 'color': 'red'}),
                html.P("The Global Terrorism Database™ (GTD) is an open-source database including information on terrorist events around the world from 1970 through 2020 (with additional annual updates planned for the future). Unlike many other event databases, the GTD includes systematic data on domestic as well as transnational and international terrorist incidents that have occurred during this time period and now includes more than 200,000 cases. For each GTD incident, information is available on the date and location of the incident, the weapons used and nature of the target, the number of casualties, and--when identifiable--the group or individual responsible."),
                html.P("Statistical information contained in the Global Terrorism Database is based on reports from a variety of open media sources. Information is not added to the GTD unless and until we have determined the sources are credible. Users should not infer any additional actions or results beyond what is presented in a GTD entry and specifically, users should not infer an individual associated with a particular incident was tried and convicted of terrorism or any other criminal offense. If new documentation about an event becomes available, an entry may be modified, as necessary and appropriate."),
                html.P("The National Consortium for the Study of Terrorism and Responses to Terrorism (START) makes the GTD available via this online interface in an effort to increase understanding of terrorist violence so that it can be more readily studied and defeated."),
                html.H3(children="Characteristics of the GTD",  style={'font-size': '20px', 'color': 'red'}),
                html.Ul(
                    [
                        html.Li("Contains information on over 200,000 terrorist attacks."),
                        html.Li("Currently the most comprehensive unclassified database on terrorist attacks in the world."),
                        html.Li("Includes information on more than 88,000 bombings, 19,000 assassinations, and 11,000 kidnappings since 1970."),
                        html.Li("Includes information on at least 45 variables for each case, with more recent incidents including information on more than 120 variables"),
                        html.Li("More than 4,000,000 news articles and 25,000 news sources were reviewed to collect incident data from 1998 to 2017 alone."),
                    ]
                )
            ]
        ),
        style={"background-color": "#282c34", "color": "white"}
    )
])
