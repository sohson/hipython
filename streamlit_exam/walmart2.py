import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="Walmart 매출 최적화 전략 대시보드",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 48px;
        font-weight: bold;
        color: #2c3e50;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin: 30px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

# 데이터 로드
# 데이터 로드
@st.cache_data
def load_data():
    import os
    
    # 가능한 경로들 시도
    possible_paths = [
        './data/walmart.csv',
        'walmart.csv',
        '../data/walmart.csv',
        './walmart.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
            for encoding in encodings:
                try:
                    df = pd.read_csv(path, encoding=encoding)
                    df.columns = df.columns.str.strip().str.replace("'", "")
                    st.success(f"✅ 파일 로드 성공: {path}")
                    return df
                except:
                    continue
    
    # 파일을 찾지 못한 경우
    st.error("❌ CSV 파일을 찾을 수 없습니다.")
    st.info("📁 walmart.csv 파일을 다음 위치 중 하나에 놓아주세요:")
    st.code("\n".join(possible_paths))
    st.stop()

# 데이터 전처리
@st.cache_data
def preprocess_data(df):
    # 제품별 집계
    product_agg = df.groupby('Product_ID').agg({
        'Purchase': ['sum', 'mean', 'count']
    }).reset_index()
    product_agg.columns = ['Product_ID', 'Total_Sales', 'Avg_Price', 'Volume']
    product_agg = product_agg.sort_values('Total_Sales', ascending=False)
    
    # 누적 비율
    product_agg['Cumulative_Sales'] = product_agg['Total_Sales'].cumsum()
    product_agg['Sales_Ratio'] = product_agg['Cumulative_Sales'] / product_agg['Total_Sales'].sum()
    product_agg['Product_Rank_Ratio'] = np.arange(1, len(product_agg) + 1) / len(product_agg)
    
    # 가격 세그먼트
    p33, p67 = product_agg['Avg_Price'].quantile([0.33, 0.67])
    product_agg['Price_Segment'] = pd.cut(
        product_agg['Avg_Price'],
        bins=[0, p33, p67, np.inf],
        labels=['Low Price', 'Medium Price', 'High Price']
    )
    
    return df, product_agg

# 메인 실행
try:
    df = load_data()
    df_original, product_agg = preprocess_data(df)
    
except Exception as e:
    st.error(f"❌ 오류 발생: {str(e)}")
    st.info("💡 Tip: CSV 파일이 './data/walmart.csv' 경로에 있는지 확인하세요.")
    st.stop()

# 사이드바
with st.sidebar:
    st.markdown("## 🛒 Walmart")
    st.markdown("### 매출 최적화 전략")
    st.markdown("---")
    
    st.markdown("### 📊 필터 옵션")
    price_filter = st.multiselect(
        "가격 세그먼트",
        options=['High Price', 'Medium Price', 'Low Price'],
        default=['High Price', 'Medium Price', 'Low Price']
    )
    
    top_n = st.slider("Top N 카테고리", 5, 20, 10, 1)
    
    st.markdown("---")
    st.markdown("### 📌 핵심 인사이트")
    st.info("✅ 상위 20% 제품 → 73.3% 매출")
    st.success("✅ 고가 제품군 → 50.3% 매출")
    st.warning("✅ Cat 1+5+8 → 97% 동시구매")

# 메인 대시보드
st.title("🛒 Walmart 매출 최적화 전략 대시보드")
st.markdown("---")

# KPI 섹션
st.markdown('<div class="section-header">Executive Summary - 핵심 성과 지표</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

total_sales = df['Purchase'].sum()
avg_price = df['Purchase'].mean()
top_20_ratio = product_agg.head(int(len(product_agg)*0.2))['Total_Sales'].sum() / product_agg['Total_Sales'].sum() * 100
high_price_ratio = product_agg[product_agg['Price_Segment']=='High Price']['Total_Sales'].sum() / product_agg['Total_Sales'].sum() * 100

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">총 매출</div>
        <div class="metric-value">{total_sales/1e9:.2f}B</div>
        <div style="color: #27ae60; font-size: 14px;">↑ $</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">평균 객단가</div>
        <div class="metric-value">{avg_price:,.0f}</div>
        <div style="color: #7f8c8d; font-size: 14px;">$</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">상위 20% 매출 기여도</div>
        <div class="metric-value">{top_20_ratio:.1f}%</div>
        <div style="color: #e74c3c; font-size: 14px;">파레토 법칙</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">고가 제품 매출 비중</div>
        <div class="metric-value">{high_price_ratio:.1f}%</div>
        <div style="color: #3498db; font-size: 14px;">프리미엄 전략</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 파레토 분석
st.markdown('<div class="section-header">파레토 분석 - 제품 vs 고객 매출 집중도</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=product_agg['Product_Rank_Ratio'],
        y=product_agg['Sales_Ratio'],
        mode='lines',
        line=dict(color='#3498db', width=3),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.2)',
        name='누적 매출'
    ))
    
    fig.add_vline(x=0.2, line_dash="dash", line_color="red", line_width=2)
    fig.add_hline(y=0.733, line_dash="dash", line_color="red", line_width=2)
    fig.add_annotation(x=0.2, y=0.733, text="73.3% Revenue", showarrow=True, bgcolor="white")
    
    fig.update_layout(
        title="제품별 파레토 분석",
        xaxis_title="누적 제품 비율",
        yaxis_title="누적 매출 비율",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    customer_agg = df.groupby('User_ID')['Purchase'].sum().sort_values(ascending=False).reset_index()
    customer_agg['Cumulative'] = customer_agg['Purchase'].cumsum()
    customer_agg['Sales_Ratio'] = customer_agg['Cumulative'] / customer_agg['Purchase'].sum()
    customer_agg['Rank_Ratio'] = np.arange(1, len(customer_agg)+1) / len(customer_agg)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=customer_agg['Rank_Ratio'],
        y=customer_agg['Sales_Ratio'],
        mode='lines',
        line=dict(color='#27ae60', width=3),
        fill='tozeroy',
        fillcolor='rgba(39, 174, 96, 0.2)'
    ))
    
    top_20_cust = customer_agg[customer_agg['Rank_Ratio']<=0.2]['Sales_Ratio'].iloc[-1]
    fig2.add_vline(x=0.2, line_dash="dash", line_color="orange", line_width=2)
    fig2.add_hline(y=top_20_cust, line_dash="dash", line_color="orange", line_width=2)
    fig2.add_annotation(x=0.2, y=top_20_cust, text=f"{top_20_cust*100:.1f}% Revenue", showarrow=True, bgcolor="white")
    
    fig2.update_layout(
        title="고객별 파레토 분석",
        xaxis_title="누적 고객 비율",
        yaxis_title="누적 매출 비율",
        height=400,
        plot_bgcolor='white'
    )
    st.plotly_chart(fig2, use_container_width=True)

