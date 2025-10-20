### YOUR IMPORTS HERE ###
import pandas as pd
import numpy as np

# List of columns we want to keep
COLS = ['year', 'PLAYER', 'TEAM', 'GP', 'PTS', 'REB', 'AST', 'STL', 'BLK']

def avg(to_averge: int, tot_games: int) -> float:
    return round(to_averge/tot_games, 2)

def read_NBA_stats(url: str) -> pd.DataFrame:

    df = pd.read_csv(url)
    # keep only the columns we want
    df = df[COLS]
    return df

def convert_to_averages(df: pd.DataFrame) -> pd.DataFrame:

    for col in COLS[4:]:
            df[col] = np.round(df[col]/df['GP'], 1)   
        
    return df

def player_stat(df: pd.DataFrame, player: str, season: str, stat: str) -> pd.DataFrame:

    df = df.loc[(df['PLAYER'] == player) & (df['year'] == season)].copy()
    df['stat'] = stat
    df['value'] = df[stat]
    df = df[['year', 'PLAYER', 'TEAM', 'stat', 'value']]
    df.reset_index(drop=True, inplace=True)
    
    return df

def leader(df: pd.DataFrame, season: str) -> pd.DataFrame:

    # get only stats from the given season
    df = df[df["year"] == season]
    # create a new empty data frame to input rows into
    df_leader = pd.DataFrame(columns=['PLAYER', 'TEAM', 'stat', 'value'])
    # df_leader['year'] == season

    # use to index the rows
    i = 0
    # loop for each stat we need to find the max of
    for col in COLS[3:]:
        # find the row with the highest value for the given stat
        row = df[col].idxmax()
        df_leader.loc[i] = [df.loc[row, 'PLAYER'], df.loc[row, 'TEAM'], col, df[col].max()]
        i = i+1

    df_leader.insert(0, 'year', season)
    
    return df_leader








