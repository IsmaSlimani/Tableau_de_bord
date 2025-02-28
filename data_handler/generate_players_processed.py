import pandas as pd


def generate_players_processed():
    games = pd.read_csv('./data/prod_data_processed.csv')

    games["completed_at"] = pd.to_datetime(games["completed_at"])
    games['started_at'] = pd.to_datetime(games['started_at'])
    games['duration'] = pd.to_timedelta(games['duration'])

    games = games[(games['success'] == True) | (games['duration'].apply(lambda x: x.total_seconds() > 5))]

    levels = pd.read_csv('./data/prod_levels_metrics.csv')

    games = games.merge(levels, on='level', how='left')

    games['performance'] = games['score'] / games['max_score']

    games = games[['player', 'level', 'success', 'performance','score','duration']]

    games['attempts'] = 1

    games = games.groupby(['player', 'level']).agg({'success': 'max', 'score':'mean','performance':'max','attempts':'sum','duration':'mean'}).reset_index()

    games.rename(columns={'score':'average_score','duration':'average_duration'}, inplace=True)

    games.to_csv('./data/players_processed.csv', index=False)