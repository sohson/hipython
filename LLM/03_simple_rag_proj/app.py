import streamlit as st
from rag_chain import build_rag_chain

st.set_page_config(
    page_title="Samsung Memory Assistant",
    page_icon="💾",
    layout="centered",
)

# ── Samsung Design System CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=Bebas+Neue&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #F4F6FB !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* Main container */
.main .block-container {
    max-width: 800px !important;
    padding: 0 0 100px 0 !important;
    margin: 0 auto !important;
}

/* ── HEADER ── */
.samsung-header {
    background: #1428A0;
    padding: 16px 36px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 0;
}
.samsung-wordmark {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 24px;
    letter-spacing: 5px;
    color: #fff;
    line-height: 1;
}
.header-sep {
    width: 1px; height: 20px;
    background: rgba(255,255,255,0.28);
}
.header-sub {
    font-size: 12.5px;
    font-weight: 300;
    color: rgba(255,255,255,0.65);
    letter-spacing: 0.3px;
}
.header-pill {
    margin-left: auto;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 100px;
    padding: 3px 11px;
    font-size: 10.5px;
    font-weight: 500;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.8);
}

/* ── WELCOME CARD ── */
.welcome-card {
    margin: 28px 36px 0;
    background: linear-gradient(130deg, #1428A0 0%, #1E38D4 60%, #2548E8 100%);
    border-radius: 20px;
    padding: 30px 32px;
    color: #fff;
    position: relative;
    overflow: hidden;
}
.welcome-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 160px; height: 160px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.welcome-card::after {
    content: '';
    position: absolute;
    bottom: -30px; left: 60px;
    width: 100px; height: 100px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.wc-eyebrow {
    font-size: 10px; font-weight: 600;
    letter-spacing: 2.5px; text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 8px;
}
.wc-title {
    font-size: 20px; font-weight: 600;
    color: #fff; margin-bottom: 8px;
    line-height: 1.35;
}
.wc-desc {
    font-size: 13.5px; font-weight: 300;
    color: rgba(255,255,255,0.68);
    line-height: 1.7;
}

/* ── CHIPS ── */
.chips-wrap {
    margin: 20px 36px 0;
}
.chips-eyebrow {
    font-size: 10px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase;
    color: #9298B8;
    margin-bottom: 10px;
}
.chips-row {
    display: flex; flex-wrap: wrap; gap: 8px;
}
.chip {
    background: #fff;
    border: 1.5px solid #D2D7EE;
    border-radius: 100px;
    padding: 7px 15px;
    font-size: 13px; font-weight: 500;
    color: #1428A0;
    cursor: pointer;
    transition: all 0.16s ease;
    white-space: nowrap;
    font-family: 'DM Sans', sans-serif;
}
.chip:hover {
    background: #1428A0;
    color: #fff;
    border-color: #1428A0;
    transform: translateY(-1px);
    box-shadow: 0 5px 14px rgba(20,40,160,0.22);
}

/* ── MESSAGES ── */
.msg-area {
    padding: 24px 36px;
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.msg-row {
    display: flex;
    gap: 11px;
    align-items: flex-end;
    animation: riseIn 0.28s ease;
}
@keyframes riseIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user-row { flex-direction: row-reverse; }

.av {
    width: 34px; height: 34px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    font-size: 13px;
}
.av-ai {
    background: #1428A0; color: #fff;
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 1px;
    font-size: 12px;
}
.av-user {
    background: #E4E8F7;
    font-size: 15px;
}

.bubble {
    max-width: 78%;
    padding: 13px 17px;
    font-size: 14.5px;
    font-weight: 400;
    line-height: 1.68;
}
.bubble-ai {
    background: #fff;
    color: #1A1C2E;
    border-radius: 4px 16px 16px 16px;
    border: 1px solid #E0E4F0;
    box-shadow: 0 2px 14px rgba(20,40,160,0.07);
}
.bubble-user {
    background: #1428A0;
    color: #fff;
    border-radius: 16px 4px 16px 16px;
}

/* ── THINKING ── */
.thinking {
    display: flex; gap: 11px; align-items: flex-end;
    margin: 0 36px;
    animation: riseIn 0.28s ease;
}
.dots {
    background: #fff;
    border: 1px solid #E0E4F0;
    border-radius: 4px 16px 16px 16px;
    padding: 14px 20px;
    display: flex; gap: 5px; align-items: center;
    box-shadow: 0 2px 14px rgba(20,40,160,0.07);
}
.dot {
    width: 7px; height: 7px;
    background: #1428A0;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: 0.15s; }
.dot:nth-child(3) { animation-delay: 0.30s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.35; }
    40%            { transform: translateY(-6px); opacity: 1; }
}

/* ── INPUT BAR ── */
[data-testid="stChatInput"] > div {
    border: 2px solid #D2D7EE !important;
    border-radius: 14px !important;
    background: #fff !important;
    box-shadow: 0 2px 18px rgba(20,40,160,0.09) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: #1428A0 !important;
    box-shadow: 0 4px 22px rgba(20,40,160,0.16) !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    color: #1A1C2E !important;
}
[data-testid="stChatInput"] button {
    background: #1428A0 !important;
    border-radius: 9px !important;
    color: #fff !important;
}
[data-testid="stChatInputContainer"] {
    padding: 12px 36px 20px !important;
    background: #F4F6FB !important;
}

/* Stale button hide (chip dummy buttons) */
.stButton > button {
    display: none !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #C5CBE8; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── RAG chain ─────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="매뉴얼을 불러오는 중입니다...")
def get_chain():
    return build_rag_chain()

rag_chain = get_chain()

# ── State ─────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chip_query" not in st.session_state:
    st.session_state.chip_query = None
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="samsung-header">
    <span class="samsung-wordmark">SAMSUNG</span>
    <div class="header-sep"></div>
    <span class="header-sub">Memory Card Manual Assistant</span>
    <span class="header-pill">AI Powered</span>
</div>
""", unsafe_allow_html=True)

# ── Welcome + chips (no messages yet) ────────────────────────────────────────
CHIPS = [
    "동시에 몇 개의 메모리카드나 UFD를 인식할 수 있나요?",
    "BitLocker가 활성화된 메모리카드도 인증할 수 있나요?",
    "인증 결과가 정확하게 나오지 않는 원인 세 가지를 알려주세요.",
    "지원하는 파일 시스템은 무엇인가요?",
]
CHIP_LABELS = [
    "💾 동시 인식 가능한 장치 수",
    "🔒 BitLocker 메모리카드 인증",
    "⚠️ 인증 오류 주요 원인",
    "📋 지원 파일 시스템",
]

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <div class="wc-eyebrow">Samsung Memory Solutions</div>
        <div class="wc-title">메모리카드 매뉴얼 AI 어시스턴트</div>
        <div class="wc-desc">
            삼성 메모리카드 공식 매뉴얼을 기반으로 정확한 정보를 제공합니다.<br>
            호환성·사양·인증·문제 해결 등 무엇이든 질문해 보세요.
        </div>
    </div>
    <div class="chips-wrap">
        <div class="chips-eyebrow">자주 묻는 질문</div>
        <div class="chips-row">
            <span class="chip">💾 동시 인식 가능한 장치 수</span>
            <span class="chip">🔒 BitLocker 메모리카드 인증</span>
            <span class="chip">⚠️ 인증 오류 주요 원인</span>
            <span class="chip">📋 지원 파일 시스템</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Real invisible Streamlit buttons behind chips
    cols = st.columns(4)
    for i, col in enumerate(cols):
        with col:
            if st.button(CHIP_LABELS[i], key=f"chip_{i}"):
                st.session_state.chip_query = CHIPS[i]
                st.rerun()

# ── Message history ───────────────────────────────────────────────────────────
if st.session_state.messages:
    st.markdown('<div class="msg-area">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "assistant":
            st.markdown(f"""
            <div class="msg-row">
                <div class="av av-ai">AI</div>
                <div class="bubble bubble-ai">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row user-row">
                <div class="av av-user">👤</div>
                <div class="bubble bubble-user">{msg["content"]}</div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("메모리카드에 대해 무엇이든 질문하세요...")

# Chip → input 처리
if st.session_state.chip_query:
    user_input = st.session_state.chip_query
    st.session_state.chip_query = None

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user bubble immediately + thinking animation
    st.markdown('<div class="msg-area">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="msg-row user-row">
        <div class="av av-user">👤</div>
        <div class="bubble bubble-user">{user_input}</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div class="thinking">
        <div class="av av-ai">AI</div>
        <div class="dots">
            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    answer = rag_chain.invoke(user_input)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()