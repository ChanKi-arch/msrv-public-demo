✅ MSR-V Public Demo – README (Final Rendered Version)

# MSR-V Public Demo (v2.5.5-final)

**White-box Structural Routing & Control Layer for LLM Management**  
*Engine + Gateway + Benchmark artifacts — reproducible & open artifacts only*

---

## 📦 Download

- **Source code (ZIP)**  
  https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-final.zip

- **Source code (TAR.GZ)**  
  https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-final.tar.gz

- **Release page**  
  https://github.com/ChanKi-arch/msrv-public-demo/releases/tag/v2.5.5-final

---

## 🚀 Overview

MSR-V is a **white-box inference control layer** that routes input to different model tiers based on structural confidence and alignment needs.  
It is *not* a model itself — instead, it enables **cost reduction with safety controls** using reproducible routing logic.

This repository includes:
- Production-ready **engine** + **adapter gateway**
- CLI & WebUI samples
- Full **benchmarks** (v2.5.5-final)
- Reproducible artifacts (summary JSON + JSONL + report)

---

## 📌 Key Concepts

| Term | Meaning |
|------|---------|
| **Engine** | Core structural router / score analyzer |
| **Gateway** | Adapter layer to LLM providers |
| **Tier** | MINI / STANDARD / PREMIUM (cost vs quality) |
| **Mode** | Conservative / Balanced / Aggressive runtime presets |
| **Routing** | Decision of which tier to use per request |

> **Tier naming note**  
> Legacy docs may use **bypass / lite / full** — these map 1:1 to  
> **MINI / STANDARD / PREMIUM** in this release.

---

## 📊 v2.5.5-final Benchmark Summary

**Engine Version:** `2.5.5-final`  
**Total Samples:** 4,200  
**Alignment:** 89.8%  
**Latency:** 0.3–2 ms  

### 🔒 Conservative (Safety-first)
| MINI | STANDARD | PREMIUM | Cost Saving |
|------|----------|---------|-------------|
| 0 (0.0%) | 3,810 (90.7%) | 390 (9.3%) | 63.5% |

### ⚖️ Balanced (Default)
| MINI | STANDARD | PREMIUM | Cost Saving |
|------|----------|---------|-------------|
| 1,019 (24.3%) | 2,873 (68.4%) | 308 (7.3%) | 71.7% |

### 🚀 Aggressive (Cost-optimized)
| MINI | STANDARD | PREMIUM | Cost Saving |
|------|----------|---------|-------------|
| 2,595 (61.8%) | 1,387 (33.0%) | 218 (5.2%) | **83.7%** |

Full details are in the `report/` directory.

---

## 📍 Quickstart

```bash
git clone https://github.com/ChanKi-arch/msrv-public-demo
cd msrv-public-demo
git checkout v2.5.5-final
pip install -r requirements.txt
python msrv_v255_unified_final.py --stdin


---

🧪 Reproduce Benchmarks

python tools/msrv_benchmark_unified.py \
  --mode balanced \
  --output report/benchmark_report.md \
  --summary-json report/benchmark_summary.json

Artifacts:

report/benchmark_summary.json

report/benchmark_details.jsonl

report/benchmark_report.md



---

🔐 IP & Safety Notice

This repository contains reproducible benchmarks and a public demo engine.
Proprietary production models, weights, and provider credentials are not included.


---

📦 Included Files

msrv_v255_unified_final.py
msrv_gateway_v11_final.py
sample.json
webui/
demo/
tools/
report/
docs/
BENCHMARK_SUMMARY.md


---

📝 References

ARCHITECTURE_OVERVIEW.md — engine design

ROUTING_AND_CONTROL.md — tier & policy logic

GOVERNANCE_PHILOSOPHY.md — safety framing
