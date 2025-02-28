from dash import Input, Output, callback
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.time_delta import format_timedelta


sessions_df = pd.read_csv('./data/sessions.csv')
sessions_df["start_at"] = pd.to_datetime(sessions_df["start_at"])
sessions_df["end_at"] = pd.to_datetime(sessions_df["end_at"])
sessions_df["duration"] = pd.to_timedelta(sessions_df["duration"])

players_df = pd.read_csv('./data/players_processed.csv')


levels_df = pd.read_csv('./data/prod_levels_metrics.csv')

all_players = sessions_df["player"].unique()

average_session_length = f"{round(sessions_df['duration'].apply(lambda x: x.seconds).mean() / 60)} minutes"

average_games_per_player = f"{round(players_df.groupby('player')['level'].count().mean())}"


average_performance= f"{round(players_df['performance'].mean(),2)}"

median_performance = f"{round(players_df['performance'].sort_values().median(),2)}"

total_players= all_players.shape[0]


players_performances_sorted_by_best = round(players_df.groupby("player")["performance"].mean().sort_values(ascending=False).head(10).reset_index(), 2)
players_performances_sorted_by_worst = round(players_df.groupby("player")["performance"].mean().sort_values(ascending=True).head(10).reset_index(), 2)


levels_df['scenario_cat']= pd.Categorical(levels_df['scenario'], categories=levels_df['scenario'].unique(), ordered=True)
last_levels= levels_df.groupby('scenario_cat').agg({'scenario': 'last', 'level': 'last'}).reset_index()

scenario_completed_count= players_df.merge(last_levels, on='level', how='left')

scenario_completed_count.sort_values('scenario_cat', inplace=True)


scenario_completed_count.dropna(subset=['scenario'], inplace=True)
scenario_completed_count= scenario_completed_count[scenario_completed_count['success'] == True]

scenario_completed_count= scenario_completed_count.groupby('player').agg({'scenario': 'last'}).reset_index()


scenario_completed_count= scenario_completed_count.groupby('scenario').agg({'player': 'count'}).reset_index()



no_scenario= {'scenario': 'no scenario',
                         'player': all_players.shape[0] - scenario_completed_count['player'].sum()}

scenario_completed_count= pd.concat([scenario_completed_count, pd.DataFrame([no_scenario])], ignore_index=True)

blobal_sessions_lengths_df = pd.DataFrame({'duration': sessions_df['duration'].apply(lambda x: round(x.seconds / 60))})
global_peroforance_df= pd.DataFrame({'performance': players_df['performance'].apply(lambda x: round(x, 2))})

fig_performance_distribution= px.histogram(
    global_peroforance_df,
    x="performance",
    nbins=10,
    title="Performance Distribution",
    labels={"performance": "Performance"},
)
fig_sessions_distribution= px.histogram(
    blobal_sessions_lengths_df,
    x="duration",
    nbins=5,
    title="Sessions Lengths Distribution",
    labels={"duration": "Duration (min)"},
)

