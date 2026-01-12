# MSR-V Gateway v1.1.1 + Engine v2.5.5-patch-fracture 통합 벤치마크

**생성일시**: 2026-01-11 14:05:26  
**총 샘플**: 4,200개  
**게이트웨이 버전**: 1.1.1  
**엔진 버전**: 2.5.5-patch-fracture

---

## 📋 패치 내용

### Gateway v1.1.1 패치
```python
# _safe_route_from_str() backward-compat 추가

# ✅ 레거시 용어 지원
if "BYPASS" in route_upper:
    return RouteDecision.MINI
if "LITE" in route_upper:
    return RouteDecision.STANDARD
if "FULL" in route_upper:
    return RouteDecision.PREMIUM

# 신규 용어
if "MINI" in route_upper:
    return RouteDecision.MINI
# ...
```

### backward-compat 테스트
| 상태 | 결과 |
|------|------|
| 테스트 통과 | ✅ PASS |

---

## 📈 모드별 결과 요약

| 모드 | MINI | STANDARD | PREMIUM | 비용 절감 | 평균 지연 | Fracture→MINI |
|------|------|----------|---------|----------|----------|---------------|
| **CONSERVATIVE** | 0 (0.0%) | 3817 (90.9%) | 383 (9.1%) | 63.6% | 0.904ms | ✅ 0 |
| **BALANCED** | 961 (22.9%) | 2856 (68.0%) | 383 (9.1%) | 70.0% | 0.889ms | ✅ 0 |
| **AGGRESSIVE** | 2444 (58.2%) | 1374 (32.7%) | 382 (9.1%) | 79.9% | 0.917ms | ✅ 0 |

---

## 🔒 안전성 검증

| 모드 | Fracture 샘플 | Fracture→MINI | 검증 |
|------|--------------|---------------|------|
| CONSERVATIVE | 382 | 0 | ✅ PASS |
| BALANCED | 382 | 0 | ✅ PASS |
| AGGRESSIVE | 382 | 0 | ✅ PASS |

---

## 🏗️ 아키텍처

```
User Request
     ↓
┌─────────────────┐
│  MSR-V Gateway  │  ← backward-compat 레이어
│    v1.1.1       │     BYPASS/LITE/FULL → MINI/STANDARD/PREMIUM
└─────────────────┘
     ↓
┌─────────────────┐
│  MSR-V Engine   │  ← Fracture cap 패치
│  v2.5.5-patch   │     is_fracture → cap 금지
└─────────────────┘
     ↓
┌────┴────┬────────┐
↓         ↓        ↓
MINI   STANDARD  PREMIUM
(skip)  (cheap)  (premium)
```

---

## ✅ 결론

- **CONSERVATIVE**: 63.6% 비용 절감, 0.0% MINI 라우팅
- **BALANCED**: 70.0% 비용 절감, 22.9% MINI 라우팅
- **AGGRESSIVE**: 79.9% 비용 절감, 58.2% MINI 라우팅

### ✅ 모든 검증 통과
- backward-compat 테스트 통과
- Fracture→MINI 라우팅 없음
- 거버넌스 신뢰 보장
