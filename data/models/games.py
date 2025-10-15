import requests
import pandas as pd
import time
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

headers = {
    "x-rapidapi-key": os.environ["RAPIDAPI_KEY"],
    "x-rapidapi-host": os.environ["RAPIDAPI_HOST"]
}

key_paths = [
    ['startTimestamp'],
    ['tournament', 'name'],
    ['tournament', 'uniqueTournament', 'category', 'name'],
    ['tournament', 'uniqueTournament', 'groundType'],
    ['roundInfo', 'name'],
    ['status', 'description'],
    ['winnerCode'],
    ['homeTeam', 'name'],
    ['awayTeam', 'name'],
    ['homeScore', 'period1'],
    ['homeScore', 'period2'],
    ['homeScore', 'period3'],
    ['homeScore', 'period4'],
    ['homeScore', 'period5'],
    ['awayScore', 'period1'],
    ['awayScore', 'period2'],
    ['awayScore', 'period3'],
    ['awayScore', 'period4'],
    ['awayScore', 'period5']
]

column_names = [
    'start_timestamp',
    'tournament_name',
    'category_name',
    'ground_type',
    'round_name',
    'status',
    'winner',
    'home_team',
    'away_team',
    'home_set1', 'home_set2', 'home_set3', 'home_set4', 'home_set5',
    'away_set1', 'away_set2', 'away_set3', 'away_set4', 'away_set5',
]

def get_nested_value(d, keys):
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return None
    return d

valid_categories = ['ATP', 'WTA', 'Challenger']

rows = []
host = os.environ["RAPIDAPI_HOST"]

for day in range(1, 32):
    print(f'day number {day}')
    time.sleep(2)
    url = f"https://{host}/api/tennis/events/{day}/7/2025"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'events' not in data:
            continue
        
        for event in data['events']:
            category = get_nested_value(event, ['tournament', 'uniqueTournament', 'category', 'name'])
            
            if category in valid_categories:
                row = [get_nested_value(event, keys) for keys in key_paths]
                rows.append(row)
                
    except Exception as e:
        print(f"Error fetching data for day {day}: {e}")
        continue

df = pd.DataFrame(rows, columns=column_names)

df = df[
    (~df['home_team'].astype(str).str.contains('/', na=False)) &
    (~df['away_team'].astype(str).str.contains('/', na=False))
]

df['start_timestamp'] = pd.to_numeric(df['start_timestamp'], errors='coerce')
df = df.sort_values(by='start_timestamp', ascending=True).reset_index(drop=True)


grandparent = Path(__file__).resolve().parent.parent
csv_path = os.path.join(grandparent, r'raw\tennis_games_july.csv')
df.to_csv(csv_path, index=False)

print(f"Final dataset shape (after removing doubles): {df.shape}")
