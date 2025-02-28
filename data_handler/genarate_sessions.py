import pandas as pd

def generate_sessions():
    games = pd.read_csv('./data/prod_data_processed.csv')

    games["completed_at"] = pd.to_datetime(games["completed_at"])
    games['started_at'] = pd.to_datetime(games['started_at'])
    games['duration'] = pd.to_timedelta(games['duration'])


    games['started_at'] = pd.to_datetime(games['started_at'])
    games['completed_at'] = pd.to_datetime(games['completed_at'])

    games.reset_index(drop=True, inplace=True)

    games = games.sort_values(by=['player', 'started_at'])


    games["previous_completed_at"] = games['completed_at'].shift(1)

    def assign_session_ids(group):
        time_diff = group['started_at'] - group['previous_completed_at']
        new_session = (time_diff >= pd.Timedelta(minutes=15)) | (time_diff.isna())
        group['session_id'] = new_session.cumsum()
        return group

    games = games.groupby('player').apply(assign_session_ids).reset_index(drop=True)

    sessions = games.groupby(['player', 'session_id']).agg(
        start_at=('started_at', 'min'),
        end_at=('completed_at', 'max')
    ).reset_index()

    sessions['duration'] = sessions['end_at'] - sessions['start_at']

    def get_period(start_at):
        hour = start_at.hour
        if 6 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        else:
            return 'evening'

    sessions['period'] = sessions['start_at'].apply(get_period)

    sessions.to_csv('./data/sessions.csv', index=False)