import os
import pandas as pd
import sys
from pathlib import Path
from compute.elo.elo import ELO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
grandparent = Path(__file__).resolve().parent.parent.parent
path_file = os.path.join(grandparent, r'data\raw\tennis_games_january.csv')

df = pd.read_csv(path_file)
df = df.drop_duplicates()
df = df[df['category_name'] != 'WTA']
df_copy = df.dropna(subset=['winner'], axis=0)

elo = ELO()

for _, row in df_copy.iterrows():
    date = row['start_timestamp']
    player_a = row['home_team']
    player_b = row['away_team']
    winner = row['winner']
    elo.update_match(date, player_a, player_b, winner)

print(elo.get_leaderboard())