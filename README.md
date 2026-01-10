![Version](https://img.shields.io/badge/version-2.5.5--final-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Samples](https://img.shields.io/badge/benchmark-4%2C200%20samples-orange)
![Cost Reduction](https://img.shields.io/badge/cost%20reduction-up%20to%2083.7%25-brightgreen)

# MSR-V Public Demo (v2.5.5-final)

**White-box Structural Routing & Control Layer for LLM Orchestration**  
*Control reasoning depth, not tokens.*

---

## 🚀 Overview

MSR-V is a **white-box governance layer** that decides *how much reasoning* is structurally necessary — **before** the LLM runs.

It is *not* a model itself.  
It enables **cost reduction with safety controls** using deterministic, traceable routing logic.

This repository provides a **fully reproducible public demo** including:

- **Public demo routing engine**
- CLI & Web UI interfaces
- **Complete benchmark artifacts** (4,200 samples)
- Machine-readable and human-readable evaluation results

---

## 📦 Download

| Format | Link |
|--------|------|
| **ZIP** | [v2.5.5-final.zip](https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-final.zip) |
| **TAR.GZ** | [v2.5.5-final.tar.gz](https://github.com/ChanKi-arch/msrv-public-demo/archive/refs/tags/v2.5.5-final.tar.gz) |
| **Release** | [Releases Page](https://github.com/ChanKi-arch/msrv-public-demo/releases/tag/v2.5.5-final) |
> Note: ZIP/TAR.GZ are source archives generated from the Git tag.
---

## 📌 Key Concepts

| Term | Description |
|------|-------------|
| **Engine** | Structural routing and scoring engine (public demo version) |
| **Tier** | MINI / STANDARD / PREMIUM (cost vs. quality levels) |
| **Mode** | CONSERVATIVE / BALANCED / AGGRESSIVE runtime presets |
| **Routing** | Deterministic selection of tier per request |

> **Naming Note**: Legacy docs may reference `BYPASS / LITE / FULL` — these map 1:1 to `MINI / STANDARD / PREMIUM`.

---

## 📊 Benchmark Results (v2.5.5-final)

**Total Samples:** 4,200 (Korean & English × Normal / Negation / Hard)  
**Structural Alignment:** 89.8%  
**Governance Latency:** 0.3–2 ms

| Mode | MINI | STANDARD | PREMIUM | Cost Reduction |
|------|-----:|--------:|--------:|---------------:|
| 🔒 **CONSERVATIVE** | 0 (0.0%) | 3,810 (90.7%) | 390 (9.3%) | 63.5% |
| ⚖️ **BALANCED** | 1,019 (24.3%) | 2,873 (68.4%) | 308 (7.3%) | 71.7% |
| 🚀 **AGGRESSIVE** | 2,595 (61.8%) | 1,387 (33.0%) | 218 (5.2%) | **83.7%** |

Full details: [`report/benchmark_report.md`](report/benchmark_report.md), [`BENCHMARK_SUMMARY.md`](BENCHMARK_SUMMARY.md)

---

## 🎛️ Mode Selection

| Mode | Use Case | MINI Routing |
|------|----------|--------------|
| 🔒 **CONSERVATIVE** | Pilot / regulated / safety-critical | Disabled |
| ⚖️ **BALANCED** | General production (recommended) | Moderate |
| 🚀 **AGGRESSIVE** | Cost-optimized with trusted MINI | Maximized |

---

## 📍 Quick Start
```bash
git clone https://github.com/ChanKi-arch/msrv-public-demo
cd msrv-public-demo
git checkout v2.5.5-final
pip install -r requirements.txt

# CLI Demo
python demo/demo_cli.py

# Web UI
streamlit run demo/web_ui.py
```

---

## 🧪 Reproduce Benchmarks
```bash
python tools/msrv_benchmark_unified.py \
  --mode balanced \
  --output report/benchmark_report.md \
  --summary-json report/benchmark_summary.json
```

**Generated artifacts:**
- `report/benchmark_*_summary.json` — Aggregated metrics
- `report/benchmark_*_details.jsonl` — Per-sample traces
- `report/benchmark_report.md` — Human-readable report

---

## 📁 Repository Structure
```
msrv-public-demo/
├── demo/
│   ├── engine.py              # Public demo engine
│   ├── demo_cli.py            # CLI interface
│   ├── web_ui.py              # Streamlit Web UI
│   └── public_samples.json    # Sample data
├── docs/
│   ├── ARCHITECTURE_OVERVIEW.md
│   ├── FAQ.md
│   └── GOVERNANCE_PHILOSOPHY.md
├── report/
│   ├── benchmark_report.md
│   ├── benchmark_*_summary.json
│   └── benchmark_*_details.jsonl
├── tools/
│   └── msrv_benchmark_unified.py
├── BENCHMARK_SUMMARY.md
├── README.md
├── LICENSE
└── requirements.txt
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE_OVERVIEW.md](docs/ARCHITECTURE_OVERVIEW.md) | Structural routing architecture |
| [FAQ.md](docs/FAQ.md) | Frequently asked questions |
| [GOVERNANCE_PHILOSOPHY.md](docs/GOVERNANCE_PHILOSOPHY.md) | Safety & governance design |
| [BENCHMARK_SUMMARY.md](BENCHMARK_SUMMARY.md) | Quick benchmark overview |

---

## 🔐 IP & Safety Notice

This repository contains a **public demo engine** and **reproducible benchmark artifacts**.

The proprietary MSR-V production engine, provider gateways, tuning logic, and credentials are **not included**.

---

## 📄 License

[Apache License 2.0](LICENSE)

---

<p align="center">
<strong>MSR-V White Engine</strong><br/>
Control reasoning depth, not tokens.
</p>
