# 🏀프로젝트

## 프로젝트 개요
#### NBA 팀,선수 들의 데이터를 가져오는 NBA 데이터 센터를 Streamlit 을 이용하여 만들기.
###### - 선수별, 팀별 데이터 를 각각 날짜 또는 팀별로 구분하여 차트로 나타냅니다.
---

## 프로젝트 개발 과정
#### 1. kaggle 에서 무료 데이터를 가져왔습니다.
[NBA 데이터 다운로드](https://www.kaggle.com/datasets/nathanlauga/nba-games?resource=download&select=teams.csv)
### Jupyter 사용

#### 2. Jupyter notebook 을 통해 데이터를 가져와 이상이 없는지 확인합니다.
###### - 가져온 데이터에 밀림현상이 있어서 shift() 을 이용해 데이터를 재 가공합니다.

#### 3. 데이터의 컬럼을 분석하기 쉽게 전부 한글화를 진행하였습니다.
###### - rename()을 이용.

#### 4. 필요한 데이터를 가져오기 위해 데이터프레임들을 합치거나 삭제합니다.
###### - merge() , drop(axis=(0 or 1)) 을 이용

#### 5. 가공한 데이터프레임에서 원하는 정보를 가져와 차트로 만듭니다.
###### - plotly.express.bar() 사용

### Visual Studio Code 사용

#### 6. visual studio code 를 이용한 streamlit 라이브러리를 통해 웹대시보드의 설계를 구상합니다.

#### 7. 화면 구성에 필요한 image 들의 주소를 코드에 작성하여 이미지를 구성하도록 합니다.
###### - streamlit.image() 사용

#### 8. 구성에 위해 Jupyter 에서 작성한 코드들을 visual studio code 로 옮긴 다음 streamlit 을 이용하여 내가 원하는 대로 웹화면을 구성합니다.
###### - streamlit.dataframe() , radio(), text_input() 등등 사용

#### 9. local 에서 완성한 결과물을 EC2 서버에 업로드하여 정상적으로 작동하는지 확인합니다.
###### - 작동을 확인하던 도중 EC2가 다운되는 증상이 있었습니다. 원인을 분석해본 결과 games_detail와 teams를 merge를 통해 합치는 과정에서 데이터 용량이 너무 커서 서버가 다운되었습니다. 이에따라 games_detail의 데이터를 절반으로 조절하여 진항해였습니다.
---

## 사용환경 및 라이브러리
##### 환경
<img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=Windows&logoColor=white"> <img src="https://img.shields.io/badge/Amazon EC2-FF9900.svg?style=for-the-badge&logo=Amazon EC2&logoColor=white"/> <img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python3.8&logoColor=white"/> <img src="https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white"/> 

##### 라이브러리
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Streamlit-FF4B4B.svg?style=for-the-badge&logo=Streamlit&logoColor=white"/> <img src="https://img.shields.io/badge/pandas-150458.svg?style=for-the-badge&logo=pandas&logoColor=white"/> <img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style=for-the-badge&logo=Plotly&logoColor=white"/> <img src="https://img.shields.io/badge/NumPy-013243.svg?style=for-the-badge&logo=NumPy&logoColor=white"/>
---

## 프로젝트 주소
[EC2 프로젝트 확인](http://ec2-3-39-251-194.ap-northeast-2.compute.amazonaws.com:8501/)
---



