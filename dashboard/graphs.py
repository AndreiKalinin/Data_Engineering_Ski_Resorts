import plotly.express as px
from dashboard.data_handling import *


color_map = {'Europe': '#5bc0de',
             'Asia': '#f46c6c',
             'North America': '#ffe28a',
             'South America': '#c0e1c0',
             'Oceania': '#bbb3ec'}

figure_snow_by_month = px.line(df_snow.groupby('month', as_index=False).agg({'snow': 'mean'}),
                               x='month',
                               y='snow',
                               color_discrete_sequence=['#5bc0de'],
                               title='Average Snow Cover by Months',
                               height=410)

figure_scatter = px.scatter(df_resorts,
                            x='highest_point',
                            y='lowest_point',
                            color='continent',
                            color_discrete_map=color_map,
                            title='Highest Point & Longest Run',
                            height=410)

figure_run = px.bar(df_resorts.groupby('continent', as_index=False).agg({'longest_run': 'max'}),
                    x='continent',
                    y='longest_run',
                    color='continent',
                    color_discrete_map=color_map,
                    title='Highest & Lowest Point',
                    height=410)

figure_beginners_slopes = px.bar(df_resorts.groupby('continent', as_index=False).agg({'beginner_slopes': 'sum'}),
                                 x='continent',
                                 y='beginner_slopes',
                                 color='continent',
                                 color_discrete_map=color_map,
                                 title='Beginner Slopes by Continent',
                                 height=410)

figure_intermediate_slopes = px.bar(df_resorts.groupby('continent', as_index=False).agg({'intermediate_slopes': 'sum'}),
                                    x='continent',
                                    y='intermediate_slopes',
                                    color='continent',
                                    color_discrete_map=color_map,
                                    title='Intermediate Slopes by Continent',
                                    height=410)

figure_difficult_slopes = px.bar(df_resorts.groupby('continent', as_index=False).agg({'difficult_slopes': 'sum'}),
                                 x='continent',
                                 y='difficult_slopes',
                                 color='continent',
                                 color_discrete_map=color_map,
                                 title='Difficult Slopes by Continent',
                                 height=420)
