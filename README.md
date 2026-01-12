![Version](https://img.shields.io/badge/version-2.5.5--patch-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Samples](https://img.shields.io/badge/benchmark-4%2C200%20samples-orange)
![Cost Reduction](https://img.shields.io/badge/cost%20reduction-up%20to%2079.9%25-brightgreen)

# MSR-V White Engine — Public Demo (v2.5.5-patch)

**White-box Structural Routing & Control Layer for LLM Orchestration**  
Control reasoning depth, not tokens.

---

## 🚀 Overview

MSR-V is a white-box governance layer that decides **how much reasoning / which tier is structurally necessary — before an LLM runs.**

- It is **not a model** itself.
- It enables **cost reduction** with explicit safety controls using **deterministic, traceable routing logic**.

This repository provides a fully reproducible public demo including:

- Public demo routing engine
- CLI & Web UI interfaces
- Complete benchmark artifacts (4,200 samples)
- Machine-readable and human-readable evaluation results
- Gateway benchmark artifacts (adapter/gateway path)

---

## 🛡 Public Demo Clarification (IP / Safety)

This repository is a public, reproducible demo of the MSR-V governance architecture.

It demonstrates:

- routing logic
- structural classification
- trace fields
- benchmark reproducibility

…without exposing proprietary production internals (advanced parsers, private policy tuning logic, provider-side details, credentials).

Some components may use heuristic fallback and/or precomputed samples to preserve interface behavior while keeping the core IP protected.

> This demo is intended for architectural inspection and governance evaluation  
> (i.e., “Is routing deterministic, traceable, and safe?”),  
> not for claiming real-world model accuracy or domain truthfulness.

---

## 🔒 Governance Rule (v2.5.5-patch)

The public demo enforces the same **Fracture → STANDARD/PREMIUM** governance rule  
as the proprietary MSR-V White Engine, even when heuristic fallback is used.

**Fracture state → MUST route to STANDARD or PREMIUM, NEVER MINI**

---

## 📦 Download

| Format | Link |
|---|---|
| ZIP | https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-patch.zip |
| TAR.GZ | https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-patch.tar.gz |
| Release | https://github.com/ChanKi-arch/msrv-public-demo/releases/tag/v2.5.5-patch |

> Note: ZIP/TAR.GZ are source archives generated from the Git tag.

---

## 📌 Key Concepts

| Term | Description |
|---|---|
| Engine | Structural routing and scoring engine (public demo version) |
| Tier | MINI / STANDARD / PREMIUM (cost vs. quality levels) |
| Mode | CONSERVATIVE / BALANCED / AGGRESSIVE runtime presets |
| Routing | Deterministic tier selection per request |

> Naming Note: Legacy docs may reference BYPASS / LITE / FULL — these map 1:1 to MINI / STANDARD / PREMIUM.

---

## 📊 Benchmark Results (v2.5.5-patch)

- **Benchmark date:** 2026-01-11  
- **Total samples:** 4,200 (KO/EN × Normal/Negation/Hard)  
- **Cost weights:** MINI=2, STANDARD=30, PREMIUM=100 (PREMIUM baseline)

| Mode | MINI | STANDARD | PREMIUM | Cost Reduction | Avg Latency | Fracture→MINI |
|---|---:|---:|---:|---:|---:|---:|
| CONSERVATIVE | 0 (0.0%) | 3817 (90.9%) | 383 (9.1%) | 63.6% | 0.87 ms | 0 |
| BALANCED | 961 (22.9%) | 2856 (68.0%) | 383 (9.1%) | 70.0% | 0.85 ms | 0 |
| AGGRESSIVE | 2444 (58.2%) | 1374 (32.7%) | 382 (9.1%) | 79.9% | 0.86 ms | 0 |

✅ **Safety Validation:** All Fracture samples correctly routed to STANDARD/PREMIUM (**0 → MINI**)

- Full report: `report/BENCHMARK_REPORT.md`
- Machine-readable: `report/benchmark_*_summary.json`, `report/benchmark_*_details.jsonl`

---

## 🧭 What “Gateway Benchmark” means

In addition to the engine benchmark, this repo includes gateway/adapter benchmark artifacts to show:

- routing + policy overhead in a gateway-ready path
- per-mode summaries
- detailed traces similar to the engine benchmark

- Gateway report: `Gateway report/gateway_benchmark_report.md`  
  (relative link: `Gateway%20report/gateway_benchmark_report.md`)
- Machine-readable: `Gateway report/gateway_*_summary.json`, `Gateway report/gateway_*_details.jsonl`  
  (relative links: `Gateway%20report/gateway_*_summary.json`, `Gateway%20report/gateway_*_details.jsonl`)

---

## 🎛️ Mode Selection

| Mode | Use Case | MINI Routing |
|---|---|---|
| CONSERVATIVE | Pilot / regulated / safety-critical | Effectively disabled |
| BALANCED | General production (recommended) | Moderate |
| AGGRESSIVE | Cost-optimized with trusted MINI | Maximized |

---

## 📍 Quick Start

```bash
pip install -r requirements.txt

# CLI
python demo/demo_cli.py

# Web UI (Streamlit)
streamlit run demo/web_ui.py


---

🧪 Reproduce Benchmarks

python tools/msrv_benchmark_unified.py \
  --mode balanced \
  --output report/BENCHMARK_REPORT.md \
  --summary-json report/benchmark_balanced_summary.json

Generated artifacts:

report/benchmark_*_summary.json — Aggregated metrics

report/benchmark_*_details.jsonl — Per-sample traces

report/BENCHMARK_REPORT.md — Human-readable report



---

📁 Repository Structure

msrv-public-demo/
├── demo/
│   ├── engine.py
│   ├── demo_cli.py
│   ├── web_ui.py
│   └── public_samples.json
├── docs/
│   ├── ARCHITECTURE_OVERVIEW.md
│   ├── FAQ.md
│   └── GOVERNANCE_PHILOSOPHY.md
├── report/
│   ├── BENCHMARK_REPORT.md
│   ├── benchmark_*_summary.json
│   └── benchmark_*_details.jsonl
├── Gateway report/
│   ├── gateway_benchmark_report.md
│   ├── gateway_*_summary.json
│   └── gateway_*_details.jsonl
├── tools/
│   └── msrv_benchmark_unified.py
├── README.md
├── LICENSE
└── requirements.txt


---

📚 Documentation

Document	Description

docs/ARCHITECTURE_OVERVIEW.md	Structural routing architecture
docs/FAQ.md	Frequently asked questions
docs/GOVERNANCE_PHILOSOPHY.md	Safety & governance design



---

🔐 IP & Safety Notice

This repository contains a public demo engine and reproducible benchmark artifacts.

The proprietary MSR-V production engine, advanced parsers, provider gateways, tuning logic, and any credentials are not included.


---

📄 License

Apache License 2.0 — see LICENSE


---

<p align="center">
  <strong>MSR-V White Engine</strong><br/>
  Control reasoning depth, not tokens.
</p>
