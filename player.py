import streamlit as st
import data_init
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import platform
from matplotlib import font_manager, rc
def player(player_name) :
    plt.rcParams['axes.unicode_minus'] = False
    if platform.system() == 'Linux':
        rc('font', family='NanumGothic')
    elif platform.system() == 'Windows':
        path = "c:/Windows/Fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=path).get_name()
        rc('font', family=font_name)

    # 데이터를 읽어온다.
    # 선수 데이터
    df_players = data_init.df_players
    # 선수 스탯 데이터
    df_games_detail = data_init.df_games_detail
    # 팀정보
    df_team = data_init.df_teams
    # header
    st.header('선수 정보')
    # 선수명 확인
    player_list = df_players[df_players['선수명'].str.contains(player_name,case=False)]['선수명'].unique().tolist()
    if len(player_list) > 1 :
       
        st.error('중복되는 선수명을 가진 선수가 있습니다. 내역을 보시고 다시 입력해주세요.')
        player = pd.DataFrame(player_list,columns=['선수명'])
        st.dataframe(player)
    elif len(player_list) == 0 :
        st.error('등록된 선수가 없습니다. 다시 입력해주세요.')
    elif len(player_list) == 1 :
        player = player_list[0]
        # 플레이어 데이터 보여주기
        df_player = df_players[df_players['선수명'] == player]
        st.dataframe(df_player.iloc[:,[0,4,2,3]])

        # 스탯 조회하기
        # 선수 데이터 가져오기
        df_player_data = df_games_detail[df_games_detail['선수ID'] == df_player['선수ID'].unique()[0]].sort_values('경기날짜',ascending=False)
        # 1. 기간 선택하기
        st.subheader('선수 스탯 조회하기')
        radio_status = st.radio('검색',['날짜별','소속팀별'])
        if radio_status == '날짜별' :
            start_date = st.date_input('시작 날짜')
            end_date = st.date_input('종료 날짜')
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            
            if start_date > end_date :
                st.error('시작 날짜를 종료 날짜보다 전으로 설정해주세요.')
            else :
                if df_player_data['경기날짜'].values[0] < start_date :
                    st.error('경기정보가 없습니다.')
                else :
                    df_player_data_set=df_player_data[( df_player_data['경기날짜'] >= start_date ) & (df_player_data['경기날짜'] <= end_date) ]
                    
                    multiselectbox_list = ['상세','공격지표','수비지표']
                    selected_player_data = st.multiselect('데이터 선택',multiselectbox_list)
                    if '상세' in selected_player_data : 
                        st.dataframe(df_player_data_set.iloc[:,[15,16,3,4,5,6,7,8,9,10,11,12,13,14,]])
                    if '공격지표' in selected_player_data :
                        offense_data_date = df_player_data_set.iloc[:,[6,7,8,-2]]
                        
                        chart_offense_data_date = px.bar(offense_data_date,x='경기날짜',y=['2점슛','3점슛','자유투'] ,barmode='group')
                        st.plotly_chart(chart_offense_data_date)
                    
                    if '수비지표' in selected_player_data :
                        defense_data_date = df_player_data_set.iloc[:,[9,10,11,12,13,14,-2]]
                        
                        chart_defense_data_date = px.bar(defense_data_date,x='경기날짜',y=['리바운드','어시스트','가로채기','블락','턴오버','파울'] ,barmode='group')
                        st.plotly_chart(chart_defense_data_date)
                    

        
        elif radio_status =='소속팀별' :
            pass
