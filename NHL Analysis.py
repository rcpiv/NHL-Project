#%% Import Packages
import pandas as pd
#%% Data Loading

NHL_Pen = pd.read_csv(r'C:\Users\rcpat\Desktop\IAA\Personal Projects\NHL Penalties\Data\NHL Penalties.csv')
NHL_Games = pd.read_csv(r'C:\Users\rcpat\Desktop\IAA\Personal Projects\NHL Penalties\Data\NHL Games.csv')
NHL_Refs = pd.read_csv(r'C:\Users\rcpat\Desktop\IAA\Personal Projects\NHL Penalties\Data\NHL 2020.csv')
#%% Data Cleaning

NHL_Refs = NHL_Refs.drop('Unnamed: 0', axis=1) # Drops weird column

# Adjusting 'Date' columns to be read as dates
NHL_Pen['Date'] = pd.to_datetime(NHL_Pen['Date'])
NHL_Refs['date'] = pd.to_datetime(NHL_Refs['date'])
NHL_Games['Date'] = pd.to_datetime(NHL_Games['Date'])

# Sorting data frames to get the same order and index for each
NHL_Games = NHL_Games.sort_values(['Date','Home']).reset_index(drop=True)
NHL_Refs = NHL_Refs.sort_values(['date','home']).reset_index(drop=True)

# Assigning variable 'Game_ID' to be used 
NHL_Refs['Game_ID'] = NHL_Refs.index + 1
NHL_Games['Game_ID'] = NHL_Refs.index + 1

# Merge NHL Games Data with NHL Refs Data and dropping repeat variables
NHL = pd.merge(NHL_Games, NHL_Refs, how='inner', on='Game_ID').drop(['date','home','away'], axis=1)
NHL.columns
# Create Tables for Total Count of Linesmen and Referees
ref1 = NHL['referee1'].value_counts().reset_index()
ref2 = NHL['referee2'].value_counts().reset_index()
lines1 = NHL['linesmen1'].value_counts().reset_index()
lines2 = NHL['linesmen2'].value_counts().reset_index()

# Merge officials' tables to get total count
Refs = pd.merge(ref1,ref2, on='index', how='outer').rename(columns={'index':'Name'})
Linesmen = pd.merge(lines1,lines2, on='index').rename(columns={'index':'Name'})
Refs['Total'] = Refs['referee1'] + Refs['referee2']
Linesmen['Total'] = Linesmen['linesmen1'] + Linesmen['linesmen2']
#%% EDA
# Total Penalties 2019-2020 Regular Season: 7836
print(len(NHL_Pen.index))
    
# For a total of 18262 minutes
sum(NHL_Pen['Minutes'])
    
# Teams averaged anywhere between 6.58 and 11.29 minutes per game
# The Rangers were the most penalized at 11.29 min per game
# The Coyotes were the least penalized at 6.58 min per game
Teams = list(NHL_Games['Home'].unique())

Avg_Pen_Per_Game = NHL_Pen[['Date','Team','Minutes']].groupby(['Date','Team']).\
                    sum().sort_values(by=['Date','Minutes'], ascending=[False,False]).\
                        groupby('Team').mean('Minutes').sort_values('Minutes', ascending=False).round(2).reset_index()
print(Avg_Pen_Per_Game)

Avg_Drawn_Per_Game = NHL_Pen[['Date','Team','Minutes']].groupby(['Date','Team']).sum().reset_index()

test = pd.merge(NHL_Games, Avg_Drawn_Per_Game, how='left', left_on=['Date','Home'], right_on=['Date','Team'])

Team_Pen_Counts = {}
for team in Teams:
    Team_Pen_Counts[team] = NHL_Pen[NHL_Pen['Team'] == team]['Penalty'].value_counts()







