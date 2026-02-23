import streamlit as st

st.title('안녕하세요')
st.write('Hello Streamlit!') # 브라우저에 텍스트 출력

st.divider()

name = st.text_input('이름: ') # 사용자 입력을 받는 요소
st.write(name)

## 버튼

def bt1_click(): # 선) 정의
  st.write('그렇구나 잘했어')
st.write('')

btn1 = st.button('눌러주세요') # 후) 호출

if btn1 :
  #st.write('눌렀네?')
  bt1_click()


## 판다스 사용
import pandas as pd
df = pd.read_csv('./data/pew.csv')
# df.info()
print(df.info()) # log 출력하기
st.write(df.head())