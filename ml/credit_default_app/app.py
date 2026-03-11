# app.py
import streamlit as st
from predict import predict

# ── 페이지 설정
st.set_page_config(page_title='채무불이행 예측', layout='wide')
st.title('💳 신용카드 채무불이행 고객 예측')

# ════════════════════════════════
# 사이드바 — 고객 정보 입력
# ════════════════════════════════
st.sidebar.header('고객 정보 입력')

limit_bal = st.sidebar.number_input('신용한도 (LIMIT_BAL)', 10000, 1000000, 200000, step=10000)
sex       = st.sidebar.selectbox('성별 (SEX)', [1, 2], format_func=lambda x: '남(1)' if x==1 else '여(2)')
education = st.sidebar.selectbox('학력 (EDUCATION)', [1,2,3,4],
                format_func=lambda x: {1:'대학원',2:'대학교',3:'고등학교',4:'기타'}[x])
marriage  = st.sidebar.selectbox('결혼 (MARRIAGE)', [1,2,3],
                format_func=lambda x: {1:'기혼',2:'미혼',3:'기타'}[x])
age       = st.sidebar.slider('나이 (AGE)', 21, 79, 35)

st.sidebar.subheader('납부 상태 (PAY)')
st.sidebar.caption('-2=소비없음  /  -1=정상납부  /  0=리볼빙  /  1~8=연체 개월 수')
pay_0 = st.sidebar.slider('PAY_0 (최근달)', -2, 8, 0)
pay_2 = st.sidebar.slider('PAY_2', -2, 8, 0)
pay_3 = st.sidebar.slider('PAY_3', -2, 8, 0)
pay_4 = st.sidebar.slider('PAY_4', -2, 8, 0)
pay_5 = st.sidebar.slider('PAY_5', -2, 8, 0)
pay_6 = st.sidebar.slider('PAY_6', -2, 8, 0)

st.sidebar.subheader('청구금액 (BILL_AMT)')
bill_amt1 = st.sidebar.number_input('BILL_AMT1', -500000, 2000000, 50000, step=1000)
bill_amt2 = st.sidebar.number_input('BILL_AMT2', -500000, 2000000, 50000, step=1000)
bill_amt3 = st.sidebar.number_input('BILL_AMT3', -500000, 2000000, 50000, step=1000)
bill_amt4 = st.sidebar.number_input('BILL_AMT4', -500000, 2000000, 50000, step=1000)
bill_amt5 = st.sidebar.number_input('BILL_AMT5', -500000, 2000000, 50000, step=1000)
bill_amt6 = st.sidebar.number_input('BILL_AMT6', -500000, 2000000, 50000, step=1000)

st.sidebar.subheader('납부금액 (PAY_AMT)')
pay_amt1 = st.sidebar.number_input('PAY_AMT1', 0, 2000000, 3000, step=1000)
pay_amt2 = st.sidebar.number_input('PAY_AMT2', 0, 2000000, 3000, step=1000)
pay_amt3 = st.sidebar.number_input('PAY_AMT3', 0, 2000000, 3000, step=1000)
pay_amt4 = st.sidebar.number_input('PAY_AMT4', 0, 2000000, 3000, step=1000)
pay_amt5 = st.sidebar.number_input('PAY_AMT5', 0, 2000000, 3000, step=1000)
pay_amt6 = st.sidebar.number_input('PAY_AMT6', 0, 2000000, 3000, step=1000)

threshold = st.sidebar.slider('분류 임계값 (Threshold)', 0.1, 0.9, 0.5, 0.05)

# ════════════════════════════════
# 예측 실행
# ════════════════════════════════
input_dict = {
    'LIMIT_BAL':limit_bal, 'SEX':sex, 'EDUCATION':education,
    'MARRIAGE':marriage,   'AGE':age,
    'PAY_0':pay_0, 'PAY_2':pay_2, 'PAY_3':pay_3,
    'PAY_4':pay_4, 'PAY_5':pay_5, 'PAY_6':pay_6,
    'BILL_AMT1':bill_amt1, 'BILL_AMT2':bill_amt2, 'BILL_AMT3':bill_amt3,
    'BILL_AMT4':bill_amt4, 'BILL_AMT5':bill_amt5, 'BILL_AMT6':bill_amt6,
    'PAY_AMT1':pay_amt1,   'PAY_AMT2':pay_amt2,   'PAY_AMT3':pay_amt3,
    'PAY_AMT4':pay_amt4,   'PAY_AMT5':pay_amt5,   'PAY_AMT6':pay_amt6,
}

result = predict(input_dict, threshold=threshold)
prob   = result['probability']

# ════════════════════════════════
# 메인 화면 — 결과 출력
# ════════════════════════════════
col1, col2, col3 = st.columns(3)
col1.metric('채무불이행 확률', f"{prob*100:.1f}%")
col2.metric('예측 결과', result['label'])
col3.metric('적용 임계값', threshold)

# 위험도 게이지 바
color = 'tomato' if result['prediction'] == 1 else 'steelblue'
st.markdown(f"""
<div style='background:#eee; border-radius:8px; height:28px; margin:16px 0'>
  <div style='background:{color}; width:{prob*100:.1f}%; height:28px; border-radius:8px;
              text-align:center; color:white; line-height:28px; font-weight:bold'>
    {prob*100:.1f}%
  </div>
</div>
""", unsafe_allow_html=True)

# 입력값 요약 테이블
st.subheader('입력값 요약')
import pandas as pd
st.dataframe(pd.DataFrame([input_dict]).T.rename(columns={0:'입력값'}))