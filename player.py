import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import platform
from matplotlib import font_manager, rc
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
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
    df_players = pd.read_csv('data/players.csv',index_col=0)
    # 선수 스탯 데이터
    df_games_detail = pd.read_csv('data/games_details.csv',low_memory = False,index_col=0)
   
    
    # header
    st.header('선수 정보')
    # 선수명 확인
    player_list = df_players[df_players['선수명'].str.contains(player_name,case=False)]['선수명'].unique().tolist()
    
    if len(player_list) > 1 :
       
        st.error('중복되는 선수명을 가진 선수가 있습니다. 내역을 보시고 다시 입력해주세요.')
        player = pd.DataFrame(sorted(player_list),columns=['선수명'])
        st.dataframe(player)
    elif len(player_list) == 0 :
        st.error('등록된 선수가 없습니다. 다시 입력해주세요.')
        st.subheader('등록된 선수 목록')
        all_player_list = sorted(df_players['선수명'].unique())
        st.dataframe(pd.DataFrame({'선수명':all_player_list}))
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
        if df_player_data.empty :
            st.error('해당 선수의 데이터가 없습니다.')
        else :
            radio_status = st.radio('검색',['날짜별','소속팀별'])
            if radio_status == '날짜별' :
                min_date = datetime.strptime(df_player_data['경기날짜'].tail(1).values[0],'%Y-%m-%d' )
                max_date = datetime.strptime(df_player_data['경기날짜'].head(1).values[0],'%Y-%m-%d' )
                start_date = st.date_input('시작 날짜',min_value=min_date,max_value=max_date,value=min_date)
                end_date = st.date_input('종료 날짜',min_value=min_date,max_value=max_date,value=max_date)
                start_date = start_date.strftime('%Y-%m-%d')
                end_date = end_date.strftime('%Y-%m-%d')
                
                if start_date > end_date :
                    st.error('시작 날짜를 종료 날짜보다 전으로 설정해주세요.')
                else :
                    
                    df_player_data_set=df_player_data[( df_player_data['경기날짜'] >= start_date ) & (df_player_data['경기날짜'] <= end_date) ]
                    if df_player_data_set.empty :
                        st.error('데이터가 없습니다.')
                    else :        
                        multiselectbox_list = ['상세','평균','2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울']
                        selected_player_data = st.multiselect('데이터 선택',multiselectbox_list)
                        
                        # 그 경기 선수 평균 가져오기 
                        list_game_id = df_player_data_set['경기ID']
                        game_player_mean = df_games_detail[(df_games_detail['경기ID'].isin(list_game_id)) & (df_games_detail['출전시간'].astype(str) > '1:00' )].groupby('경기날짜').mean().iloc[:,[0,3,4,5,6,7,8,9,10,11]]
                        game_player_mean=game_player_mean.sort_values('경기날짜',ascending=False)
                        # end

                        if '상세' in selected_player_data : 
                            st.subheader('상세정보')
                            st.dataframe(df_player_data_set.iloc[:,[15,16,3,4,5,6,7,8,9,10,11,12,13,14,]])
                        if '평균' in selected_player_data :    
                            st.subheader('평균')
                            fig = go.Figure([ go.Bar(x=['2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울'],
                                                    y = df_player_data_set.loc[:,['2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울']].mean()  ) ])
                            st.plotly_chart(fig)

                        
                        # 평균과 set 합치기
                        df_player_data_set = df_player_data_set.sort_values('경기날짜',ascending=False)
                        total_player_data = pd.merge(df_player_data_set,game_player_mean,on='경기ID')
                        rename_columns = { '2점슛_x' : '2점슛' , '3점슛_x' : '3점슛' , '자유투_x' :'자유투',
                                            '리바운드_x':'리바운드','어시스트_x':'어시스트', '가로채기_x' : '가로채기',
                                            '블락_x':'블락','턴오버_x':'턴오버','파울_x':'파울','2점슛_y':'경기평균2점',
                                            '3점슛_y':'경기평균3점','자유투_y':'경기평균자유투','리바운드_y':'경기평균리바운드',
                                            '어시스트_y':'경기평균어시스트','가로채기_y':'경기평균가로채기','블락_y':'경기평균블락',
                                            '턴오버_y':'경기평균턴오버','파울_y':'경기평균파울'}
                        total_player_data = total_player_data.rename(columns=rename_columns)
                        #수비,공격지표 설정
                        offense_data_date = total_player_data.loc[:,['경기날짜','2점슛','3점슛','리바운드','어시스트','자유투','경기평균2점','경기평균3점','경기평균자유투','경기평균리바운드', '경기평균어시스트']]
                        defense_data_date = total_player_data.loc[:,['경기날짜', '가로채기', '블락', '턴오버', '파울','경기평균가로채기', '경기평균블락','경기평균턴오버', '경기평균파울']]
                        if '2점슛' in selected_player_data :
                            
                            #2점슛
                            st.subheader('2점')
                            chart_offense_data_date_2_point = px.bar(offense_data_date,x='경기날짜',y=['2점슛','경기평균2점'] ,barmode='group')
                            st.plotly_chart(chart_offense_data_date_2_point)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '3점슛' in selected_player_data :    
                            # 3점슛
                            st.subheader('3점')
                            chart_offense_data_date_3_point = px.bar(offense_data_date,x='경기날짜',y=['3점슛','경기평균3점'] ,barmode='group')
                            st.plotly_chart(chart_offense_data_date_3_point)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '자유투' in selected_player_data :    
                            #자유투
                            st.subheader('자유투')
                            chart_offense_data_date_free_point = px.bar(offense_data_date,x='경기날짜',y=['자유투','경기평균자유투'] ,barmode='group')
                            st.plotly_chart(chart_offense_data_date_free_point)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '리바운드' in selected_player_data :    
                            #리바
                            st.subheader('리바운드')
                            chart_offense_data_date_re = px.bar(offense_data_date,x='경기날짜',y=['리바운드','경기평균리바운드'] ,barmode='group')
                            st.plotly_chart(chart_offense_data_date_re)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '어시스트' in selected_player_data :    
                            #어시
                            st.subheader('어시스트')
                            chart_offense_data_date_assist = px.bar(offense_data_date,x='경기날짜',y=['어시스트','경기평균어시스트'] ,barmode='group')
                            st.plotly_chart(chart_offense_data_date_assist)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')

                        if '가로채기' in selected_player_data :
                            
                            #가로채기
                            st.subheader('가로채기')
                            chart_defense_data_date_st = px.bar(defense_data_date,x='경기날짜',y=['가로채기','경기평균가로채기'] ,barmode='group')
                            st.plotly_chart(chart_defense_data_date_st)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '블락' in selected_player_data :   
                            #블락
                            st.subheader('블락')
                            chart_defense_data_date_bk = px.bar(defense_data_date,x='경기날짜',y=['블락','경기평균블락'] ,barmode='group')
                            st.plotly_chart(chart_defense_data_date_bk)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '턴오버' in selected_player_data :       
                            #턴오버
                            st.subheader('턴오버')
                            chart_defense_data_date_to = px.bar(defense_data_date,x='경기날짜',y=['턴오버','경기평균턴오버'] ,barmode='group')
                            st.plotly_chart(chart_defense_data_date_to)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                        if '파울' in selected_player_data :       
                            #파울
                            st.subheader('파울')
                            chart_defense_data_date_p = px.bar(defense_data_date,x='경기날짜',y=['파울','경기평균파울'] ,barmode='group')
                            st.plotly_chart(chart_defense_data_date_p)
                            st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
            
                
            elif radio_status =='소속팀별' :
                team_list = df_player_data['팀약어'].unique()
                choose_team =st.multiselect('팀선택',team_list)
                if len(choose_team) < 1 :
                    st.error('팀을 선택해주세요')
                else :
                    multiselectbox_list=st.multiselect('데이터 선택',['상세','평균','2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울'])

                    choose_team_player_data = df_player_data[df_player_data['팀약어'].isin(choose_team) ]
                    
                    # 그 경기 선수 평균 가져오기 
                    list_game_id = choose_team_player_data['경기ID']
                    game_player_mean = df_games_detail[(df_games_detail['경기ID'].isin(list_game_id)) & (df_games_detail['출전시간'].astype(str) > '1:00' )].groupby('경기날짜').mean().iloc[:,[0,3,4,5,6,7,8,9,10,11]]
                    game_player_mean=game_player_mean.sort_values('경기날짜',ascending=False)
                    # end

                    #상세
                    if '상세' in multiselectbox_list : 
                        st.subheader('상세정보')
                        st.dataframe(choose_team_player_data.iloc[:,[15,16,3,4,5,6,7,8,9,10,11,12,13,14,]])
                    if '평균' in multiselectbox_list :    
                        st.subheader('평균')
                        fig = go.Figure([ go.Bar(x=['2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울'],
                                                    y = choose_team_player_data.loc[:,['2점슛', '3점슛', '자유투', '리바운드', '어시스트', '가로채기', '블락', '턴오버', '파울']].mean()  ) ])
                        st.plotly_chart(fig)

                    choose_team_player_data = choose_team_player_data.sort_values('경기날짜',ascending=False)
                    
                    total_player_data = pd.merge(choose_team_player_data,game_player_mean,on='경기ID')
                    rename_columns = { '2점슛_x' : '2점슛' , '3점슛_x' : '3점슛' , '자유투_x' :'자유투',
                                        '리바운드_x':'리바운드','어시스트_x':'어시스트', '가로채기_x' : '가로채기',
                                        '블락_x':'블락','턴오버_x':'턴오버','파울_x':'파울','2점슛_y':'경기평균2점',
                                        '3점슛_y':'경기평균3점','자유투_y':'경기평균자유투','리바운드_y':'경기평균리바운드',
                                        '어시스트_y':'경기평균어시스트','가로채기_y':'경기평균가로채기','블락_y':'경기평균블락',
                                        '턴오버_y':'경기평균턴오버','파울_y':'경기평균파울'}
                    total_player_data = total_player_data.rename(columns=rename_columns)

                    #수비,공격지표 설정
                    offense_data_date = total_player_data.loc[:,['경기날짜','2점슛','3점슛','리바운드','어시스트','자유투','경기평균2점','경기평균3점','경기평균자유투','경기평균리바운드', '경기평균어시스트']]
                    defense_data_date = total_player_data.loc[:,['경기날짜', '가로채기', '블락', '턴오버', '파울','경기평균가로채기', '경기평균블락','경기평균턴오버', '경기평균파울']]

                    if '2점슛' in multiselectbox_list :
                            
                        #2점슛
                        st.subheader('2점')
                        slider_2=st.slider('최근 2점 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_offense_data_date_2_point = px.bar(offense_data_date.head(slider_2),x=np.arange(offense_data_date.head(slider_2).count()[0]),y=['2점슛','경기평균2점'] ,barmode='group',labels={'x':'경기수'})
                        
                        st.plotly_chart(chart_offense_data_date_2_point)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '3점슛' in multiselectbox_list :    
                        # 3점슛
                        st.subheader('3점')
                        slider_3=st.slider('최근 3점 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_offense_data_date_3_point = px.bar(offense_data_date.head(slider_3),x=np.arange(offense_data_date.head(slider_3).count()[0]),y=['3점슛','경기평균3점'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_offense_data_date_3_point)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '자유투' in multiselectbox_list :    
                        #자유투
                        st.subheader('자유투')
                        slider_f=st.slider('최근 자유투 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_offense_data_date_free_point = px.bar(offense_data_date.head(slider_f),x=np.arange(offense_data_date.head(slider_f).count()[0]),y=['자유투','경기평균자유투'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_offense_data_date_free_point)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '리바운드' in multiselectbox_list :    
                            #리바
                        st.subheader('리바운드')
                        slider_r=st.slider('최근 리바운드 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_offense_data_date_re = px.bar(offense_data_date.head(slider_r),x=np.arange(offense_data_date.head(slider_r).count()[0]),y=['리바운드','경기평균리바운드'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_offense_data_date_re)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '어시스트' in multiselectbox_list :    
                        #어시
                        st.subheader('어시스트')
                        slider_r=st.slider('최근 어시 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_offense_data_date_assist = px.bar(offense_data_date.head(slider_r),x=np.arange(offense_data_date.head(slider_r).count()[0]),y=['어시스트','경기평균어시스트'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_offense_data_date_assist)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')

                    if '가로채기' in multiselectbox_list :
                        
                        #가로채기
                        st.subheader('가로채기')
                        slider_s=st.slider('최근 가로채기 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_defense_data_date_st = px.bar(defense_data_date.head(slider_s),x=np.arange(offense_data_date.head(slider_s).count()[0]),y=['가로채기','경기평균가로채기'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_defense_data_date_st)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '블락' in multiselectbox_list :   
                        #블락
                        st.subheader('블락')
                        slider_b=st.slider('최근 블락 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_defense_data_date_bk = px.bar(defense_data_date.head(slider_b),x=np.arange(offense_data_date.head(slider_b).count()[0]),y=['블락','경기평균블락'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_defense_data_date_bk)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '턴오버' in multiselectbox_list :       
                        #턴오버
                        st.subheader('턴오버')
                        slider_t=st.slider('최근 턴오버 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_defense_data_date_to = px.bar(defense_data_date.head(slider_t),x=np.arange(offense_data_date.head(slider_t).count()[0]),y=['턴오버','경기평균턴오버'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_defense_data_date_to)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
                    if '파울' in multiselectbox_list :       
                        #파울
                        st.subheader('파울')
                        slider_p=st.slider('최근 파울 데이터 경기수를 지정해주세요.',min_value= 5 , max_value=int(offense_data_date.count()[0]) , value= 10)
                        chart_defense_data_date_p = px.bar(defense_data_date.head(slider_p),x=np.arange(offense_data_date.head(slider_p).count()[0]),y=['파울','경기평균파울'] ,barmode='group',labels={'x':'경기수'})
                        st.plotly_chart(chart_defense_data_date_p)
                        st.info('자세히 보고싶은 부분을 좌클릭으로 영역 지정 해주세요.')
        




        
                

            

