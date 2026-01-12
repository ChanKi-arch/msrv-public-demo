# MSR-V v2.5.5 Benchmark Report

**Generated**: 2026-01-11 14:24:56  
**Total Samples**: 4,200  
**Engine Version**: 2.5.5

---

## 📊 Cost Weights

| Tier | Cost Weight | Description |
|------|-------------|-------------|
| MINI | 2 | Local/Internal low-cost models |
| STANDARD | 30 | Global affordable models |
| PREMIUM | 100 | Global premium models |

---

## 📈 Overall Results by Mode

| Mode | MINI | STANDARD | PREMIUM | Cost Savings | Avg Latency | Safety |
|------|------|----------|---------|--------------|-------------|--------|
| **CONSERVATIVE** | 0 (0.0%) | 3817 (90.9%) | 383 (9.1%) | 63.6% | 0.865ms | ✅ PASS |
| **BALANCED** | 961 (22.9%) | 2856 (68.0%) | 383 (9.1%) | 70.0% | 0.850ms | ✅ PASS |
| **AGGRESSIVE** | 2444 (58.2%) | 1374 (32.7%) | 382 (9.1%) | 79.9% | 0.862ms | ✅ PASS |

---

## 🔒 Safety Validation (Fracture → MINI Prevention)

| Mode | Fracture Samples | Fracture→MINI | Validation |
|------|------------------|---------------|------------|
| CONSERVATIVE | 382 | 0 | ✅ PASS |
| BALANCED | 382 | 0 | ✅ PASS |
| AGGRESSIVE | 382 | 0 | ✅ PASS |

---

## 📋 Detailed Results by Dataset

### 🔒 CONSERVATIVE Mode

| Dataset | Samples | MINI | STANDARD | PREMIUM | Cost Savings | Latency | White-Box |
|---------|---------|------|----------|---------|--------------|---------|-----------|
| 한국어 일반 | 1000 | 0 (0.0%) | 1000 (100.0%) | 0 (0.0%) | 70.0% | 0.314ms | 100% |
| 한국어 부정 | 1000 | 0 (0.0%) | 1000 (100.0%) | 0 (0.0%) | 70.0% | 0.267ms | 100% |
| 한국어 고난도 | 100 | 0 (0.0%) | 98 (98.0%) | 2 (2.0%) | 68.6% | 0.580ms | 100% |
| 영어 일반 | 1000 | 0 (0.0%) | 849 (84.9%) | 151 (15.1%) | 59.4% | 1.561ms | 100% |
| 영어 부정 | 1000 | 0 (0.0%) | 787 (78.7%) | 213 (21.3%) | 55.1% | 1.256ms | 100% |
| 영어 고난도 | 100 | 0 (0.0%) | 83 (83.0%) | 17 (17.0%) | 58.1% | 1.751ms | 100% |
| **TOTAL** | **4200** | **0** (0.0%) | **3817** (90.9%) | **383** (9.1%) | **63.6%** | **0.865ms** | **100%** |

### ⚖️ BALANCED Mode

| Dataset | Samples | MINI | STANDARD | PREMIUM | Cost Savings | Latency | White-Box |
|---------|---------|------|----------|---------|--------------|---------|-----------|
| 한국어 일반 | 1000 | 39 (3.9%) | 961 (96.1%) | 0 (0.0%) | 71.1% | 0.306ms | 100% |
| 한국어 부정 | 1000 | 0 (0.0%) | 1000 (100.0%) | 0 (0.0%) | 70.0% | 0.260ms | 100% |
| 한국어 고난도 | 100 | 0 (0.0%) | 98 (98.0%) | 2 (2.0%) | 68.6% | 0.555ms | 100% |
| 영어 일반 | 1000 | 451 (45.1%) | 398 (39.8%) | 151 (15.1%) | 72.1% | 1.535ms | 100% |
| 영어 부정 | 1000 | 417 (41.7%) | 370 (37.0%) | 213 (21.3%) | 66.8% | 1.239ms | 100% |
| 영어 고난도 | 100 | 54 (54.0%) | 29 (29.0%) | 17 (17.0%) | 73.2% | 1.769ms | 100% |
| **TOTAL** | **4200** | **961** (22.9%) | **2856** (68.0%) | **383** (9.1%) | **70.0%** | **0.850ms** | **100%** |

### 🚀 AGGRESSIVE Mode

| Dataset | Samples | MINI | STANDARD | PREMIUM | Cost Savings | Latency | White-Box |
|---------|---------|------|----------|---------|--------------|---------|-----------|
| 한국어 일반 | 1000 | 622 (62.2%) | 378 (37.8%) | 0 (0.0%) | 87.4% | 0.304ms | 100% |
| 한국어 부정 | 1000 | 568 (56.8%) | 432 (43.2%) | 0 (0.0%) | 85.9% | 0.263ms | 100% |
| 한국어 고난도 | 100 | 59 (59.0%) | 40 (40.0%) | 1 (1.0%) | 85.8% | 0.589ms | 100% |
| 영어 일반 | 1000 | 510 (51.0%) | 339 (33.9%) | 151 (15.1%) | 73.7% | 1.560ms | 100% |
| 영어 부정 | 1000 | 623 (62.3%) | 164 (16.4%) | 213 (21.3%) | 72.5% | 1.258ms | 100% |
| 영어 고난도 | 100 | 62 (62.0%) | 21 (21.0%) | 17 (17.0%) | 75.5% | 1.744ms | 100% |
| **TOTAL** | **4200** | **2444** (58.2%) | **1374** (32.7%) | **382** (9.1%) | **79.9%** | **0.862ms** | **100%** |

---

## 🏷️ White-Box Trace Fields

Each routing decision includes the following traceable fields:

```json
{
  "Zs": 0.6325,
  "state4": "Alignment",
  "shape": "─",
  "theta": 0.2,
  "need": 0.368,
  "bypass_base": 0.2,
  "short_sig": false,
  "short_sig_cap_applied": false,
  "is_fracture": false,
  "high_stakes": false,
  "residual_ratio": 0.92,
  "rule": "need=0.368<=lite;lang=KO"
}
```

| Field | Description |
|-------|-------------|
| `Zs` | Stability score (0-1) |
| `state4` | State classification (Harmony/Divergence/Alignment/Fracture) |
| `shape` | Structural complexity (□/△/─/·) |
| `need` | Computed routing need (0-1) |
| `is_fracture` | Whether sentence is in Fracture state |
| `short_sig_cap_applied` | Whether short-signal cap was applied |
| `high_stakes` | Whether high-stakes keywords detected |
| `rule` | Final routing decision rule |

---

## 🎛️ Mode Descriptions

### 🔒 CONSERVATIVE
- MINI routing disabled (`DISABLE_SHORT_SIG_CAP=True`)
- All sentences validated at STANDARD or higher
- Safety-first, minimal cost savings (~63%)

### ⚖️ BALANCED (Recommended)
- Balance between cost and safety
- Moderate MINI routing allowed
- Recommended for production (~70%)

### 🚀 AGGRESSIVE
- Maximize MINI routing
- Maximum cost savings (~80%)
- Requires trusted MINI provider

---

## ✅ Conclusion

- **CONSERVATIVE**: 63.6% cost savings, 0.0% MINI routing
- **BALANCED**: 70.0% cost savings, 22.9% MINI routing
- **AGGRESSIVE**: 79.9% cost savings, 58.2% MINI routing

### ✅ All Validations Passed
- Fracture→MINI prevention: **PASS**
- White-box traceability: **100%**
- Governance trust guaranteed
