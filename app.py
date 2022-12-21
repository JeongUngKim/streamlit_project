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
    st.sidebar.title('메뉴')
    choose  = st.sidebar.selectbox('카테고리',['홈','팀','선수'])
    if choose == '홈' :
        home()
    if choose == '팀' : 
        team_name = st.sidebar.selectbox('팀 정보',team_name_list)
        if team_name != '(팀을 선택해주세요)' :
            team(team_name)
        else : 
            st.title('팀을 선택해주세요.')
    if choose =='선수' :
        player_name = st.sidebar.text_input('선수명(영어로만)',max_chars=100)
        if player_name != '' :
            player(player_name)
        elif player_name=='' :
            st.header('선수명을 입력해주세요.')
        else :
            st.sidebar.error('선수명을 입력해주세요.')
    
    
    image = 'data:image/png;base64,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'
    st.sidebar.image(image,use_column_width='always')
if __name__ == '__main__' :
    main()