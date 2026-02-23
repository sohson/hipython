import streamlit as st

def main():
    # 페이지 기본 설정 
    st.set_page_config(page_title="환경 대시보드", layout="centered")

    # 대시보드 제목
    st.title("🌿 환경 상태 미니 대시보드")
    st.markdown("---")

    # 1. 레이아웃 분할 (가로로 2개)
    col1, col2 = st.columns(2)

    # 2. 첫 번째 컬럼: 온도 (오늘의 날씨)
    with col1:
        # delta="3" -> 양수이므로 기본적으로 초록색 표시
        st.metric(
            label="오늘의 날씨",
            value="35도",
            delta="3",
            delta_color="normal" 
        )

    # 3. 두 번째 컬럼: 공기질 (오늘의 미세먼지)
    with col2:
        # delta="-30" -> 음수지만 미세먼지는 줄어들수록 좋으므로
        # delta_color="inverse"를 사용하여 음수일 때 초록색이 나오도록 설정
        st.metric(
            label="오늘의 미세먼지",
            value="좋음",
            delta="-30",
            delta_color="inverse"
        )

if __name__ == "__main__":
    main()