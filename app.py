import streamlit as st
from home import home
from team import team
from player import player
def main() :
    home()
    st.sidebar.title('menu')
    team_name_list = ['ATL', 'BOS', 'NOP', 'CHI', 'DAL', 'DEN', 'HOU', 'LAC', 'LAL',
       'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX',
       'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET',
       'CHA', 'CLE', 'GSW']
    team_name = st.sidebar.selectbox('team',team_name_list)
    print(team_name)
    if team_name is not None :
        team(team_name)
    player_name = st.sidebar.selectbox('player info',[''])
    if player_name is not None :
        player(player_name)

if __name__ == '__main__' :
    main()