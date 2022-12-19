import streamlit as st
from home import home
from team import team
from player import player
def main() : 
    team_name_list = ['','ATL', 'BOS', 'NOP', 'CHI', 'DAL', 'DEN', 'HOU', 'LAC', 'LAL',
       'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX',
       'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET',
       'CHA', 'CLE', 'GSW']
    st.sidebar.title('menu')
    
    team_name = st.sidebar.selectbox('team',team_name_list)
    player_name = st.sidebar.selectbox('player info',[''])
    if team_name != '' :
        team(team_name)
    elif player_name != '' :
        player(player_name)
    else :
        home()
if __name__ == '__main__' :
    main()