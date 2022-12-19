import streamlit as st
from home import home
from team import team
from player import player
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc

def main() :
    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Linux':
        rc('font', family='NanumGothic')
        
    team_name_list = ['(팀을 선택해주세요)','ATL', 'BOS', 'NOP', 'CHI', 'DAL', 'DEN', 'HOU', 'LAC', 'LAL',
       'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX',
       'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET',
       'CHA', 'CLE', 'GSW']
    st.sidebar.title('menu')
    
    team_name = st.sidebar.selectbox('team',team_name_list)
    player_name = st.sidebar.selectbox('player info',[''])
    if team_name != '(팀을 선택해주세요)' :
        team(team_name)
    elif player_name != '' :
        player(player_name)
    else :
        home()
if __name__ == '__main__' :
    main()