import pandas as pd
import joblib

# ── 1. 학습 시 사용한 전처리 함수 동일하게 정의
def preprocess(X):
    X = X.copy()
    X['EDUCATION'] = X['EDUCATION'].replace({0:4, 5:4, 6:4})
    X['MARRIAGE']  = X['MARRIAGE'].replace({0:3})
    return X

# ── 2. 모델 로드
pipeline = joblib.load('./model/pipeline.pkl')

# ── 3. 학습 시 컬럼 순서
FEATURE_COLS = [
    'LIMIT_BAL','SEX','EDUCATION','MARRIAGE','AGE',
    'PAY_0','PAY_2','PAY_3','PAY_4','PAY_5','PAY_6',
    'BILL_AMT1','BILL_AMT2','BILL_AMT3','BILL_AMT4','BILL_AMT5','BILL_AMT6',
    'PAY_AMT1','PAY_AMT2','PAY_AMT3','PAY_AMT4','PAY_AMT5','PAY_AMT6'
]

# ── 4. 예측 함수
def predict(input_dict: dict, threshold: float = 0.5) -> dict:

    # 입력 → DataFrame
    X = pd.DataFrame([input_dict])

    # 컬럼 순서 정렬
    X = X[FEATURE_COLS]

    # 학습 때와 동일한 전처리
    X = preprocess(X)

    # 확률 예측
    prob = pipeline.predict_proba(X)[0][1]

    # threshold 기준 분류
    pred = int(prob >= threshold)

    return {
        "probability": round(float(prob), 4),
        "prediction": pred,
        "label": "채무불이행 위험 ⚠️" if pred else "정상 고객 ✅"
    }