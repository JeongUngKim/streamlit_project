import streamlit as st

def home() :
    st.title('NBA 데이터 센터에 오신걸 환영합니다.')
    image_url = 'https://mblogthumb-phinf.pstatic.net/MjAxOTA2MTNfMjkw/MDAxNTYwMzkyODk3MDQ0._UQzxFUpS-lLFTg5FX4nsP6o9WxKBVB1IlEAoo3Scz8g.50FBo4vY3wwoXSPk2-Pzt5mP_mM_gx8n2HsbZ7ZR7Lkg.PNG.swmh69/nba_%EB%A1%9C%EA%B3%A0.png?type=w800'
    st.image(image_url)
    st.subheader('')
    st.subheader('사용방법')
    st.text('왼쪽 사이드바에서 보고싶은 팀 또는 선수를 선택하세요.')

    