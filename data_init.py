import pandas as pd

df_teams = pd.read_csv('data/teams.csv')
df_games = pd.read_csv('data/games.csv')
df_players = pd.read_csv('data/players.csv')
df_games_detail = pd.read_csv('data/games_details.csv',low_memory = False)

df_teams = df_teams.loc[:,['TEAM_ID','ABBREVIATION','YEARFOUNDED','CITY','ARENA']]
df_games = df_games.loc[:,['GAME_DATE_EST','GAME_ID','HOME_TEAM_ID','PTS_home','AST_home','REB_home','TEAM_ID_away','PTS_away','AST_away','REB_away','HOME_TEAM_WINS']]
# 문제 없는 데이터프레임
df_games_detail_1 = df_games_detail.loc[:,:'START_POSITION']
# 문제 있는 데이터프레임 짜른 뒤 수정
df_games_detail_2 = df_games_detail.loc[:,'COMMENT':].shift(-1,axis= 1)
# 짜른 두 코드를 합쳤다.
df_games_detail = pd.concat([df_games_detail_1,df_games_detail_2],axis=1)
df_games_detail = df_games_detail.loc[:,['GAME_ID', 'TEAM_ID','PLAYER_ID','PLAYER_NAME','START_POSITION',
                       'COMMENT','MIN', 'FG_PCT', 'FG3_PCT', 
                       'DREB', 'REB', 'AST', 'STL', 'BLK','TO']]
rename ={ 'GAME_DATE_EST' : '경기날짜' ,'GAME_ID':'경기ID', 'HOME_TEAM_ID':'홈팀ID','PTS_home':'홈팀점수','AST_home':'홈팀어시','REB_home':'홈팀리바운드','TEAM_ID_away':'어웨이팀ID','PTS_away':'어웨이팀점수','AST_away':'어웨이팀어시','REB_away':'어웨이팀리바운드','HOME_TEAM_WINS':'홈팀승리여부'  }
df_games = df_games.rename(columns=rename)
df_games=df_games.fillna(0)

rename_detail = { 'GAME_ID':'경기ID','TEAM_ID':'팀ID','PLAYER_ID':'선수ID','PLAYER_NAME':'선수명',
                 'START_POSITION':'포지션',
 'COMMENT':'출전시간','MIN':'2점슛', 'FG_PCT':'3점슛', 'FG3_PCT':'자유투',
 'DREB':'리바운드','REB':'어시스트','AST':'가로채기','STL':'블락','BLK':'턴오버','TO':'파울'}
df_games_detail = df_games_detail.rename(columns=rename_detail)
df_games_detail = df_games_detail.fillna(0)
    
rename_playes = { 'PLAYER_NAME':'선수명','TEAM_ID':'팀ID','PLAYER_ID':'선수ID','SEASON':'시즌' }
df_players=df_players.rename(columns=rename_playes)
    
rename_team = {'TEAM_ID':'팀ID','ABBREVIATION':'팀약어','YEARFOUNDED':'팀창설해',
                'CITY':'연고지','ARENA':'홈구장'}
df_teams = df_teams.rename(columns=rename_team)

 # 가공을 편하게 하기위해 df_games에 홈팀명,어웨이팀명 추가
df_teams_home = df_teams.rename(columns={'팀ID':'홈팀ID'})
new_data = pd.merge(df_games,df_teams_home, on = '홈팀ID').iloc[:,:-3].rename(columns={'팀약어':'홈팀'})
df_teams_away = df_teams.rename(columns={'팀ID':'어웨이팀ID'})
df_games=pd.merge(new_data,df_teams_away,on = '어웨이팀ID').iloc[:,:-3].rename(columns={'팀약어':'어웨이팀'})

# 가공을 편하게 하기 위해 df_platers에 팀명 추가
df_players=pd.merge(df_players,df_teams,on='팀ID').iloc[:,0:4+1]

# 가공을 편하게 하기 위해 df_games_detail 에 날짜 추가
df_games_detail=pd.merge(df_games_detail,df_games,on='경기ID').loc[:,:'경기날짜'].sort_values('경기날짜',ascending=False)

# 가공을 편하게 하기위해 df_games_detail에 약어 추가
df_games_detail = pd.merge(df_games_detail,df_teams,on='팀ID').iloc[:,:-3]