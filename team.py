import streamlit as st
import pandas as pd
import team_url as tu
import data_init
import matplotlib.pyplot as plt
import numpy as np
import platform
from matplotlib import font_manager, rc
import plotly.express as px

def team(team_name) :
    
    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Linux':
        rc('font', family='NanumGothic')
    elif platform.system() == 'Windows':
        path = "c:/Windows/Fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)
    
    # 팀의 데이터를 읽어온다.
    df_teams = data_init.df_teams
    df_games = data_init.df_games
    df_games_detail = data_init.df_games_detail
    # 팀정보 헤더 지정
    st.header(team_name)
    # 팀의 맞는 이미지 생성
    st.subheader('로고')
    st.image(tu.team_url(team_name),width=500)
    # 사이드바에서 선택한 팀으로 정보
    st.subheader('정보')
    df_teams_info = df_teams.loc[df_teams['팀약어'] == team_name,'팀약어':]
    st.dataframe(df_teams_info)
    
    # 시즌별 성적보기
    st.header('일자별 성적보기')
    team_id = df_teams[df_teams['팀약어'] == team_name]['팀ID'].values[0]
    
    
    
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
    if df_games['경기날짜'][0] < start_date :
           st.error('경기정보가 없습니다. 날짜를 조정해주세요.')
           
    else :   
        # 홈 / 어웨이 선택
        selected = st.selectbox('홈/어웨이 선택',['홈','어웨이'])
        list_selected_box = ['상세','득점','어시스트','리바운드','역대전적','선수 스탯']       
        if selected == '홈' : 
            # 홈성적
            st.subheader('홈 성적')
            home_multi = st.multiselect('데이터 선택',list_selected_box)
            
            df_games_home = df_games.loc[ (df_games['홈팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),:]
            df_games_home = df_games_home.sort_values('경기날짜',ascending=False)    
            if '상세' in home_multi :
                st.subheader('상세')
                st.dataframe(df_games_home.iloc[:,[11,12,0,3,4,5,7,8,9]])

            if '득점' in home_multi :
                
                
                #득점 데이터
                st.subheader('득점')
                recently_game = st.slider('홈 경기 득점 경기 수',min_value=3,max_value=int(df_games_home['경기ID'].count()),value=7)
                recently_point_pig = px.bar(df_games_home.head(recently_game),x='경기날짜',y=['홈팀점수','어웨이팀점수'],barmode='group')
                st.plotly_chart(recently_point_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
            if '어시스트' in home_multi :
                #어시스트 데이터
                st.subheader('어시스트')
                recently_game = st.slider('홈 경기 어시스트 경기 수',min_value=3,max_value=int(df_games_home['경기ID'].count()),value=7)
                recently_assist_pig = px.bar(df_games_home.head(recently_game),x='경기날짜',y=['홈팀어시','어웨이팀어시'],barmode='group')
                st.plotly_chart(recently_assist_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
            if '리바운드' in home_multi :
                #리바운드 데이터
                st.subheader('리바운드')
                recently_game = st.slider('최근 경기 리바운드 경기 수',min_value=3,max_value=int(df_games_home['경기ID'].count()),value=7)
                recently_rebound_pig = px.bar(df_games_home.head(recently_game),x='경기날짜',y=['홈팀리바운드','어웨이팀리바운드'],barmode='group')
                st.plotly_chart(recently_rebound_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                
            if '역대전적' in home_multi:
                st.subheader('역대 홈 전적비교')
                compare_home_team = st.selectbox('팀선택',team_name_list)
                print(compare_home_team+' '+team_name)
                if compare_home_team != '' and compare_home_team != team_name : 
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
                        st.title('')
                elif compare_home_team == team_name :
                    st.error('같은 팀 입니다. 다른 팀을 선택해주세요.')
                else : 
                    st.error('팀을 선택해주세요')

                
            if '선수 스탯' in home_multi :
                st.subheader('홈경기 선수 스탯')
                home_game_id = df_games_home['경기ID']
                print(team_id)
                home_team_player_info = df_games_detail[(df_games_detail['경기ID'].isin(home_game_id)) & (df_games_detail['팀ID'] == team_id)].iloc[:,3:].groupby('선수명').mean()
                st.dataframe(home_team_player_info)
                st.info('선수의 자세한 스탯은 카테고리 - 선수 를 이용해주세요.')
            
            else :
                st.write('')

        elif selected =='어웨이' :

            st.subheader('어웨이 성적')
            away_multi = st.multiselect('데이터 선택',list_selected_box)
            
            df_games_away = df_games.loc[ (df_games['어웨이팀ID']==team_id) & (start_date<=df_games['경기날짜']) & (df_games['경기날짜']<=end_date),:]
            df_games_away = df_games_away.sort_values('경기날짜',ascending=False)  
            if '상세' in away_multi :
                st.subheader('상세')
                st.dataframe(df_games_away.iloc[:,[11,12,0,3,4,5,7,8,9]])
            if '득점' in away_multi :
                
                 #득점 데이터
                st.subheader('득점')
                recently_game = st.slider('어웨이 경기 득점 경기 수',min_value=3,max_value=int(df_games_away['경기ID'].count()),value=7)
                recently_point_pig = px.bar(df_games_away.head(recently_game),x='경기날짜',y=['홈팀점수','어웨이팀점수'],barmode='group')
                st.plotly_chart(recently_point_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
            if '어시스트' in away_multi :
                #어시스트 데이터
                st.subheader('어시스트')
                recently_game = st.slider('어웨이 경기 어시스트 경기 수',min_value=3,max_value=int(df_games_away['경기ID'].count()),value=7)
                recently_assist_pig = px.bar(df_games_away.head(recently_game),x='경기날짜',y=['홈팀어시','어웨이팀어시'],barmode='group')
                st.plotly_chart(recently_assist_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
            if '리바운드' in away_multi :    
                #리바운드 데이터
                st.subheader('리바운드')
                recently_game = st.slider('어웨이 경기 리바운드 경기 수',min_value=3,max_value=int(df_games_away['경기ID'].count()),value=7)
                recently_rebound_pig = px.bar(df_games_away.head(recently_game),x='경기날짜',y=['홈팀리바운드','어웨이팀리바운드'],barmode='group')
                st.plotly_chart(recently_rebound_pig)
                st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
           
            if '역대전적' in away_multi :
                st.subheader('역대 어웨이 전적비교')
                compare_away_team = st.selectbox('팀 선택',team_name_list)
            
                if compare_away_team != '' and compare_away_team != team_name: 
                    compare_team_id_away = df_teams[df_teams['팀약어'] == compare_away_team]['팀ID'].values[0]
                    data_away=df_games[(df_games['홈팀ID'] == compare_team_id_away) & (df_games['어웨이팀ID'] ==team_id)]
                    st.dataframe(data_away.iloc[:,[11,0,3,4,5,12,7,8,9,10]].sort_values('경기날짜',ascending=False))

                    if data_away.empty == False :
                        data_away = data_away.mean(numeric_only=None)
                        data_away['어웨이승리'] = 1 - data_away['홈팀승리여부']
                        fig_away = plt.figure()
                        plt.subplot(2,2,1)
                        plt.pie(data_away[[10,9]],autopct='%.1f',startangle = 90)
                        plt.title('어웨이팀 승률')
                        plt.legend(['어웨이','홈'])
                        
                        plt.subplot(2,2,2)
                        plt.pie(data_away[[6,2]],autopct='%.1f',startangle=90)
                        plt.title('평균 득점')
                        plt.legend(['어웨이','홈'])

                        plt.subplot(2,2,3)
                        plt.pie(data_away[[7,3]],autopct='%.1f',startangle=90)
                        plt.title('평균 어시')
                        plt.legend(['어웨이','홈'])

                        plt.subplot(2,2,4)
                        plt.pie(data_away[[8,4]],autopct='%.1f',startangle=90)
                        plt.title('평균 리바운드')
                        plt.legend(['어웨이','홈'])
                        st.pyplot(fig_away)
                    else :
                        st.title('')
                elif compare_away_team == team_name :
                    st.error('같은 팀 입니다. 다른 팀을 선택해주세요.')
                else : 
                    st.error('팀을 선택해주세요')

            if '선수 스탯' in away_multi :
                st.subheader('어웨이경기 선수 스탯')
                home_away_id = df_games_away['경기ID']  
                away_team_player_info = df_games_detail[(df_games_detail['경기ID'].isin(home_away_id)) & (df_games_detail['팀ID'] == team_id)].iloc[:,3:].groupby('선수명').mean()
                st.dataframe(away_team_player_info)
                st.info('선수의 자세한 스탯은 카테고리 - 선수 를 이용해주세요.')
            else :
                st.write('')

    

    

