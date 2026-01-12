# MSR-V White Engine — Public Demo (v2.5.5-patch)

> **Structural control layer for LLM orchestration** — control *reasoning depth*, not tokens.

This repository contains the **public demo** of the MSR-V White Engine (core logic + gateway-ready adapter),
including a **full 4,200-sample benchmark** (KO/EN × normal/negation/hard).

---

## What MSR-V is (in one paragraph)

MSR-V is a **white-box routing and safety control layer** that inspects a prompt's *structural risk and need*
and decides **how much reasoning / which tier** should handle it.
It is designed to reduce unnecessary premium-model usage while preserving safety through explicit gates
(e.g., `high_stakes`, fracture escalation, mode thresholds).

---

## 🔒 Governance Rule (v2.5.5-patch)

The public demo enforces the same **Fracture → STANDARD/PREMIUM** governance rule
as the proprietary MSR-V White Engine, even when using heuristic fallback.

```
Fracture state → MUST route to STANDARD or PREMIUM, NEVER MINI
```

This ensures safety-critical structural breakdowns are always handled by verified models.

---

## Key benchmark results (4,200 samples)

Benchmark date: **2026-01-11**  
Engine: **v2.5.5-patch**  
Cost weights: MINI=2, STANDARD=30, PREMIUM=100 (PREMIUM baseline)

| Mode | MINI | STANDARD | PREMIUM | Cost Reduction | Avg Latency | Fracture→MINI |
|---|---:|---:|---:|---:|---:|---:|
| 🔒 CONSERVATIVE | 0 (0.0%) | 3,817 (90.9%) | 383 (9.1%) | 63.6% | 0.87 ms | ✅ 0 |
| ⚖️ BALANCED | 961 (22.9%) | 2,856 (68.0%) | 383 (9.1%) | 70.0% | 0.85 ms | ✅ 0 |
| 🚀 AGGRESSIVE | 2,444 (58.2%) | 1,374 (32.7%) | 382 (9.1%) | 79.9% | 0.86 ms | ✅ 0 |

**✅ Safety Validation: All 382 Fracture samples correctly routed to STANDARD/PREMIUM (0 → MINI)**

➡️ Full report: **`report/BENCHMARK_REPORT.md`**  
➡️ Machine-readable: **`report/benchmark_*_summary.json`**, **`report/benchmark_*_details.jsonl`**

---

## 3 modes (operational intent)

- **🔒 CONSERVATIVE**: pilot / trust-building (MINI effectively disabled) — 63.6% cost savings
- **⚖️ BALANCED**: recommended default (cost ↔ safety balanced) — 70.0% cost savings
- **🚀 AGGRESSIVE**: cost-optimization (MINI maximized; requires trusted MINI provider) — 79.9% cost savings

---

## White-Box Trace Fields

Each routing decision includes traceable fields:

```json
{
  "route": "STANDARD",
  "state4": "Fracture",
  "Zs": 0.32,
  "need": 0.65,
  "route_reason": {
    "is_fracture": true,
    "short_sig_cap_applied": false,
    "governance": "Fracture→MINI blocked"
  }
}
```

---

## Quickstart

```bash
pip install -r requirements.txt

# CLI
cd demo
python demo_cli.py

# Web UI (Streamlit)
cd demo
streamlit run web_ui.py
```

---

## Files

```
msrv-public-demo/
├── demo/
│   ├── engine.py              ← Core demo engine (Fracture governance enforced)
│   ├── demo_cli.py            ← CLI interface
│   ├── web_ui.py              ← Streamlit web UI
│   └── public_samples.json    ← Sample data
├── docs/
│   ├── ARCHITECTURE_OVERVIEW.md
│   ├── FAQ.md
│   └── GOVERNANCE_PHILOSOPHY.md
├── report/
│   ├── BENCHMARK_REPORT.md    ← Full benchmark report
│   ├── benchmark_*_summary.json
│   └── benchmark_*_details.jsonl
├── tools/
│   └── msrv_benchmark_unified.py
└── README.md
```

---

## Dataset Composition

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

## License / Notice

This is a **public demo** intended to showcase the white-box control concept and benchmark evidence.

This repository provides a public demo interface and benchmark artifacts.
The proprietary MSR-V core engine, policy logic, and advanced parsers are not included in this release.

**The public demo enforces the same Fracture→STANDARD+ governance rule as the proprietary engine.**
