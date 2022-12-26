import streamlit as st
import pandas as pd
def home() :
    st.title('NBA 데이터 센터에 오신걸 환영합니다.')
    
    image_url = 'https://mblogthumb-phinf.pstatic.net/MjAxOTA2MTNfMjkw/MDAxNTYwMzkyODk3MDQ0._UQzxFUpS-lLFTg5FX4nsP6o9WxKBVB1IlEAoo3Scz8g.50FBo4vY3wwoXSPk2-Pzt5mP_mM_gx8n2HsbZ7ZR7Lkg.PNG.swmh69/nba_%EB%A1%9C%EA%B3%A0.png?type=w800'
    st.image(image_url)
    st.subheader('')

    st.subheader('프로젝트 안내사항')
    st.text('kaggle 에 NBA 데이터를 이용하였습니다.')
    st.write("[kaggle nba data 바로가기](https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download&select=teams.csv)")
    st.text('사용한 데이터는 다음과 같습니다.')
    df_teams = pd.read_csv('data/teams.csv',index_col=0)
    df_games = pd.read_csv('data/games.csv',index_col=0)
    df_games_detail = pd.read_csv('data/games_details.csv',low_memory = False,index_col=0)
    st.text('teams')
    
    st.dataframe(df_teams.head())
    st.text('players')
   
    st.dataframe(df_players.head())
    st.text('games')
    
    st.dataframe(df_games.head())
    st.text('games_details')
    
    st.dataframe(df_games_detail.head())
    st.error('games_details 에 데이터용량이 프리티어 버전 EC2서버에서 이용하기에는 너무 커 절반만 사용하였습니다.')

    
    

    