import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ════════════════════════════════════════════════════════
# 페이지 설정
# ════════════════════════════════════════════════════════
st.set_page_config(
    page_title="신용카드 연체확률 예측 시스템",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════
# 글로벌 스타일
# ════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
* { font-family: 'Noto Sans KR', sans-serif !important; }

section[data-testid="stSidebar"] {
    background: #1e293b; padding-top: 12px;
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] label { font-size: 0.78rem !important; color:#94a3b8 !important; }
section[data-testid="stSidebar"] h3 {
    color:#f1f5f9 !important; font-size:0.9rem !important;
    border-bottom:1px solid #334155; padding-bottom:6px; margin:14px 0 8px;
}
section[data-testid="stSidebar"] .stButton > button {
    background: #ef4444; color: white; border: none;
    border-radius: 8px; font-weight: 700; font-size: 1rem;
    width: 100%; padding: 12px; margin-top: 12px;
}
section[data-testid="stSidebar"] .stButton > button:hover { background: #dc2626; }

.main .block-container { padding: 28px 36px; background: #f8fafc; }

.card {
    background: white; border-radius: 12px;
    padding: 20px 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-bottom: 16px; height: 100%;
}
.card-title { font-size:0.78rem; font-weight:700; color:#94a3b8; letter-spacing:0.05em; margin-bottom:6px; }
.big-metric { font-size:2.6rem; font-weight:700; color:#0f172a; line-height:1.1; }
.badge { display:inline-block; font-size:0.75rem; font-weight:700; padding:2px 10px; border-radius:999px; margin-top:8px; }
.badge-safe    { background:#dcfce7; color:#15803d; }
.badge-caution { background:#fef9c3; color:#a16207; }
.badge-warning { background:#ffedd5; color:#c2410c; }
.badge-danger  { background:#fee2e2; color:#b91c1c; }

.grade-card { border-radius:12px; padding:20px; text-align:center; font-weight:700; margin-bottom:16px; }
.grade-safe    { background:#f0fdf4; border:1.5px solid #86efac; }
.grade-caution { background:#fefce8; border:1.5px solid #fde047; }
.grade-warning { background:#fff7ed; border:1.5px solid #fdba74; }
.grade-danger  { background:#fef2f2; border:1.5px solid #fca5a5; }

.grade-dot { width:36px; height:36px; border-radius:50%; margin:0 auto 10px; box-shadow:0 2px 6px rgba(0,0,0,0.15); }
.dot-safe    { background:#22c55e; }
.dot-caution { background:#eab308; }
.dot-warning { background:#f97316; }
.dot-danger  { background:#ef4444; }
.grade-label { font-size:1.6rem; font-weight:700; margin-bottom:4px; }
.grade-sub   { font-size:0.78rem; color:#64748b; font-weight:400; }

.action-card { background:white; border-radius:12px; padding:20px 24px; box-shadow:0 1px 4px rgba(0,0,0,0.07); margin-bottom:16px; }
.action-label { font-size:0.78rem; color:#94a3b8; font-weight:500; margin-bottom:8px; }
.action-text  { font-size:1.05rem; font-weight:700; }
.action-safe    { color:#15803d; }
.action-caution { color:#a16207; }
.action-warning { color:#c2410c; }
.action-danger  { color:#b91c1c; }

.section-hd { font-size:0.88rem; font-weight:700; color:#475569; margin:4px 0 12px; }
.divider { border:none; border-top:1px solid #e2e8f0; margin:20px 0; }

.guide-box {
    background:white; border-radius:12px; padding:48px;
    text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.07);
}
.grade-table { width:100%; border-collapse:collapse; font-size:0.88rem; margin-top:8px; }
.grade-table th { background:#f1f5f9; color:#475569; padding:8px 14px; text-align:left; }
.grade-table td { padding:8px 14px; border-bottom:1px solid #f1f5f9; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# EX-01: 모델 파일 존재 확인
# ════════════════════════════════════════════════════════
MODEL_PATH = "./model/pipeline.pkl"

if not os.path.exists(MODEL_PATH):
    st.error("⛔ 모델 파일을 찾을 수 없습니다. `model/pipeline.pkl` 경로를 확인해주세요.")
    st.stop()

def preprocess(X):
    X = X.copy()
    X['EDUCATION'] = X['EDUCATION'].replace({0:4, 5:4, 6:4})
    X['MARRIAGE']  = X['MARRIAGE'].replace({0:3})
    return X

import __main__
__main__.preprocess = preprocess

import joblib

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

pipeline = load_model()

# ════════════════════════════════════════════════════════
# 상수 / 설정
# ════════════════════════════════════════════════════════
FEATURE_COLS = [
    'LIMIT_BAL','SEX','EDUCATION','MARRIAGE','AGE',
    'PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6',
    'BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6',
    'PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6',
]

VALID_RANGES = {
    'LIMIT_BAL':(10_000,1_000_000),'SEX':(1,2),'EDUCATION':(1,4),
    'MARRIAGE':(1,3),'AGE':(18,100),
    'PAY_0':(-1,9),'PAY_2':(-1,9),'PAY_3':(-1,9),
    'PAY_4':(-1,9),'PAY_5':(-1,9),'PAY_6':(-1,9),
    **{f'BILL_AMT{i}':(0,10_000_000) for i in range(1,7)},
    **{f'PAY_AMT{i}' :(0,10_000_000) for i in range(1,7)},
}

RISK_CONFIG = {
    'danger' :{'label':'위험','icon':'🔴','dot':'dot-danger', 'card':'grade-danger',
               'action_cls':'action-danger', 'badge':'badge-danger',
               'action':'한도 정지 / 추심 조치를 권장합니다.','color':'#ef4444'},
    'warning':{'label':'경고','icon':'🟠','dot':'dot-warning','card':'grade-warning',
               'action_cls':'action-warning','badge':'badge-warning',
               'action':'신용 한도 축소 검토를 권장합니다.','color':'#f97316'},
    'caution':{'label':'주의','icon':'🟡','dot':'dot-caution','card':'grade-caution',
               'action_cls':'action-caution','badge':'badge-caution',
               'action':'지속적인 모니터링이 필요합니다.','color':'#eab308'},
    'safe'   :{'label':'안전','icon':'🟢','dot':'dot-safe',  'card':'grade-safe',
               'action_cls':'action-safe',  'badge':'badge-safe',
               'action':'신용 한도 증액을 검토할 수 있습니다.','color':'#22c55e'},
}

def classify(prob):
    if prob >= 0.7:   return 'danger'
    elif prob >= 0.5: return 'warning'
    elif prob >= 0.3: return 'caution'
    else:             return 'safe'

def validate(d):
    missing = [k for k in FEATURE_COLS if d.get(k) is None]
    if missing:
        return False, f"EX-02 : 모든 항목을 입력해주세요. (누락: {', '.join(missing)})"
    for col,(lo,hi) in VALID_RANGES.items():
        if not (lo <= d[col] <= hi):
            return False, f"EX-03 : [{col}] 값 {d[col]}이(가) 유효 범위({lo}~{hi})를 벗어났습니다."
    return True, ""

# ════════════════════════════════════════════════════════
# 시각화
# ════════════════════════════════════════════════════════
def make_gauge(prob, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob * 100,
        number={'suffix':'%','font':{'size':38,'color':color}},
        gauge={
            'axis':{'range':[0,100],'tickwidth':1,'tickcolor':'#cbd5e1','tickfont':{'size':11}},
            'bar': {'color':color,'thickness':0.25},
            'bgcolor':'white',
            'steps':[
                {'range':[0,30],  'color':'#dcfce7'},
                {'range':[30,50], 'color':'#fefce8'},
                {'range':[50,70], 'color':'#fff7ed'},
                {'range':[70,100],'color':'#fef2f2'},
            ],
            'threshold':{'line':{'color':color,'width':3},'thickness':0.8,'value':prob*100},
            'shape':'angular',
        },
        title={'text':'연체 확률 (%)','font':{'size':13,'color':'#64748b'}},
    ))
    fig.update_layout(
        height=260, margin=dict(t=40,b=10,l=20,r=20),
        paper_bgcolor='white', font={'family':'Noto Sans KR'},
    )
    return fig

def make_grade_bar(current_key):
    grades = [('안전','#22c55e','safe'),('주의','#eab308','caution'),
              ('경고','#f97316','warning'),('위험','#ef4444','danger')]
    fig = go.Figure()
    for name, color, key in grades:
        h = 1.0 if key == current_key else 0.45
        fig.add_trace(go.Bar(
            x=[name], y=[h], marker_color=color, name=name,
            showlegend=True, marker_line_width=0,
        ))
    cur_name = next(g[0] for g in grades if g[2] == current_key)
    fig.add_annotation(x=cur_name, y=1.08, text='◀ 현재',
                       showarrow=False, font=dict(size=11, color='#334155'))
    fig.update_layout(
        height=220, margin=dict(t=40,b=10,l=0,r=0),
        paper_bgcolor='white', plot_bgcolor='white',
        yaxis=dict(visible=False, range=[0,1.25]),
        xaxis=dict(showgrid=False), barmode='group', bargap=0.3,
        legend=dict(orientation='h',yanchor='bottom',y=-0.28,xanchor='center',x=0.5,font=dict(size=11)),
        font={'family':'Noto Sans KR'},
    )
    return fig

# ════════════════════════════════════════════════════════
# 사이드바
# ════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 💳 고객 정보 입력")
    pay_opts = list(range(-1, 10))

    st.markdown("### 👤 기본 정보")
    limit_bal = st.number_input("신용한도", 10_000, 1_000_000, 200_000, step=10_000)
    sex       = st.selectbox("성별", [1,2], format_func=lambda x:"남(1)" if x==1 else "여(2)")
    education = st.selectbox("학력", [1,2,3,4],
                    format_func=lambda x:{1:"대학원",2:"대학교",3:"고등학교",4:"기타"}[x])
    marriage  = st.selectbox("결혼", [1,2,3],
                    format_func=lambda x:{1:"기혼",2:"미혼",3:"기타"}[x])
    age       = st.number_input("나이", 18, 100, 35)

    st.markdown("### 📅 납부 상태 (-1=정상, 1~9=연체월)")
    pay_0 = st.selectbox("9월 납부상태", pay_opts, index=1)
    pay_2 = st.selectbox("8월 납부상태", pay_opts, index=1)
    pay_3 = st.selectbox("7월 납부상태", pay_opts, index=1)
    pay_4 = st.selectbox("6월 납부상태", pay_opts, index=1)
    pay_5 = st.selectbox("5월 납부상태", pay_opts, index=1)
    pay_6 = st.selectbox("4월 납부상태", pay_opts, index=1)

    st.markdown("### 🧾 최근 6개월 청구금액 (원)")
    bill_amt1 = st.number_input("9월 청구액", 0, 10_000_000, 50_000, step=1_000)
    bill_amt2 = st.number_input("8월 청구액", 0, 10_000_000, 50_000, step=1_000)
    bill_amt3 = st.number_input("7월 청구액", 0, 10_000_000, 50_000, step=1_000)
    bill_amt4 = st.number_input("6월 청구액", 0, 10_000_000, 50_000, step=1_000)
    bill_amt5 = st.number_input("5월 청구액", 0, 10_000_000, 50_000, step=1_000)
    bill_amt6 = st.number_input("4월 청구액", 0, 10_000_000, 50_000, step=1_000)

    st.markdown("### 💰 최근 6개월 실제 납부금액 (원)")
    pay_amt1 = st.number_input("9월 납부액", 0, 10_000_000, 3_000, step=1_000)
    pay_amt2 = st.number_input("8월 납부액", 0, 10_000_000, 3_000, step=1_000)
    pay_amt3 = st.number_input("7월 납부액", 0, 10_000_000, 3_000, step=1_000)
    pay_amt4 = st.number_input("6월 납부액", 0, 10_000_000, 3_000, step=1_000)
    pay_amt5 = st.number_input("5월 납부액", 0, 10_000_000, 3_000, step=1_000)
    pay_amt6 = st.number_input("4월 납부액", 0, 10_000_000, 3_000, step=1_000)

    st.markdown("---")
    predict_btn = st.button("🔍 연체확률 예측", use_container_width=True)

# ════════════════════════════════════════════════════════
# 메인 헤더
# ════════════════════════════════════════════════════════
st.markdown("## 💳 신용카드 연체확률 예측 시스템")
st.markdown(
    "<p style='color:#94a3b8;font-size:0.85rem;margin-top:-12px;'>"
    "IOSF 설계 기반 · Pipeline: RFC + SMOTE · 입력변수 23개"
    "</p>", unsafe_allow_html=True
)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# 입력값 딕셔너리
# ════════════════════════════════════════════════════════
input_dict = {
    'LIMIT_BAL':limit_bal,'SEX':sex,'EDUCATION':education,'MARRIAGE':marriage,'AGE':age,
    'PAY_0':pay_0,'PAY_2':pay_2,'PAY_3':pay_3,'PAY_4':pay_4,'PAY_5':pay_5,'PAY_6':pay_6,
    'BILL_AMT1':bill_amt1,'BILL_AMT2':bill_amt2,'BILL_AMT3':bill_amt3,
    'BILL_AMT4':bill_amt4,'BILL_AMT5':bill_amt5,'BILL_AMT6':bill_amt6,
    'PAY_AMT1':pay_amt1,'PAY_AMT2':pay_amt2,'PAY_AMT3':pay_amt3,
    'PAY_AMT4':pay_amt4,'PAY_AMT5':pay_amt5,'PAY_AMT6':pay_amt6,
}

# ════════════════════════════════════════════════════════
# 예측 실행
# ════════════════════════════════════════════════════════
if predict_btn:

    valid, err_msg = validate(input_dict)
    if not valid:
        st.error(f"⚠️ {err_msg}")
        st.stop()

    try:
        X    = pd.DataFrame([input_dict])[FEATURE_COLS]
        prob = pipeline.predict_proba(X)[0][1]
        if not (0.0 <= prob <= 1.0):
            st.error("EX-04 : 예측에 실패했습니다. 입력값을 확인해주세요.")
            st.stop()
    except Exception as e:
        st.error(f"EX-05 : 서비스 오류가 발생했습니다. ({e})")
        st.stop()

    risk_key = classify(prob)
    cfg      = RISK_CONFIG[risk_key]
    pct      = prob * 100

    # Row 1
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card">
          <div class="card-title">연체 확률</div>
          <div class="big-metric">{pct:.1f}%</div>
          <span class="badge {cfg['badge']}">{cfg['icon']} {cfg['label']}</span>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="grade-card {cfg['card']}">
          <div class="grade-dot {cfg['dot']}"></div>
          <div class="grade-label">{cfg['label']}</div>
          <div class="grade-sub">위험 등급</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="action-card">
          <div class="action-label">권장 조치</div>
          <div class="action-text {cfg['action_cls']}">{cfg['action']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Row 2
    g1, g2 = st.columns(2)
    with g1:
        st.markdown('<div class="section-hd">📊 연체확률 게이지</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(prob, cfg['color']), use_container_width=True)
    with g2:
        st.markdown('<div class="section-hd">🎯 위험등급 현황</div>', unsafe_allow_html=True)
        st.plotly_chart(make_grade_bar(risk_key), use_container_width=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Row 3 — 입력 요약 탭
    st.markdown('<div class="section-hd">📋 입력 데이터 요약</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["👤 기본정보", "📅 납부상태", "🧾 청구금액", "💰 납부금액"])

    with tab1:
        st.dataframe(pd.DataFrame([{
            '신용한도':limit_bal,'성별':sex,'학력':education,'결혼':marriage,'나이':age
        }]).T.rename(columns={0:'입력값'}), use_container_width=True)

    with tab2:
        st.dataframe(pd.DataFrame([{
            'PAY_0(9월)':pay_0,'PAY_2(8월)':pay_2,'PAY_3(7월)':pay_3,
            'PAY_4(6월)':pay_4,'PAY_5(5월)':pay_5,'PAY_6(4월)':pay_6
        }]).T.rename(columns={0:'입력값'}), use_container_width=True)

    with tab3:
        st.dataframe(pd.DataFrame([{
            'BILL_AMT1(9월)':bill_amt1,'BILL_AMT2(8월)':bill_amt2,'BILL_AMT3(7월)':bill_amt3,
            'BILL_AMT4(6월)':bill_amt4,'BILL_AMT5(5월)':bill_amt5,'BILL_AMT6(4월)':bill_amt6
        }]).T.rename(columns={0:'입력값'}), use_container_width=True)

    with tab4:
        st.dataframe(pd.DataFrame([{
            'PAY_AMT1(9월)':pay_amt1,'PAY_AMT2(8월)':pay_amt2,'PAY_AMT3(7월)':pay_amt3,
            'PAY_AMT4(6월)':pay_amt4,'PAY_AMT5(5월)':pay_amt5,'PAY_AMT6(4월)':pay_amt6
        }]).T.rename(columns={0:'입력값'}), use_container_width=True)

# ════════════════════════════════════════════════════════
# 초기 안내
# ════════════════════════════════════════════════════════
else:
    st.markdown("""
    <div class="guide-box">
      <div style="font-size:2.8rem;margin-bottom:14px;">💳</div>
      <div style="font-size:1.15rem;font-weight:700;color:#334155;margin-bottom:8px;">
        고객 신용정보를 입력하고 예측 버튼을 눌러주세요
      </div>
      <div style="font-size:0.88rem;color:#94a3b8;">
        왼쪽 사이드바에서 23개 변수를 입력한 후 <b>🔍 연체확률 예측</b> 버튼을 클릭하세요
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-hd">📌 위험등급 기준</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="grade-table">
      <tr><th>등급</th><th>연체확률 구간</th><th>권장조치</th></tr>
      <tr><td>🔴 위험</td><td>p ≥ 70%</td><td>한도 정지 / 추심</td></tr>
      <tr><td>🟠 경고</td><td>50% ≤ p &lt; 70%</td><td>한도 축소 검토</td></tr>
      <tr><td>🟡 주의</td><td>30% ≤ p &lt; 50%</td><td>모니터링 필요</td></tr>
      <tr><td>🟢 안전</td><td>p &lt; 30%</td><td>한도 증액 가능</td></tr>
    </table>
    """, unsafe_allow_html=True)