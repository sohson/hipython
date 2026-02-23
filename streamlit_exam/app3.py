import streamlit as st
import pandas as pd
import numpy as np
import time

# -----------------------------------------------------------------------------
# 1. 페이지 설정 (친근한 아이콘과 제목)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="마이 샵 대시보드",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. 데이터 생성 (가상 데이터)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    dates = pd.date_range(start="2024-01-01", periods=30, freq="D")
    
    # 데이터 생성
    visitors = np.random.randint(500, 1500, size=30)         # 전체 방문자
    active_users = (visitors * np.random.uniform(0.3, 0.6, size=30)).astype(int) # 활성 사용자 (30~60%)
    revenue = np.random.randint(50, 200, size=30) * 10000    # 매출 (만원 단위)
    orders = np.random.randint(10, 50, size=30)              # 주문수
    
    data = pd.DataFrame({
        "날짜": dates,
        "방문자수": visitors,
        "활성사용자": active_users,
        "매출": revenue,
        "주문수": orders
    }).set_index("날짜")
    return data

df = load_data()

# -----------------------------------------------------------------------------
# 3. 사이드바 (메뉴)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🏡 마이 샵")
    st.write("오늘도 화이팅하세요! 💪")
    st.write("")
    
    # 메뉴 선택 (라디오 버튼 대신 보기 편한 형식)
    menu = st.radio(
        "메뉴 이동",
        ["🏠 홈 (대시보드)", "📈 상세 분석", "⚙️ 설정"],
        index=0
    )
    
    st.markdown("---")
    st.caption("내 가게 상태")
    # 딱딱한 텍스트 대신 상태바 활용
    st.success("영업 중 (온라인) 🟢")
    
    st.write("")
    # 프로필 카드 느낌
    with st.container(border=True):
        st.write("**김대표 님**")
        st.caption("Premium 플랜 사용 중")

# -----------------------------------------------------------------------------
# 4. 페이지별 구성
# -----------------------------------------------------------------------------

# [A] 홈 (대시보드) - 직관적이고 쉬운 요약
if menu == "🏠 홈 (대시보드)":
    
    # 1. 환영 문구 및 히어로 섹션
    col_text, col_img = st.columns([2, 1])
    
    with col_text:
        st.title("반갑습니다, 김대표님! 👋")
        st.write(f"오늘 날짜: {time.strftime('%Y년 %m월 %d일')}")
        st.write("")
        st.markdown("""
        > **💡 오늘의 꿀팁** > 주말에는 방문자가 평소보다 **20%** 더 많아요.  
        > 오늘 오후에 깜짝 이벤트를 준비해보는 건 어떨까요?
        """)
        
    with col_img:
        # 따뜻하고 편안한 느낌의 일러스트/사진 사용
        st.image(
            "https://images.unsplash.com/photo-1493612276216-ee3925520721?q=80&w=1000&auto=format&fit=crop",
            caption="오늘도 기분 좋은 하루 되세요!",
            use_container_width=True
        )

    st.divider()

    # 2. 핵심 지표 (카드 UI)
    st.subheader("한눈에 보는 오늘의 현황")
    
    # 4개의 지표를 나란히 배치
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # 어제 대비 변화량 계산
    today_vis = df["방문자수"].iloc[-1]
    diff_vis = int(today_vis - df["방문자수"].iloc[-2])
    
    today_rev = df["매출"].iloc[-1]
    diff_rev = int(today_rev - df["매출"].iloc[-2])

    today_ord = df["주문수"].iloc[-1]
    diff_ord = int(today_ord - df["주문수"].iloc[-2])

    # 보기 편한 카드 스타일
    with kpi1:
        st.metric(label="오늘 방문자", value=f"{today_vis}명", delta=f"{diff_vis}명")
    with kpi2:
        # 활성 사용자 비율 간단 계산
        active_rate = int((df["활성사용자"].iloc[-1] / today_vis) * 100)
        st.metric(label="실제 활동 유저", value=f"{active_rate}%", delta="양호", delta_color="off")
    with kpi3:
        st.metric(label="오늘 매출", value=f"{today_rev//10000}만원", delta=f"{diff_rev//10000}만")
    with kpi4:
        st.metric(label="주문 건수", value=f"{today_ord}건", delta=f"{diff_ord}건")

    # 3. 간단한 그래프 (복잡하지 않게)
    st.write("")
    st.write("")
    st.subheader("이번 달 방문자 흐름")
    # 부드러운 색상의 영역 차트
    st.area_chart(df["방문자수"], color="#80C080", height=250)


# [B] 상세 분석 - 방문자/활성 사용자 집중 분석
elif menu == "📈 상세 분석":
    st.title("📈 데이터 분석")
    st.markdown("우리 가게에 누가, 얼마나 오는지 자세히 살펴볼까요?")
    
    # 탭을 사용하여 정보를 깔끔하게 분리
    tab1, tab2 = st.tabs(["👥 방문자 & 활성 유저", "💰 매출 분석"])
    
    # 탭 1: 요청하신 방문자/활성 사용자 분석
    with tab1:
        st.subheader("방문자 vs 활성 사용자 비교")
        st.caption("💡 '활성 사용자'란 사이트에 들어와서 실제로 클릭하거나 활동한 사람을 말해요.")
        
        # 라인 차트로 두 데이터 비교
        chart_data = df[["방문자수", "활성사용자"]]
        st.line_chart(chart_data, color=["#E0E0E0", "#FF7F50"]) # 회색(전체), 주황색(활성)으로 강조
        
        # 상세 데이터 설명
        c1, c2 = st.columns(2)
        with c1:
            avg_active = int(df["활성사용자"].mean())
            st.info(f"이번 달 평균 활성 사용자는 **{avg_active}명** 입니다.")
        with c2:
            max_day = df["활성사용자"].idxmax().strftime("%m월 %d일")
            st.success(f"가장 활발했던 날은 **{max_day}** 입니다!")

        st.write("---")
        st.subheader("상세 데이터 표")
        st.dataframe(
            df[["방문자수", "활성사용자"]].sort_index(ascending=False),
            use_container_width=True,
            column_config={
                "방문자수": st.column_config.ProgressColumn(
                    "전체 방문자", format="%d명", min_value=0, max_value=2000
                ),
                "활성사용자": st.column_config.NumberColumn(
                    "활성 사용자", format="%d명"
                )
            }
        )

    # 탭 2: 매출 분석 (간단하게)
    with tab2:
        st.subheader("일별 매출 추이")
        st.bar_chart(df["매출"], color="#6495ED")
        st.write("매출이 꾸준히 발생하고 있어요. 주말 마케팅을 강화하면 더 좋을 것 같아요!")


# [C] 설정 - 어렵지 않은 옵션
elif menu == "⚙️ 설정":
    st.title("⚙️ 환경 설정")
    
    st.subheader("알림 받기")
    st.toggle("매일 아침 카카오톡으로 요약 받기", value=True)
    st.toggle("매출 목표 달성 시 알림", value=True)
    
    st.divider()
    
    st.subheader("화면 설정")
    theme = st.radio("테마 선택", ["밝은 모드 (기본)", "어두운 모드"], horizontal=True)
    
    st.divider()
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("캐시 삭제 및 새로고침"):
            st.cache_data.clear()
            st.toast("데이터를 새로 불러왔어요! 🍋")
            time.sleep(1)
            st.rerun()