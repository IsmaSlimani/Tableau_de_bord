import pandas as pd
import os


def generate_data_processed():
    levels = pd.read_csv('./data/static/prod_levels_filtered.csv')

    while not os.path.exists('./data/prod_data.csv'):
        pass

    df = pd.read_csv('./data/prod_data.csv')


    df['timestamp'] = pd.to_datetime(
        df['timestamp'], format='ISO8601').dt.tz_localize(None)

    df = df.sort_values(by=['timestamp'], ascending=False)

    df.drop_duplicates(
        subset=['verb', 'player', 'timestamp'], keep='first', inplace=True)


    for index, row in df[df['verb'] == 'completed'].iterrows():
        matching_row = df[(df.index > index) & (df['verb'] == 'launched') & (
            df['player'] == row['player'])].head(1)
        if not matching_row.empty:
            df.at[index, 'level'] = matching_row['level'].values[0]

            df.at[index, 'started_at'] = matching_row['timestamp'].values[0]

            df.at[index, 'duration'] = row['timestamp'] - \
                matching_row['timestamp'].values[0]


    df = df[df['level'].isin(levels['level'])]


    for index, row in df[df['verb'] == 'exited'].iterrows():
        matching_row = df[(df.index > index) & (df['verb'] != 'exited') & (
            df['player'] == row['player']) & (df['level'] == row['level'])].head(1)

        if not matching_row.empty and matching_row['verb'].values[0] == 'launched':
            df.at[index, 'started_at'] = matching_row['timestamp'].values[0]

            df.at[index, 'score'] = 0
            df.at[index, 'success'] = False

            df.at[index, 'duration'] = row['timestamp'] - \
                matching_row['timestamp'].values[0]

    df.dropna(subset=['success'], inplace=True)
    df.rename(columns={'timestamp': 'completed_at'}, inplace=True)
    df.drop('verb', axis=1, inplace=True)

    df.to_csv('./data/prod_data_processed.csv', index=False)
