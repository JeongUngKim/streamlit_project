import streamlit as st
import data_init
def home() :
    st.title('NBA 데이터 센터에 오신걸 환영합니다.')
    st.header('푸티테스트')
    image_url = 'https://mblogthumb-phinf.pstatic.net/MjAxOTA2MTNfMjkw/MDAxNTYwMzkyODk3MDQ0._UQzxFUpS-lLFTg5FX4nsP6o9WxKBVB1IlEAoo3Scz8g.50FBo4vY3wwoXSPk2-Pzt5mP_mM_gx8n2HsbZ7ZR7Lkg.PNG.swmh69/nba_%EB%A1%9C%EA%B3%A0.png?type=w800'
    st.image(image_url)
    st.subheader('')

    st.subheader('프로젝트 안내사항')
    st.text('kaggle 에 NBA 데이터를 이용하였습니다.')
    st.write("[kaggle nba data 바로가기](https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download&select=teams.csv)")
    st.text('사용한 데이터는 다음과 같습니다.')
    st.text('teams')
    st.dataframe(data_init.df_teams.head())
    st.text('players')
    st.dataframe(data_init.df_players.head())
    st.text('games')
    st.dataframe(data_init.df_games.head())
    st.text('games_detail')
    st.dataframe(data_init.df_games_detail.head())
    st.error('games_details 에 데이터용량이 프리티어 버전 EC2서버에서 이용하기에는 너무 커 절반만 사용하였습니다.')

    
    

    