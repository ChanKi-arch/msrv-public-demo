# MSR-V v2.5.5 Unified 벤치마크 리포트

**생성일시**: 2026-01-06 13:10:01  
**총 샘플**: 4,200개  
**엔진 버전**: 2.5.5-unified-patched

---

## 📋 용어 변경

| 기존 | 신규 | 의미 |
|------|------|------|
| BYPASS | **MINI** | 초저가/내부/국내 모델 |
| LITE | **STANDARD** | 저가 글로벌 모델 |
| FULL | **PREMIUM** | 고급 글로벌 모델 |

---

## 📊 비용 가중치

| 티어 | 비용 가중치 |
|------|------------|
| MINI | 2 |
| STANDARD | 30 |
| PREMIUM | 100 |

---

## 📈 모드별 결과 요약

| 모드 | MINI | STANDARD | PREMIUM | 비용 절감 | 평균 지연 | 총 시간 |
|------|------|----------|---------|----------|----------|---------|
| **CONSERVATIVE** | 0 (0.0%) | 3810 (90.7%) | 390 (9.3%) | 63.5% | 0.84ms | 3.6s |
| **BALANCED** | 1019 (24.3%) | 2873 (68.4%) | 308 (7.3%) | 71.7% | 0.85ms | 3.6s |
| **AGGRESSIVE** | 2595 (61.8%) | 1387 (33.0%) | 218 (5.2%) | 83.7% | 0.88ms | 3.7s |

---

## 🎛️ 모드 설명

### 🔒 CONSERVATIVE (파일럿/신뢰구축)
- MINI 라우팅 비활성화
- 모든 문장 최소 STANDARD 이상 검증
- 안전 우선, 비용 절감 최소화

### ⚖️ BALANCED (권장 운영)
- 비용과 안전의 균형
- 적절한 MINI 라우팅 허용
- 일반 운영 환경 권장

### 🚀 AGGRESSIVE (비용 최적화)
- MINI 라우팅 극대화
- 최대 비용 절감
- 신뢰된 MINI 제공자 필요

---

## 📁 데이터셋 구성

| 언어 | 유형 | 샘플 수 |
|------|------|---------|
| KO | 일반 (norm) | 1,000 |
| KO | 부정 (neg) | 1,000 |
| KO | 고난도 (hard) | 100 |
| EN | 일반 (norm) | 1,000 |
| EN | 부정 (neg) | 1,000 |
| EN | 고난도 (hard) | 100 |
| **총합** | | **4,200** |

---

## 🔧 사용법

```python
from msrv_v255_unified_final import MSRVEngineV25, ThresholdConfig

engine = MSRVEngineV25(ThresholdConfig())

# 모드 전환
engine.set_mode("conservative")   # 파일럿
engine.set_mode("balanced")       # 권장
engine.set_mode("aggressive")     # 최대 절감

# 분석
result = engine.inspect("문장", lang="KO")
print(result["output"]["route"])  # MINI/STANDARD/PREMIUM
```

---

## 📊 화이트 로직 트레이스 예시

각 샘플에서 추출되는 화이트 트레이스:

```json
{
  "Zs": 0.63,
  "state4": "Alignment",
  "shape": "△",
  "theta": 0.357,
  "high_stakes": false,
  "residual_ratio": 0.24,
  "need": 0.55,
  "short_sig": false
}
```

---

## ✅ 결론

- **CONSERVATIVE**: 63.5% 비용 절감, 0.0% MINI 라우팅
- **BALANCED**: 71.7% 비용 절감, 24.3% MINI 라우팅
- **AGGRESSIVE**: 83.7% 비용 절감, 61.8% MINI 라우팅
