# MSR-V White Engine — Public Demo (v2.5.5-final)

> **Structural control layer for LLM orchestration** — control *reasoning depth*, not tokens.

This repository contains the **public demo** of the MSR-V White Engine (core logic + gateway-ready adapter),
including a **full 4,200-sample benchmark** (KO/EN × normal/negation/hard).

---

## What MSR-V is (in one paragraph)

MSR-V is a **white-box routing and safety control layer** that inspects a prompt’s *structural risk and need*
and decides **how much reasoning / which tier** should handle it.
It is designed to reduce unnecessary premium-model usage while preserving safety through explicit gates
(e.g., `high_stakes`, fracture escalation, mode thresholds).

---

## Key benchmark results (4,200 samples)

Benchmark date: **2026-01-06**  
Engine: **v2.5.5-final**  
Cost weights: MINI=2, STANDARD=30, PREMIUM=100 (PREMIUM baseline)

| Mode | MINI | STANDARD | PREMIUM | Cost Reduction | Avg Latency |
|---|---:|---:|---:|---:|---:|
| CONSERVATIVE | 0 (0.0%) | 3810 (90.7%) | 390 (9.3%) | 63.5% | 0.84 ms |
| BALANCED | 1019 (24.3%) | 2873 (68.4%) | 308 (7.3%) | 71.7% | 0.85 ms |
| AGGRESSIVE | 2595 (61.8%) | 1387 (33.0%) | 218 (5.2%) | 83.7% | 0.88 ms |

➡️ Full report: **`report/benchmark_report.md`**  
➡️ Machine-readable: **`report/benchmark_*_summary.json`**, **`report/benchmark_*_details.jsonl`**

---

## 3 modes (operational intent)

- **CONSERVATIVE**: pilot / trust-building (MINI effectively disabled)
- **BALANCED**: recommended default (cost ↔ safety balanced)
- **AGGRESSIVE**: cost-optimization (MINI maximized; requires trusted MINI provider)

---

## Quickstart

```bash
pip install -r requirements.txt
python demo_cli.py
```

---

## Files

- **Core engine**: `engine.py`
- **Gateway/adapter demo**: `web_ui.py`
- **Benchmark report (MD)**: `report/benchmark_report.md`
- **Benchmark summaries (JSON)**: `report/benchmark_conservative_summary.json`, etc.
- **Benchmark details (JSONL)**: `report/benchmark_conservative_details.jsonl`, etc.
- **Benchmark runner**: `tools/msrv_benchmark_unified.py`

---

## License / Notice

This is a **public demo** intended to showcase the white-box control concept and benchmark evidence.

This repository provides a public demo interface and benchmark artifacts.
The proprietary MSR-V core engine, policy logic, and advanced parsers are not included in this release.
