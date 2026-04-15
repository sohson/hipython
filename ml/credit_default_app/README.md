# 💳 신용카드 채무불이행 고객 예측 — ML + Streamlit 대시보드

> UCI Credit Card Default Dataset을 활용한 채무불이행 예측 모델 개발 및 인터랙티브 대시보드 구현

---

## 📌 프로젝트 개요

대만 신용카드 고객 30,000명 데이터를 기반으로 다음 달 채무불이행 여부를 예측하는 머신러닝 모델을 개발하고, Streamlit 웹 애플리케이션으로 배포한 프로젝트입니다.

클래스 불균형 문제(정상 77% : 채무불이행 23%)를 해결하기 위해 SMOTE, class_weight 조정, 임계값 최적화 등 다양한 기법을 체계적으로 실험하고 비교 분석했습니다.

- **데이터**: UCI Default of Credit Card Clients (30,000건 × 24개 피처)
- **Target**: `default` (0 = 정상, 1 = 채무불이행)

---

## 🔍 분석 프로세스

| 단계 | 내용 |
|------|------|
| 1단계 EDA | 클래스 비율·결측치·기술통계·피처 분포·상관관계 |
| 2단계 전처리 | EDUCATION·MARRIAGE 이상값 통합 |
| 2-2단계 PCA | 다중공선성 탐색·차원 축소·클래스 분리 시각화 |
| 3단계 Split | Stratified 80:20 분할 |
| 4단계 불균형 처리 비교 | 베이스라인 → class_weight='balanced' → SMOTE |
| 5단계 XGBoost 비교 | XGBoost 베이스라인 / XGBoost + SMOTE |
| 6단계 전체 비교 | 5개 모델 종합 비교표·최종 모델 선택 |
| 7단계 피처 중요도 | RFC+SMOTE vs 베이스라인 RFC 비교 |
| 8단계 PR Curve | 소수 클래스(채무불이행) 관점 성능 확인 |
| 9단계 임계값 조정 | Threshold 변화에 따른 Recall 개선 |
| 10단계 최종 비교 | 임계값 적용 전후 최종 성능 비교 |

---

## 📊 모델 성능 비교

**평가 지표 선택 근거**: 채무불이행 탐지가 목적이므로 Recall과 F1-Score를 주요 지표로 사용

| 모델 | Precision | Recall | F1-Score | ROC-AUC |
|------|:---------:|:------:|:--------:|:-------:|
| RFC 베이스라인 | 0.6429 | 0.3595 | 0.4611 | 0.7572 |
| RFC + balanced | 0.6450 | 0.3436 | 0.4484 | 0.7583 |
| **RFC + SMOTE** | 0.5105 | **0.4770** | **0.4932** | 0.7443 |
| **XGBoost 베이스라인** | 0.6121 | 0.3580 | 0.4517 | **0.7601** |
| XGBoost + SMOTE | 0.4574 | 0.4657 | 0.4615 | 0.7330 |

### 임계값 최적화 적용 후 최종 성능

| 모델 | 최적 Threshold | Precision | Recall | F1-Score |
|------|:-----------:|:---------:|:------:|:--------:|
| RFC + SMOTE | 0.42 | 0.4460 | 0.5818 | **0.5049** |
| XGBoost 베이스라인 | 0.27 | 0.4720 | 0.5659 | **0.5147** |

→ **최종 선택 모델**: RFC + SMOTE (임계값 0.42 적용) — Precision/Recall 균형 및 파이프라인 재현성 우수

---

## 🖥️ Streamlit 대시보드

고객 정보를 입력하면 채무불이행 리스크를 실시간으로 예측하는 인터랙티브 웹 앱입니다.

**주요 기능**
- Plotly 게이지 차트 기반 **4단계 리스크 분류** (안전 / 주의 / 경고 / 위험)
- 고객 특성 입력 폼 (신용한도, 성별, 학력, 결혼 여부, 나이, 납부 이력 등)
- 예측 확률 및 주요 피처 기여도 시각화

---

## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=flat&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

| 분류 | 기술 |
|------|------|
| **언어** | Python |
| **ML** | Scikit-learn (RFC), XGBoost, imbalanced-learn (SMOTE) |
| **전처리/분석** | Pandas, NumPy, PCA |
| **시각화** | Matplotlib, Seaborn, Plotly |
| **웹 앱** | Streamlit |
| **모델 저장** | joblib |

---

## 📁 파일 구조

```
credit_default_app/
├── 11_신용카드_채무불이행_고객예측.ipynb  # 전체 모델링 과정
├── app.py                                 # Streamlit 대시보드
└── model/
    └── pipeline.pkl                       # 학습된 모델 파이프라인 (joblib)
```

---

*Data Source: [UCI Machine Learning Repository — Default of Credit Card Clients](https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset)*
