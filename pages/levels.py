from dash import dcc, html
import pandas as pd
import plotly.express as px

levels_data = pd.read_csv('./data/prod_levels_metrics.csv').round(2)
levels_data['level'] = levels_data['scenario'] + ' ' + levels_data['mission']

total_games = levels_data["attempts"].sum()
total_wins = levels_data["wins"].sum()
win_percentage = (total_wins / total_games) * 100

levels_data_sorted_by_difficulty = levels_data.sort_values(
    by="difficulty", ascending=False).head(10)
levels_data_sorted_by_ease = levels_data.sort_values(
    by="difficulty", ascending=True).head(10)

levels_data_sorted_by_difficulty['difficulty'] = levels_data_sorted_by_difficulty['difficulty']
levels_data_sorted_by_ease['difficulty'] = levels_data_sorted_by_ease['difficulty']

levels_data_sorted_by_fastest = levels_data.sort_values(
    by="average_duration_seconds", ascending=True).head(10)
levels_data_sorted_by_slowest = levels_data.sort_values(
    by="average_duration_seconds", ascending=False).head(10)

levels_data_sorted_by_fastest['average_duration_seconds'] = levels_data_sorted_by_fastest['average_duration_seconds']
levels_data_sorted_by_slowest['average_duration_seconds'] = levels_data_sorted_by_slowest['average_duration_seconds']

levels_data_sorted_by_difficulty_index = levels_data.copy()
levels_data_sorted_by_difficulty_index = levels_data_sorted_by_difficulty_index.sort_values(
    by="difficulty")

fig_attempts = px.line(
    levels_data,
    x="level",
    y="attempts",
    markers=True,
    title="Number of Attempts per Level",
    labels={"attempts": "attempts", "level": "level"},
    hover_data=['level', 'attempts', 'wins', 'average_score', 'average_duration_seconds',
                'difficulty'],
)

fig_attempts_before_success = px.line(
    levels_data,
    x="level",
    y="attempts_before_success",
    markers=True,
    title="Average Attempts Before First Success",
    labels={"attempts_before_success": "attempts", "level": "level"}
)


fig_duration_before_success = px.line(
    levels_data,
    x="level",
    y="average_duration_before_success",
    markers=True,
    title="Average Duration Before First Success (seconds)",
    labels={
        "average_duration_before_success": "Duration (s)", "level": "level"}
)


fig_difficulty_vs_duration = px.scatter(
    levels_data,
    y="average_duration_seconds",  
    x="difficulty",  
    title="Difficulty Index vs Duration",
    labels={
        "average_duration_seconds": "Duration (s)",
        "level": "Level",
        "difficulty": "Difficulty Index",
        "average_score": "Score"
    },
    opacity=0.7,  
    hover_data=['level', 'average_score', 'average_duration_seconds',
                'difficulty']
)

fig_level_vs_duration = px.line(
    levels_data,
    x="level",  
    y="average_duration_seconds",  
    title="Level vs Average Duration",
    labels={
        "level": "Level",
        "average_duration_seconds": "Average Duration (s)"
    },
    template="plotly", 
)


layout = html.Div(
    [
        html.H1("Levels Statistics", className="page-title"),
        html.Div(
            [
              
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Total Games Played",
                                        className="stat-title"),
                                html.P(f"{total_games}",
                                       className="stat-value"),
                            ],
                            className="stat-block",
                        ),
                        html.Div(
                            [
                                html.H3("Win Percentage",
                                        className="stat-title"),
                                html.P(f"{win_percentage:.2f}%",
                                       className="stat-value"),
                            ],
                            className="stat-block",
                        ),
                    ],
                    className="left-column",
                ),
                html.Div(
                    dcc.Graph(figure=fig_attempts),
                    className="right-column",
                ),
            ],
            className="two-column-layout",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H3("Hardest Levels", className="sub-title"),
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [html.Th("Level"), html.Th("Difficulty Index")])
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [html.Td(level), html.Td(score)])
                                        for level, score in zip(
                                            levels_data_sorted_by_difficulty["level"],
                                            levels_data_sorted_by_difficulty["difficulty"]
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
                        html.H3("Easiest Levels", className="sub-title"),
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr(
                                        [html.Th("Level"), html.Th("Difficulty Index")])
                                ),
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [html.Td(level), html.Td(score)])
                                        for level, score in zip(
                                            levels_data_sorted_by_ease["level"],
                                            levels_data_sorted_by_ease["difficulty"]
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

            dcc.Graph(figure=fig_level_vs_duration),
            className="line-plot-container"  
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(figure=fig_attempts_before_success),
                    className="level-list-column",
                ),
                html.Div(
                    dcc.Graph(figure=fig_duration_before_success),
                    className="level-list-column",
                ),
            ],
            className="level-list-layout",
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.H3("Slowest Levels", className="sub-title"),
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr([html.Th("level"), html.Th(
                                        "attempts"), html.Th("Average Duration")])
                                ),
                                html.Tbody(
                                    [
                                        html.Tr([html.Td(level), html.Td(
                                            attempts), html.Td(score)])
                                        for level, attempts, score in zip(
                                            levels_data_sorted_by_slowest["level"],
                                            levels_data_sorted_by_slowest["attempts"],
                                            levels_data_sorted_by_slowest["average_duration_seconds"]
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
                        html.H3("Fastest Levels", className="sub-title"),
                        html.Table(
                            [
                                html.Thead(
                                    html.Tr([html.Th("level"), html.Th(
                                        "attempts"), html.Th("Average Duration")])
                                ),
                                html.Tbody(
                                    [
                                        html.Tr([html.Td(level), html.Td(
                                            attempts), html.Td(score)])
                                        for level, attempts, score in zip(
                                            levels_data_sorted_by_fastest["level"],
                                            levels_data_sorted_by_fastest["attempts"],
                                            levels_data_sorted_by_fastest["average_duration_seconds"]
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
            dcc.Graph(figure=fig_difficulty_vs_duration),
            className="scatter-plot-container" 
        )

    ],
)
