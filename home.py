import streamlit as st
import data_init
def home() :
    st.title('NBA 데이터 센터에 오신걸 환영합니다.')
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

    st.subheader('개선점')
    st.text('데이터의 밀림 현상이 있어 수정을 진행하였고,')
    st.text('선수의 정보를 입력하면 포지션을 알려주는 머신러닝을 개발하고 싶었으나')
    st.text('받아온 데이터가 비어있는 경우도 많았고 있는 데이터에서는 각 포지션별로 편차가 크지 않아')
    st.text('머신러닝을 사용하기에는 부적합하다고 판단하였습니다. ')
    
    
    

    