layout= html.Div([
    html.Div(
        [
            html.H1("Players Statistics", className="page-header"),

            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div([
                                        html.H4("Average Session Length:"),
                                        html.P(average_session_length, style={
                                               "margin-left": "10px"})
                                    ], style={"display": "flex", "align-items": "center"}),

                                    html.Div([
                                        html.H4(
                                            "Average Number of Games per Player:"),
                                        html.P(average_games_per_player, style={
                                               "margin-left": "10px"})
                                    ], style={"display": "flex", "align-items": "center"}),

                                    html.Div([
                                        html.H4("Average Performance:"),
                                        html.P(f"{average_performance}", style={
                                               "margin-left": "10px"})
                                    ], style={"display": "flex", "align-items": "center"}),

                                    html.Div([
                                        html.H4("Median Performance:"),
                                        html.P(f"{median_performance}", style={
                                               "margin-left": "10px"})
                                    ], style={"display": "flex", "align-items": "center"}),

                                    html.Div([
                                        html.H4("Total Number of Players:"),
                                        html.P(f"{total_players}", style={
                                               "margin-left": "10px"})
                                    ], style={"display": "flex", "align-items": "center"}),


                                ],
                                className="player-stats-block",
                            ),
                        ],
                        className="stat-block",
                        style={"width": "50%", "padding": "10px"},
                    ),

                    html.Div(
                        [
                            dcc.Graph(
                                id="players-pie-chart",
                                figure={
                                    "data": [
                                        {
                                            "labels": scenario_completed_count['scenario'],
                                            "values": scenario_completed_count['player'],
                                            "type": "pie",
                                        }
                                    ],
                                    "layout": {
                                        "title": "Percentage of Players Who Reached Scenario"
                                    },
                                },
                            ),
                        ],
                        className="right-column"
                    ),
                ],
                className="main-content",
                style={"display": "flex",
                       "justify-content": "space-between", "gap": "20px"},
            ), html.Div(
                [
                    html.Div(

                            dcc.Graph(figure=fig_sessions_distribution),

                        className="level-list-column",
                    ),
                    html.Div(
                            dcc.Graph(figure=fig_performance_distribution),

                        className="level-list-column",
                    ),
                ],
                className="level-list-layout", 
            ), html.Div(
                [
                    html.Div(
                        [
                            html.H3("Best Players", className="sub-title"),
                            html.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [html.Th("Player"), html.Th("Performance Index")])
                                    ),
                                    html.Tbody(
                                        [
                                            html.Tr(
                                                [html.Td(level), html.Td(score)])
                                            for level, score in zip(
                                                players_performances_sorted_by_best["player"],
                                                players_performances_sorted_by_best["performance"]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        className="level-list-column",
                    ),
                    html.Div(
                        [
                            html.H3("Worst Players", className="sub-title"),
                            html.Table(
                                [
                                    html.Thead(
                                        html.Tr(
                                            [html.Th("Player"), html.Th("Performance Index")])
                                    ),
                                    html.Tbody(
                                        [
                                            html.Tr(
                                                [html.Td(level), html.Td(score)])
                                            for level, score in zip(
                                                players_performances_sorted_by_worst["player"],
                                                players_performances_sorted_by_worst["performance"]
                                            )
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        className="level-list-column",
                    ),
                ],
                className="level-list-layout",
            ),

            html.Div(
                [
                    html.Label("Select Player:", style={
                        "font-weight": "bold", "margin-right": "10px"}),
                    dcc.Dropdown(
                        id="player-dropdown",
                        options=[{"label": f"Player {id}", "value": id}
                                 for id in all_players],
                        value='85FF7534',
                        clearable=False,  
                        style={"width": "30rem"},
                    ),
                ],
                style={"margin-bottom": "20px", "display": "flex",
                    'margin-top': '2rem', 'align-items': 'center'},
            ),
            html.Div(id="player-specific-stats",
                     className="visualization-block"),
        ],
        className = "players-page-layout",
    )
])


@ callback(
    Output("player-specific-stats", "children"),
    [Input("player-dropdown", "value")]
)
def update_player_specific_stats(selected_player_id):
    player_data= players_df[players_df["player"] == selected_player_id]
    player_data['average_duration']= pd.to_timedelta(player_data['average_duration'])


    player_data = player_data.merge(levels_df[['level', 'mission', 'scenario']], on='level', how='right')

    player_data['level_name']= player_data['scenario'] + ' ' + player_data['mission']


    player_data['average_duration']= player_data['average_duration'].apply(lambda x: x.seconds / 60)


    player_sessions = sessions_df[sessions_df['player'] == selected_player_id]

    sessions_lengths_df = pd.DataFrame({'duration': player_sessions['duration'].apply(lambda x: round(x.seconds / 60))})


    longest_session= format_timedelta(player_sessions['duration'].max())

    total_attempts= player_data['attempts'].sum()

    average_performance= player_data['performance'].mean()

    failed_levels = player_data[player_data['success'] == False].shape[0]
    completed_levels = player_data[player_data['success'] == True].shape[0]
    never_played_levels = levels_df.shape[0] - failed_levels - completed_levels

    fig_performance_distribution = px.histogram(
        sessions_lengths_df,
        x="duration",
        nbins=20,  
        title="Sessions Length Distribution",
        labels={"duration": "Duration (minutes)"},
        category_orders={"duration": sorted(
            sessions_lengths_df['duration'].unique())},
    )

    fig_performance_distribution.update_layout(
        bargap=0.2, 
        xaxis=dict(
            tickmode='array', 
            tickvals=list(range(0, 81, 10)),
            ticktext=[f"{i} min" for i in range(
                0, 81, 10)], 
        ),
    )

    fig_periods_distribution = px.histogram(
            player_sessions,
            x="period",
            title="Sessions Periods Distribution",
            labels={"period": "Period"},
            category_orders={"period": sorted(
                player_sessions['period'].unique())},
        )

    fig_periods_distribution.update_layout(
        bargap=0.2, 
    )

    fig_player_score_level= px.line(
        player_data,
        x="level_name",
        y="average_score",
        title="Player Scores Per Level",
        labels={"level_name": "Level", "average_score": "Average Score"},
    )
    fig_player_duration_level= px.line(
        player_data,
        x="level_name",
        y="average_duration",
        title="Player Levels Duration",
        labels={"level_name": "Level", "average_duration": "Average Duration"},
    )


    stats= [


        html.H3(
            f"Stats for Player {selected_player_id}", className="page-title"),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div([
                                    html.H4("Player's Performance:"),
                                    html.P(f"{average_performance:.2f}", style={
                                        "margin-left": "10px"})
                                ], style={"display": "flex", "align-items": "center"}),
                                html.Div([
                                    html.H4(
                                        "Total Games:"),
                                    html.P(total_attempts, style={
                                        "margin-left": "10px"})
                                ], style={"display": "flex", "align-items": "center"}),
                                html.Div([
                                    html.H4("Longest Session Length:"),
                                    html.P(longest_session, style={
                                        "margin-left": "10px"})
                                ], style={"display": "flex", "align-items": "center"}),




                            ],
                            className="player-stats-block",
                        ),
                    ],
                    className="stat-block",
                    style={"width": "50%", "padding": "10px"},
                ),

                html.Div(
                    [
                        dcc.Graph(
                            id="players-pie-chart",
                            figure={
                                "data": [
                                    {
                                        "labels": ["Completed", "Failed",  "Not Played"],
                                        "values": [completed_levels, failed_levels, never_played_levels],
                                        "type": "pie",
                                    }
                                ],
                                "layout": {
                                    "title": "Percentage of Player's Levels"
                                },
                            },
                        ),
                    ],
                    className="right-column",
                ),
            ],
            className= "main-content",
            style = {"display": "flex",
                   "justify-content": "space-between", "gap": "20px"},
        ), html.Div(
            [
                html.Div(
                        dcc.Graph(figure=fig_performance_distribution),

                    className="level-list-column",
                ),
                html.Div(
                        dcc.Graph(figure=fig_periods_distribution),
                    
                    className="level-list-column",
                ),
            ],
            className="level-list-layout",
        ),

        html.Div( dcc.Graph(figure=fig_player_score_level),
                        className="visualization-block",
        ),

        html.Div(
                dcc.Graph(figure=fig_player_duration_level),
            
            className="visualization-block",
        ),


    ]

    return stats
