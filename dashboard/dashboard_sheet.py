from dash import Dash, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.io as io

from dashboard.graphs import *
from dashboard.filters import *
from dashboard.data_handling import *

io.templates.default = 'seaborn'

# app layout
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app.layout = html.Div([
    html.Div([dbc.Row(html.H1('World Ski Resorts')),
              dbc.Row([
                  dbc.Col([html.Div('Continent', style={'font-size': '20px', 'margin-bottom': '10px'}),
                           html.Div(continent_selector)], width={'size': 2}),
                  dbc.Col([html.Div('Country', style={'font-size': '20px', 'margin-bottom': '10px'}),
                           html.Div(country_selector)], width={'size': 10})
              ], style={'margin-bottom': '20px'}),
              dbc.Row([dbc.Col(dcc.Graph(id='snow_linechart', figure=figure_snow_by_month),
                               width={'size': 4}),
                       dbc.Col(dcc.Graph(id='resorts_scatter', figure=figure_scatter),
                               width={'size': 4}),
                       dbc.Col(dcc.Graph(id='resort_points', figure=figure_run),
                               width={'size': 4})
                       ],
                      style={'margin-bottom': '20px'}),
              dbc.Row([dbc.Col(dcc.Graph(id='beginners_slopes', figure=figure_beginners_slopes),
                               width={'size': 4}),
                       dbc.Col(dcc.Graph(id='intermediate_slopes', figure=figure_intermediate_slopes),
                               width={'size': 4}),
                       dbc.Col(dcc.Graph(id='difficult_slopes', figure=figure_difficult_slopes),
                               width={'size': 4})
                       ],
                      style={'margin-bottom': '20px'})
              ])
])


# callback
@app.callback([Output(component_id='snow_linechart', component_property='figure'),
               Output(component_id='resorts_scatter', component_property='figure'),
               Output(component_id='resort_points', component_property='figure'),
               Output(component_id='beginners_slopes', component_property='figure'),
               Output(component_id='intermediate_slopes', component_property='figure'),
               Output(component_id='difficult_slopes', component_property='figure')],
              [Input(component_id='continent_selector', component_property='value'),
               Input(component_id='country_selector', component_property='value')])
def update_charts(continents, countries):
    """Update all dashboards elements according to selected values"""
    chart_data_resorts = df_resorts[(df_resorts['continent'].isin(continents)) &
                                    (df_resorts['country'].isin(countries))]

    chart_data_snow = df_snow[(df_snow['continent'].isin(continents)) &
                              (df_snow['country'].isin(countries))]
    figure_snow_linechart = px.line(chart_data_snow.groupby('month', as_index=False).agg({'snow': 'mean'}),
                                    x='month',
                                    y='snow',
                                    color_discrete_sequence=['#5bc0de'],
                                    title='Average Snow Cover by Months',
                                    height=410)
    figure_snow_linechart.update_yaxes(title='Snow Cover')
    figure_snow_linechart.update_layout(showlegend=False,
                                        xaxis={'rangeslider': {'visible': True}},
                                        margin=dict(t=50, b=50),
                                        title_x=0.05)
    figure_snow_linechart.update_traces(hovertemplate='Month: %{x} <br>Average Snow Cover, %: %{y:,.0f}<extra></extra>')
    figure_resorts_scatter = px.scatter(chart_data_resorts,
                                        x='highest_point',
                                        y='lowest_point',
                                        color='continent',
                                        color_discrete_map=color_map,
                                        title='Highest & Lowest Point',
                                        height=410)
    figure_resorts_scatter.update_layout(margin=dict(t=50, b=50), title_x=0.05)
    figure_resorts_scatter.update_traces(hovertemplate='Highest Point: %{x} <br>Lowest Point: %{y:,.0f}<extra></extra>')

    figure_longest_run = px.bar(chart_data_resorts.groupby('continent', as_index=False).agg({'longest_run': 'max'}),
                                x='continent',
                                y='longest_run',
                                color='continent',
                                color_discrete_map=color_map,
                                title='Longest Run',
                                height=410)
    figure_longest_run.update_traces(hovertemplate='Continent: %{x} <br>Longest Run: %{y} <extra></extra>')
    figure_longest_run.update_yaxes(title='Longest Run')
    figure_longest_run.update_layout(showlegend=False, margin=dict(t=50, b=50), title_x=0.05)

    figure_beginners_slopes_barchart = px.bar(chart_data_resorts.groupby('continent', as_index=False)
                                                                .agg({'beginner_slopes': 'sum'}),
                                              x='continent',
                                              y='beginner_slopes',
                                              color='continent',
                                              color_discrete_map=color_map,
                                              title='Beginner Slopes by Continent',
                                              height=410)
    figure_beginners_slopes_barchart.update_traces(hovertemplate='Continent: %{x} <br>Number of Slopes: %{y} '
                                                                 '<extra></extra>')
    figure_beginners_slopes_barchart.update_yaxes(title='Slopes')
    figure_beginners_slopes_barchart.update_layout(showlegend=False, margin=dict(t=50, b=50), title_x=0.05)

    figure_intermediate_slopes_barchart = px.bar(chart_data_resorts.groupby('continent', as_index=False)
                                                 .agg({'intermediate_slopes': 'sum'}),
                                                 x='continent',
                                                 y='intermediate_slopes',
                                                 color='continent',
                                                 color_discrete_map=color_map,
                                                 title='Intermediate Slopes by Continent',
                                                 height=410)
    figure_intermediate_slopes_barchart.update_traces(hovertemplate='Continent: %{x} <br>Number of Slopes: %{y} '
                                                                    '<extra></extra>')
    figure_intermediate_slopes_barchart.update_yaxes(title='Slopes')
    figure_intermediate_slopes_barchart.update_layout(showlegend=False, margin=dict(t=50, b=50), title_x=0.05)

    figure_difficult_slopes_barchart = px.bar(chart_data_resorts.groupby('continent', as_index=False)
                                                                .agg({'difficult_slopes': 'sum'}),
                                              x='continent',
                                              y='difficult_slopes',
                                              color='continent',
                                              color_discrete_map=color_map,
                                              title='Difficult Slopes by Continent',
                                              height=410)
    figure_difficult_slopes_barchart.update_traces(hovertemplate='Continent: %{x} <br>Number of Slopes: %{y} '
                                                                 '<extra></extra>')
    figure_difficult_slopes_barchart.update_yaxes(title='Slopes')
    figure_difficult_slopes_barchart.update_layout(showlegend=False, margin=dict(t=50, b=50), title_x=0.05)

    return figure_snow_linechart, figure_resorts_scatter, figure_longest_run, \
        figure_beginners_slopes_barchart, figure_intermediate_slopes_barchart, figure_difficult_slopes_barchart
