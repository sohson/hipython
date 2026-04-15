# 🧠 Deep Learning 
> TensorFlow / Keras 기반 딥러닝 실습 프로젝트 — CNN, RNN, DNN을 활용한 이미지 분류

---

## 📁 프로젝트 목록

### 🎽 Fashion MNIST CNN 이미지 분류 (`20_Fashion.ipynb`)

**개요**: Keras의 Fashion MNIST 데이터셋(10개 의류 카테고리, 70,000장)을 활용한 CNN 기반 이미지 분류기 개발 및 성능 비교 실험

**실험 구성**

| 실험 | 모델 | Test Accuracy |
|------|------|:-------------:|
| 베이스라인 | Basic CNN | **0.9160** |
| 개선 실험 1 | Improved - BatchNorm + Deeper | 0.9160 |
| 개선 실험 2 | Improved - BatchNorm + Dropout | 0.9135 |
| 개선 실험 3 | Improved - baseline_like | 0.9090 |
| 데이터 증강 | Augmented CNN | 0.8890 |
| 비교군 | DNN | 0.8763 |

**주요 구현 내용**
- DNN vs CNN 구조 비교 분석
- BatchNormalization, Dropout, 필터 수 조절을 통한 성능 개선 실험
- 데이터 증강(ImageDataGenerator) 적용 효과 검증
- EarlyStopping, ReduceLROnPlateau 콜백 활용
- 레이어별 피처맵 시각화 (Grad-CAM 대체)
- 실제 이미지 입력 시 자동 반전 로직 구현
- 오분류 케이스 분석

**환경**: RTX 4060 Laptop GPU, TensorFlow/Keras 3, CUDA 12.5

---

## 🛠️ 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=flat&logo=keras&logoColor=white)

| 분류 | 기술 |
|------|------|
| **프레임워크** | TensorFlow 2.x, Keras 3 |
| **언어** | Python 3.11 |
| **분석/전처리** | NumPy, Pandas |
| **시각화** | Matplotlib |
| **환경** | WSL Ubuntu, NVIDIA RTX 4060 Laptop GPU |
| **패키지 관리** | conda (miniforge) |

---

## ⚙️ 실행 환경 설정

```bash
# GPU 메모리 동적 할당 (메모리 선점 방지)
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)
```

---

*삼정KPMG Future Academy 8기 | 딥러닝 실습 커리큘럼*
