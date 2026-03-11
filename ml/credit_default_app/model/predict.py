import pandas as pd
import joblib

# 모델 로드
pipeline = joblib.load('pipeline.pkl')

# 학습 시 컬럼 순서 (feature_cols.json 없이 직접 고정)
FEATURE_COLS = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1',  'PAY_AMT2',  'PAY_AMT3',  'PAY_AMT4',  'PAY_AMT5',  'PAY_AMT6',
]

def predict(input_dict: dict, threshold: float = 0.5) -> dict:
    X    = pd.DataFrame([input_dict])[FEATURE_COLS]
    prob = pipeline.predict_proba(X)[0][1]
    pred = int(prob >= threshold)

    return {
        'probability' : round(float(prob), 4),
        'prediction'  : pred,
        'label'       : '채무불이행 위험 ⚠️' if pred == 1 else '정상 ✅',
    }