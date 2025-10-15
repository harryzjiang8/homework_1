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
    return NotImplemented








