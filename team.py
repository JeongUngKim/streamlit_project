import streamlit as st
import pandas as pd
import team_url as tu
import data_init
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc

def team(team_name) :
    # 팀의 데이터를 읽어온다.
    df_teams = data_init.df_teams
    df_games = data_init.df_games
    st.header('team info')
    df_teams_info = df_teams.loc[df_teams['팀약어'] == team_name,'팀약어':]
    st.image(tu.team_url(team_name),width=500)
    st.dataframe(df_teams_info)
    st.header('시즌별 성적보기')
    team_id = df_teams[df_teams['팀약어'] == team_name]['팀ID'].values[0]
    st.subheader('홈 성적')
    start_date = st.date_input('시작 날짜')
    end_date = st.date_input('종료 날짜')
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    df_games_home = df_games.loc[ (df_games['홈팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),['경기날짜','홈팀점수','홈팀어시','홈팀리바운드','어웨이팀점수','어웨이팀어시','어웨이팀리바운드','홈팀승리여부']]
    st.dataframe(df_games_home)

    # 차트의 한글 표시
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    if st.checkbox('홈 평균') :
        fig1 = plt.figure()
        x= np.arange(3)
        x_label = ['점수','어시','리바운드']
        home_value = df_games_home.iloc[:,1:3+1].mean()
        home_value2 = df_games_home.iloc[:,4:-1].mean()
        p1=plt.bar(x,home_value,width = 0.4,color='r')
        p2=plt.bar(x+0.4,home_value2,width = 0.4,color='b')
        plt.xticks(np.arange(0.2,3+0.2,1),x_label)
        plt.legend((p1[0],p2[0]) , ('Home','Away'), fontsize = 10 )
        st.pyplot(fig1)
    else :
        st.write('')
    st.subheader('어웨이 성적')
    df_games_away =df_games.loc[ (df_games['어웨이팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),['경기날짜','홈팀점수','홈팀어시','홈팀리바운드','어웨이팀점수','어웨이팀어시','어웨이팀리바운드','홈팀승리여부']]
    st.dataframe(df_games_away)
    if st.checkbox('어웨이 평균') :
        
        fig2 = plt.figure()
        x= np.arange(3)
        x_label = ['점수','어시','리바운드']
        away_value2 = df_games_away.iloc[:,1:3+1].mean()
        away_value = df_games_away.iloc[:,4:-1].mean()
        p1=plt.bar(x,away_value,width = 0.4,color='g')
        p2=plt.bar(x+0.4,away_value2,width = 0.4,color='y')
        plt.xticks(np.arange(0.2,3+0.2,1),x_label)
        plt.legend((p1[0],p2[0]) , ('Away','Home'), fontsize = 10 )
        
        st.pyplot(fig2)
    else :
        st.write('')

    

    