# 가격 전략
st.markdown('<div class="section-header">가격 전략 분석 - Price vs Volume</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    top_products = product_agg.head(int(len(product_agg)*0.2))
    
    fig3 = px.scatter(
        top_products,
        x='Avg_Price',
        y='Volume',
        size='Total_Sales',
        color='Price_Segment',
        color_discrete_map={
            'High Price': '#e74c3c',
            'Medium Price': '#f39c12',
            'Low Price': '#95a5a6'
        },
        title='상위 20% 제품: 가격 vs 판매량',
        height=500
    )
    
    fig3.add_hline(y=top_products['Volume'].median(), line_dash="dash", opacity=0.5)
    fig3.add_vline(x=top_products['Avg_Price'].mean(), line_dash="dash", opacity=0.5)
    fig3.update_layout(plot_bgcolor='white')
    
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    segment_sales = product_agg.groupby('Price_Segment')['Total_Sales'].sum().reset_index()
    
    fig4 = go.Figure(data=[go.Pie(
        labels=segment_sales['Price_Segment'],
        values=segment_sales['Total_Sales'],
        hole=0.4,
        marker=dict(colors=['#e74c3c', '#95a5a6', '#f39c12']),
        textinfo='label+percent'
    )])
    
    fig4.update_layout(title="세그먼트별 매출", height=250)
    st.plotly_chart(fig4, use_container_width=True)
    
    # 게이지
    fig5 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=high_price_ratio,
        title={'text': "고가 제품 비중"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ecc71"},
            'steps': [
                {'range': [0, 40], 'color': "#ecf0f1"},
                {'range': [40, 60], 'color': "#bdc3c7"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': 50}
        }
    ))
    fig5.update_layout(height=250)
    st.plotly_chart(fig5, use_container_width=True)

# 카테고리 분석
st.markdown('<div class="section-header">핵심 카테고리 성과</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    cat_sales = df.groupby('Product_Category')['Purchase'].sum().sort_values(ascending=False).head(top_n).reset_index()
    cat_sales['Category'] = 'Category ' + cat_sales['Product_Category'].astype(str)
    
    fig6 = px.bar(
        cat_sales,
        x='Category',
        y='Purchase',
        title=f'Top {top_n} 카테고리',
        color='Purchase',
        color_continuous_scale='Teal',
        height=400
    )
    fig6.update_layout(plot_bgcolor='white', showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    high_products = product_agg[product_agg['Price_Segment']=='High Price']['Product_ID']
    high_cat = df[df['Product_ID'].isin(high_products)].groupby('Product_Category')['Purchase'].sum().sort_values(ascending=False).head(10)
    high_cat_df = pd.DataFrame({
        'Category': 'Cat ' + high_cat.index.astype(str),
        'Percentage': high_cat.values / high_cat.sum() * 100
    })
    
    fig7 = px.bar(
        high_cat_df,
        y='Category',
        x='Percentage',
        orientation='h',
        title='고가 제품군 카테고리',
        color='Percentage',
        color_continuous_scale='Reds',
        height=400
    )
    fig7.update_layout(plot_bgcolor='white', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig7, use_container_width=True)

# 교차판매 매트릭스
st.markdown('<div class="section-header">번들링 & 교차판매 분석</div>', unsafe_allow_html=True)

top_cats = [1, 5, 8, 10, 2, 3, 6]
user_cat = df[df['Product_Category'].isin(top_cats)].pivot_table(
    index='User_ID',
    columns='Product_Category',
    values='Purchase',
    aggfunc='count',
    fill_value=0
)
user_cat = (user_cat > 0).astype(int)

co_matrix = user_cat.T @ user_cat
co_pct = pd.DataFrame(index=co_matrix.index, columns=co_matrix.columns, dtype=float)

for i in co_matrix.index:
    for j in co_matrix.columns:
        if i == j:
            co_pct.loc[i, j] = 0.0
        else:
            co_pct.loc[i, j] = (co_matrix.loc[i, j] / co_matrix.loc[i, i] * 100) if co_matrix.loc[i, i] > 0 else 0

fig8 = px.imshow(
    co_pct,
    x=['Cat_'+str(c) for c in co_pct.columns],
    y=['Cat_'+str(c) for c in co_pct.index],
    color_continuous_scale='RdYlGn',
    title='주요 카테고리 동시구매율 (%)',
    height=500,
    aspect='auto'
)
fig8.update_traces(text=co_pct.round(1), texttemplate='%{text}%')
st.plotly_chart(fig8, use_container_width=True)

# 실행 계획
st.markdown('<div class="section-header">실행 대시보드 - Action Plan</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📋 핵심 이니셔티브")
    initiatives = pd.DataFrame({
        'Name': ['프리미엄 번들 출시', '통합 재고 시스템', 'Cat 10 교차판매', '저가 제품 축소'],
        'KPI': ['Cat 1+5+8 동시구매↑', 'Cat 1,5,8 품절 0%', 'Cat 10 매출 15%↑', '재고회전율 개선'],
        'Status': ['In Progress', 'Analysis', 'Analysis', 'Planning'],
        'Budget': ['8.5K$', '12K$', '5K$', '3K$']
    })
    st.dataframe(initiatives, hide_index=True, use_container_width=True)

with col2:
    st.markdown("#### ⚠️ 리스크 관리")
    risks = pd.DataFrame({
        'Name': ['Cat 1 품절 리스크', '번들 가격 경쟁력', 'Cat 5-8 재고 동기화', '고가 수요 예측'],
        'Status': ['Analysis', 'Analysis', 'In Progress', 'Planning']
    })
    st.dataframe(risks, hide_index=True, use_container_width=True)

# 타임라인
st.markdown("#### 📅 이니셔티브 타임라인")

gantt = [
    dict(Task="프리미엄 번들", Start='2024-10-01', Finish='2025-01-31', Status='In Progress'),
    dict(Task="재고 시스템", Start='2025-01-01', Finish='2025-04-30', Status='Analysis'),
    dict(Task="Cat 10 육성", Start='2024-12-01', Finish='2025-03-31', Status='Analysis'),
    dict(Task="저가 축소", Start='2025-02-01', Finish='2025-04-30', Status='Planning'),
]

fig9 = px.timeline(
    gantt,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Status",
    color_discrete_map={'In Progress': '#e74c3c', 'Analysis': '#3498db', 'Planning': '#9b59b6'},
    title="전략 실행 타임라인",
    height=300
)
fig9.update_yaxes(categoryorder="total ascending")
fig9.update_layout(plot_bgcolor='white')
st.plotly_chart(fig9, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p><strong>Walmart 매출 최적화 전략 대시보드</strong></p>
    <p>Data-Driven Decision Making | Powered by Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)