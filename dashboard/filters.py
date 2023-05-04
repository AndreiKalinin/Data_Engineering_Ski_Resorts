from dash import dcc
from dashboard.data_handling import df_resorts


continent_selector = dcc.Dropdown(df_resorts['continent'].unique(),
                                  id='continent_selector',
                                  multi=True,
                                  value=df_resorts['continent'].unique(),
                                  style={'color': 'black', 'fontcolor': 'black'})

country_selector = dcc.Dropdown(df_resorts['country'].unique(),
                                id='country_selector',
                                multi=True,
                                value=df_resorts['country'].unique(),
                                style={'color': 'black'})
