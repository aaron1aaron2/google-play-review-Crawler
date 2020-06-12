import pandas as pd

df = pd.read_json('Top20_free_game_rankings.json', lines=True, orient='records')
