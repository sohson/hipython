import streamlit as st

st.title("KOSPI200 챗봇")

prompt = st.chat_input("질문 입력")

if prompt:
    st.write("질문:", prompt)