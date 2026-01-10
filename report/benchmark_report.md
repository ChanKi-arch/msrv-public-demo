# MSR-V v2.5.5 Unified Benchmark Report

**Generated**: 2026-01-06 13:10:01  
**Total Samples**: 4,200  
**Engine Version**: 2.5.5-unified-patched

---

## 📋 Terminology Changes

| Previous | New | Description |
|----------|-----|-------------|
| BYPASS | **MINI** | Ultra-low-cost / local / domestic model |
| LITE | **STANDARD** | Budget global model |
| FULL | **PREMIUM** | Premium global model |

---

## 📊 Cost Weights

| Tier | Cost Weight |
|------|-------------|
| MINI | 2 |
| STANDARD | 30 |
| PREMIUM | 100 |

---

## 📈 Results by Mode

| Mode | MINI | STANDARD | PREMIUM | Cost Reduction | Avg Latency | Total Time |
|------|------|----------|---------|----------------|-------------|------------|
| **CONSERVATIVE** | 0 (0.0%) | 3,810 (90.7%) | 390 (9.3%) | 63.5% | 0.84ms | 3.6s |
| **BALANCED** | 1,019 (24.3%) | 2,873 (68.4%) | 308 (7.3%) | 71.7% | 0.85ms | 3.6s |
| **AGGRESSIVE** | 2,595 (61.8%) | 1,387 (33.0%) | 218 (5.2%) | 83.7% | 0.88ms | 3.7s |

---

## 🎛️ Mode Descriptions

### 🔒 CONSERVATIVE (Pilot / Trust-Building)
- MINI routing disabled
- All inputs verified at STANDARD or higher
- Safety-first, minimal cost savings

### ⚖️ BALANCED (Recommended for Production)
- Cost and safety balanced
- Moderate MINI routing allowed
- Recommended for general operations

### 🚀 AGGRESSIVE (Cost Optimization)
- MINI routing maximized
- Maximum cost savings
- Requires trusted MINI provider

---

## 📁 Dataset Composition

| Language | Type | Samples |
|----------|------|---------|
| KO | Normal | 1,000 |
| KO | Negation | 1,000 |
| KO | Hard | 100 |
| EN | Normal | 1,000 |
| EN | Negation | 1,000 |
| EN | Hard | 100 |
| **Total** | | **4,200** |

---

## 🔧 Usage

```python
from msrv_v255_unified_final import MSRVEngineV25, ThresholdConfig

engine = MSRVEngineV25(ThresholdConfig())

# Switch mode
engine.set_mode("conservative")   # Pilot
engine.set_mode("balanced")       # Recommended
engine.set_mode("aggressive")     # Max savings

# Analyze
result = engine.inspect("Your text here", lang="EN")
print(result["output"]["route"])  # MINI / STANDARD / PREMIUM
```

---

## 📊 White-Box Trace Example

Each sample produces a traceable governance output:

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

## ✅ Summary

| Mode | Cost Reduction | MINI Routing |
|------|----------------|--------------|
| **CONSERVATIVE** | 63.5% | 0.0% |
| **BALANCED** | 71.7% | 24.3% |
| **AGGRESSIVE** | 83.7% | 61.8% |
