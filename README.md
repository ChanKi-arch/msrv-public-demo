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

> *Tier naming note:*  
> In earlier docs you may see **bypass/lite/full** — these map 1:1 to  
> **MINI/ STANDARD/ PREMIUM** in this release for consistency.

---

## 📊 v2.5.5-final Benchmark Summary

**Engine Version:** `2.5.5-final`  
**Total Samples:** 4,200  
**Alignment:** 89.8%  
**Latency:** 0.3–2ms

### 🔒 Conservative (Safety-first)
| Mode | MINI | STANDARD | PREMIUM | Cost Saving |
|------|------|----------|---------|--------------|
| Conservative | 0 (0.0%) | 3,810 (90.7%) | 390 (9.3%) | 63.5% |

### ⚖️ Balanced (Default)
| Mode | MINI | STANDARD | PREMIUM | Cost Saving |
|------|------|----------|---------|--------------|
| Balanced | 1,019 (24.3%) | 2,873 (68.4%) | 308 (7.3%) | 71.7% |

### 🚀 Aggressive (Cost-optimized)
| Mode | MINI | STANDARD | PREMIUM | Cost Saving |
|------|------|----------|---------|--------------|
| Aggressive | 2,595 (61.8%) | 1,387 (33.0%) | 218 (5.2%) | 83.7% |

> Full detail report and reproducible benchmark artifacts are in `report/`.

---

## 📍 Quickstart

### 1. Extract demo
```bash
unzip msrv-public-demo-v255.zip
cd msrv-public-demo-v2/

2. Run engine CLI (example)

python msrv_v255_unified_final.py --stdin --out result.json \
    --model-lang ko --input-sample sample.json

3. Gateway example

python msrv_gateway_v11_final.py --host 0.0.0.0 --port 8080

4. WebUI sample

Open webui/index.html in a browser (no server required).


---

🧪 Reproduce Benchmarks

Benchmark runner

python tools/msrv_benchmark_unified.py \
    --mode balanced \
    --output report/benchmark_report.md \
    --summary-json report/benchmark_summary.json

Inspect artifacts

report/benchmark_summary.json — aggregated metrics

report/benchmark_details.jsonl — per-sample records

report/benchmark_report.md — human-readable report



---

🔐 IP & Safety Notice

This repository contains reproducible benchmarks and artifacts for evaluation.
The core model weights or proprietary provider credentials are not included.

Use this code and results to verify performance and routing behavior without exposing sensitive API keys.


---

📦 Included Files

├─ msrv_v255_unified_final.py
├─ msrv_gateway_v11_final.py
├─ sample.json                   # example input
├─ webui/
│   └─ index.html                # UI sample
├─ demo/
│   └─ ...                      # CLI scenario scripts
├─ tools/
│   └─ msrv_benchmark_unified.py
├─ report/
│   ├─ benchmark_report.md
│   ├─ benchmark_summary.json
│   └─ benchmark_details.jsonl
├─ docs/
│   ├─ ARCHITECTURE_OVERVIEW.md
│   ├─ ROUTING_AND_CONTROL.md
│   └─ ...                     # original documentation files
└─ BENCHMARK_SUMMARY.md         # snapshot of v2.5.5 results


---

📝 References

For deeper background, see the docs in docs/:

ARCHITECTURE_OVERVIEW.md — engine design principles

ROUTING_AND_CONTROL.md — tier mapping & control logic

GOVERNANCE_PHILOSOPHY.md — safety framing



---

📣 Credits

This release is based on contributions from:

ChanKi architecture team

Community feedback and reproducibility efforts


v2.5.5-final — Public Demo Release


---
