import pandas as pd

def generate_levels_metrics():
    games = pd.read_csv('./data/prod_data_processed.csv')

    games["completed_at"] = pd.to_datetime(games["completed_at"])
    games['started_at'] = pd.to_datetime(games['started_at'])
    games['duration'] = pd.to_timedelta(games['duration'])

    games = games[(games['success'] == True) | (games['duration'].apply(lambda x: x.total_seconds() > 5))]

    levels = pd.read_csv('./data/static/prod_levels_filtered.csv')

    # Attemtps
    level_counts = games['level'].value_counts().reset_index()
    level_counts.columns = ['level', 'attempts']

    levels = levels.merge(level_counts, on='level', how='left')

    levels['attempts'] = levels['attempts'].fillna(0).astype(int)

    # Wins
    level_wins = games[games['success'] == 1]['level'].value_counts().reset_index()
    level_wins.columns = ['level', 'wins']

    levels = levels.merge(level_wins, on='level', how='left')

    levels['wins'] = levels['wins'].fillna(0).astype(int)

    # Average Score
    average_scores = games.groupby('level')['score'].mean().reset_index()
    average_scores.columns = ['level', 'average_score']

    levels = levels.merge(average_scores, on='level', how='left')

    levels['average_score'] = levels['average_score'].fillna(0)

    # Average Duration
    games['duration_seconds'] = games['duration'].dt.total_seconds()

    average_durations = games.groupby('level')['duration_seconds'].mean().reset_index()
    average_durations.columns = ['level', 'average_duration_seconds']

    levels = levels.merge(average_durations, on='level', how='left')

    levels['average_duration_seconds'] = levels['average_duration_seconds'].fillna(0)

    # Attempts Before Success
    games = games.sort_values(by=['player', 'level', 'started_at'])

    games['attempt_number'] = games.groupby(['player', 'level']).cumcount() + 1

    first_success = games[games['success']].groupby(['player', 'level']).first().reset_index()

    games = games.merge(
        first_success[['player', 'level', 'attempt_number']],
        on=['player', 'level'],
        how='left',
        suffixes=('', '_before_success')
    )

    games['valid_attempt'] = games['attempt_number'] < games['attempt_number_before_success']

    attempts_per_player = games[games['valid_attempt']].groupby(['player', 'level'])['attempt_number'].count().reset_index()
    attempts_per_player.rename(columns={'attempt_number': 'attempts_before_success'}, inplace=True)

    average_attempts = attempts_per_player.groupby('level')['attempts_before_success'].mean().reset_index()

    levels = levels.merge(average_attempts, on='level', how='left')

    levels['attempts_before_success'] = levels['attempts_before_success'].fillna(0)

    # Duration Before Success
    games['valid_duration'] = games['valid_attempt'] * games['duration'].dt.total_seconds()

    duration_per_player = games.groupby(['player', 'level'])['valid_duration'].sum().reset_index()
    duration_per_player.rename(columns={'valid_duration': 'average_duration_before_success'}, inplace=True)

    duration_per_player = duration_per_player[duration_per_player['average_duration_before_success'] > 0]

    average_duration = duration_per_player.groupby('level')['average_duration_before_success'].mean().reset_index()

    levels = levels.merge(average_duration, on='level', how='left')

    levels['average_duration_before_success'] = levels['average_duration_before_success'].fillna(0)

    # Max score
    max_score_per_level = games.groupby('level')['score'].max().reset_index()
    max_score_per_level.rename(columns={'score': 'max_score'}, inplace=True)

    levels = levels.merge(max_score_per_level, on='level', how='left')

    levels['max_score'] = levels['max_score'].fillna(0)

    # Difficulty
    levels['difficulty'] =   1 - (levels['average_score']  / levels['max_score'])

    levels['difficulty'] = levels['difficulty'].fillna(0)

    levels['average_score'] = levels['average_score'].fillna(0)

    levels.sort_values(by='difficulty', ascending=True)

    levels.to_csv('./data/prod_levels_metrics.csv', index=False)