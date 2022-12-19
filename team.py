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
    df_games_detail = data_init.df_games_detail
    # 팀정보 헤더 지정
    st.header(team_name+'의 정보')
    # 팀의 맞는 이미지 생성
    st.image(tu.team_url(team_name),width=500)
    # 사이드바에서 선택한 팀으로 정보
    df_teams_info = df_teams.loc[df_teams['팀약어'] == team_name,'팀약어':]
    st.dataframe(df_teams_info)
    
    # 시즌별 성적보기
    st.header('일자별 성적보기')
    team_id = df_teams[df_teams['팀약어'] == team_name]['팀ID'].values[0]
    st.subheader('홈 성적')
    # 시작과 끝 종료날짜를 설정하여 데이터 가져오기
    start_date = st.date_input('시작 날짜')
    end_date = st.date_input('종료 날짜')
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    if start_date > end_date :
        st.error('시작 날짜를 종료 날짜보다 전으로 설정해주세요.')
    # 전적을 비교하기 위한 list 생성
    team_name_list = ['','ATL', 'BOS', 'NOP', 'CHI', 'DAL', 'DEN', 'HOU', 'LAC', 'LAL',
       'MIA', 'MIL', 'MIN', 'BKN', 'NYK', 'ORL', 'IND', 'PHI', 'PHX',
       'POR', 'SAC', 'SAS', 'OKC', 'TOR', 'UTA', 'MEM', 'WAS', 'DET',
       'CHA', 'CLE', 'GSW']    
    
    df_games_home = df_games.loc[ (df_games['홈팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),:]
    st.dataframe(df_games_home.iloc[:,[11,12,0,3,4,5,7,8,9]])
    # 차트의 표시
    font_name = font_manager.FontProperties(fname="malgun.ttf").get_name()
    rc('font', family=font_name)
    if st.checkbox('홈 성적 자세히보기') :
        st.subheader('최근 대결 성적')
        fig1 = plt.figure()
        x= np.arange(3)
        x_label = ['점수','어시','리바운드']
        
        home_value = df_games_home.iloc[:,3:5+1].mean()
        home_value2 = df_games_home.iloc[:,7:-3].mean()
        p1=plt.bar(x,home_value,width = 0.4,color='r')
        p2=plt.bar(x+0.4,home_value2,width = 0.4,color='b')
        plt.xticks(np.arange(0.2,3+0.2,1),x_label)
        plt.legend((p1[0],p2[0]) , ('Home','Away'), fontsize = 10 )
        st.pyplot(fig1)

        st.dataframe(df_games_home.iloc[:,[3,4,5,7,8,9]].mean())
        st.subheader('역대 홈 전적비교')
        compare_home_team = st.selectbox('팀선택',team_name_list)
        if compare_home_team != '' : 
            compare_team_id_home = df_teams[df_teams['팀약어'] == compare_home_team]['팀ID'].values[0]
            data_home = df_games[(df_games['홈팀ID'] ==team_id) & (df_games['어웨이팀ID'] ==compare_team_id_home)]
            st.dataframe(data_home.iloc[:,[11,0,3,4,5,12,7,8,9,10]].sort_values('경기날짜',ascending=False))
            
            if data_home.empty == False :
                data_home = data_home.mean(numeric_only=None)
                data_home['어웨이승리'] = 1 - data_home['홈팀승리여부']
                fig_home = plt.figure()
                plt.subplot(2,2,1)
                plt.pie(data_home[[9,10]],autopct='%.1f',startangle = 90)
                plt.title('홈팀 승률')
                plt.legend(['홈','어웨이'])
                
                plt.subplot(2,2,2)
                plt.pie(data_home[[2,6]],autopct='%.1f',startangle=90)
                plt.title('평균 득점')
                plt.legend(['홈','어웨이'])

                plt.subplot(2,2,3)
                plt.pie(data_home[[3,7]],autopct='%.1f',startangle=90)
                plt.title('평균 어시')
                plt.legend(['홈','어웨이'])

                plt.subplot(2,2,4)
                plt.pie(data_home[[4,8]],autopct='%.1f',startangle=90)
                plt.title('평균 리바운드')
                plt.legend(['홈','어웨이'])
                st.pyplot(fig_home)
            else :
                st.title('실패')

        else : 
            st.error('팀을 선택해주세요')

        

        st.subheader('홈경기 선수 스탯')
        home_game_id = df_games_home['경기ID']
        home_team_player_info = df_games_detail[(df_games_detail['경기ID'].isin(home_game_id)) & (df_games_detail['팀ID'] == team_id)].iloc[:,3:].groupby('선수명').mean()
        st.dataframe(home_team_player_info)
    else :
        st.write('')


    st.subheader('어웨이 성적')
    df_games_away = df_games.loc[ (df_games['어웨이팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),:]
    st.dataframe(df_games_away.iloc[:,[11,12,0,3,4,5,7,8,9]])
    if st.checkbox('어웨이 성적 자세히 보기') :
        st.subheader('최근 대결 성적')
        fig2 = plt.figure()
        x= np.arange(3)
        x_label = ['점수','어시','리바운드']
        away_value2 = df_games_away.iloc[:,3:5+1].mean()
        away_value = df_games_away.iloc[:,7:-3].mean()
        p1=plt.bar(x,away_value,width = 0.4,color='g')
        p2=plt.bar(x+0.4,away_value2,width = 0.4,color='y')
        plt.xticks(np.arange(0.2,3+0.2,1),x_label)
        plt.legend((p1[0],p2[0]) , ('Away','Home'), fontsize = 10 )
        st.pyplot(fig2)
        st.dataframe(df_games_away.iloc[:,[3,4,5,7,8,9]].mean())
        st.subheader('역대 어웨이 전적비교')
        compare_away_team = st.selectbox('팀 선택',team_name_list)
        if compare_away_team != '' : 
            compare_team_id_away = df_teams[df_teams['팀약어'] == compare_away_team]['팀ID'].values[0]
            data_away=df_games[(df_games['홈팀ID'] ==team_id) & (df_games['어웨이팀ID'] ==compare_team_id_away)]
            st.dataframe(data_away.iloc[:,[11,0,3,4,5,12,7,8,9,10]].sort_values('경기날짜',ascending=False))

            if data_away.empty == False :
                data_away = data_away.mean(numeric_only=None)
                data_away['어웨이승리'] = 1 - data_home['홈팀승리여부']
                fig_away = plt.figure()
                plt.subplot(2,2,1)
                plt.pie(data_home[[10,9]],autopct='%.1f',startangle = 90)
                plt.title('어웨이팀 승률')
                plt.legend(['어웨이','홈'])
                
                plt.subplot(2,2,2)
                plt.pie(data_home[[6,2]],autopct='%.1f',startangle=90)
                plt.title('평균 득점')
                plt.legend(['어웨이','홈'])

                plt.subplot(2,2,3)
                plt.pie(data_home[[7,3]],autopct='%.1f',startangle=90)
                plt.title('평균 어시')
                plt.legend(['어웨이','홈'])

                plt.subplot(2,2,4)
                plt.pie(data_home[[8,4]],autopct='%.1f',startangle=90)
                plt.title('평균 리바운드')
                plt.legend(['어웨이','홈'])
                st.pyplot(fig_away)
            else :
                st.title('실패')

        else : 
            st.error('팀을 선택해주세요')


        st.subheader('어웨이경기 선수 스탯')
        home_away_id = df_games_away['경기ID']  
        away_team_player_info = df_games_detail[(df_games_detail['경기ID'].isin(home_away_id)) & (df_games_detail['팀ID'] == team_id)].iloc[:,3:].groupby('선수명').mean()
        st.dataframe(away_team_player_info)
    else :
        st.write('')

    

    

