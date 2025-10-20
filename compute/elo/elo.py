import numpy as np
import pandas as pd

class ELO:
    def __init__(self):
        self.players = {}
    
    def _initialize_player(self, player_name):
        if player_name not in self.players:
            self.players[player_name] = {
                'elo': 400,
                'n_games':0
            }

    def get_k(self, player_name):
        self._initialize_player(player_name)
        n_games = self.players[player_name]['n_games']
        return np.round(16 + 16 * np.exp(-0.072 * (n_games - 1)), 0)

    def get_elo(self, player_name):
        self._initialize_player(player_name)
        return self.players[player_name]['elo']
    
    def update_match(self, player1, player2, winner):
        r1 = self.get_elo(player1)
        r2 = self.get_elo(player2)

        k1 = self.get_k(player1)
        k2 = self.get_k(player2)

        e1 = 1 / (1 + 10 ** ((r2 - r1) / 400))
        e2 = 1 / (1 + 10 ** ((r1 - r2) / 400))

        # winner is store as 1 for player1 or 2 for player2
        s1 = int(winner == 1)
        s2 = int(winner == 2)

        r1_prime = round(r1 + k1 * (s1 - e1), 0)
        r2_prime = round(r2 + k2 * (s2 - e2), 0)

        self.players[player1]['elo'] = r1_prime
        self.players[player2]['elo'] = r2_prime

        self.players[player1]['n_games'] += 1
        self.players[player2]['n_games'] += 1

    def get_leaderboard(self, top_n=10):
        sorted_players = sorted(self.players.items(), 
                            key=lambda x: x[1]['elo'], 
                            reverse=True)[:top_n]
        
        data = [
            {
                'Rank': i + 1,
                'Player': player_name,
                'Elo': info['elo'],
                'Games': info['n_games']
            }
            for i, (player_name, info) in enumerate(sorted_players)
        ]
        
        df = pd.DataFrame(data)
        df.set_index('Rank', inplace=True)
        return df




