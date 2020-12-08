from nhlscrapi.games.game import GameKey, Game
from nhlscrapi.games.cumstats import Corsi
import pandas as pd

nhl = {'date':[], 'home':[], 'away':[], 'referee1':[], 'referee2':[],\
       'linesmen1':[], 'linesmen2':[]}


for i in range(1000,1083):
    gk = GameKey(2020,2,i)
    game = Game(gk)
    nhl['date'].append(game.matchup['date'])
    nhl['home'].append(game.matchup['home'])
    nhl['away'].append(game.matchup['away'])
    if len(list(game.refs.values())) != 0:
        nhl['referee1'].append(list(game.refs.values())[0])
        nhl['referee2'].append(list(game.refs.values())[1])
        nhl['linesmen1'].append(list(game.linesman.values())[0])
        nhl['linesmen2'].append(list(game.linesman.values())[1])
    else:
        nhl['referee1'].append('NA')
        nhl['referee2'].append('NA')
        nhl['linesmen1'].append('NA')
        nhl['linesmen2'].append('NA')
    print(i)
    
nhl_reg_2020 = pd.DataFrame.from_dict(nhl)

nhl_reg_2020.to_csv(r"C:\Users\rcpat\OneDrive\Desktop\IAA\Personal Projects\NHL Penalties\NHL 2020.csv")
