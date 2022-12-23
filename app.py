import streamlit as st
from home import home
from team import team
from player import player
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc


def main() :
     
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
            pass
            #player(player_name)
        elif player_name=='' :
            st.header('선수명을 입력해주세요.')
        else :
            st.sidebar.error('선수명을 입력해주세요.')
    
    
    image = 'https://w.namu.la/s/3e742f346a8208416b5147f2b7e86bf255bb85243262ceb3ba3668a156f338df2f3fa9b1348f9826ae0c42bf5e9d3373195ee3bfe87f9fe4f2bd21c6bc3390c50840599d9ffb25f0d104e72638441270732d7553992f377de7b6a8eaa1cc9530'
    st.sidebar.image(image,use_column_width='always')
if __name__ == '__main__' :
    main()