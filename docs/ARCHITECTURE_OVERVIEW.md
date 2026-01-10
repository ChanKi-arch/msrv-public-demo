# MSR-V Architecture Overview

MSR-V (Merge-Split-Re-merge Visibility) is a **white-box structural governance layer** for LLM systems.

It evaluates the **structural integrity** of reasoning inputs/outputs and deterministically controls execution depth.

> MSR-V is NOT a fact-checker and does NOT judge factual truth.

---

## 1. Structural Governance Objective

LLM failures are often invisible to confidence scores because fluent text can still contain:
- Unstable definitions
- Invalid relations
- Impossible operations
- System/domain mismatches

MSR-V makes these structural risks observable and governable via explicit signals and routing.

---

## 2. Core Loop Concept (Merge-Split-Re-merge)

The internal engine design follows a deterministic governance loop:

- **Merge**: Compress structural primitives (D/R/O/S)
- **Split**: Explore alternative structural tensions
- **Re-merge**: Select stable configuration and determine execution necessity

This public repo demonstrates the **interfaces and behaviors**, not proprietary internals.

---

## 3. 3-Tier Deterministic Routing (v2.5.5)

MSR-V routes execution into three tiers:

| Route | Description | Cost Weight |
|-------|-------------|-------------|
| **MINI** | Low-cost local/domestic LLM | 2 |
| **STANDARD** | Budget global LLM | 30 |
| **PREMIUM** | Premium global LLM | 100 |

Routing is based on **structural necessity**, not probability.

### Route Naming History

| Version | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| v2.5.3 | BYPASS | LITE | FULL |
| v2.5.5 | **MINI** | **STANDARD** | **PREMIUM** |

---

## 4. 3-Mode System (v2.5.5)

MSR-V v2.5.5 introduces runtime mode switching:

| Mode | MINI Enabled | Use Case | Safety |
|------|--------------|----------|--------|
| 🔒 **CONSERVATIVE** | ❌ No | Pilot/trust-building | ⭐⭐⭐⭐⭐ |
| ⚖️ **BALANCED** | ✅ Yes | General operation | ⭐⭐⭐⭐ |
| 🚀 **AGGRESSIVE** | ✅ Max | Cost optimization | ⭐⭐⭐ |

```python
# Runtime mode switching
engine.set_mode("conservative")  # Pilot phase
engine.set_mode("balanced")      # Production
engine.set_mode("aggressive")    # Cost-critical
```

---

## 5. White-Box Traceability

MSR-V exposes governance decisions using interpretable signals:

| Signal | Description |
|--------|-------------|
| **State4** | Harmony / Alignment / Divergence / Fracture |
| **Zs** | Structural stability index (0-1) |
| **Theta (θ)** | Internal tension/torsion index |
| **Shape** | Structural shape indicator |
| **need** | Routing necessity score |
| **route_reason** | Detailed routing decision factors |

This enables audits, safe deployment, and system-level optimization.

---

## 6. Parser-Agnostic Design

MSR-V's core is the **Structural Physics Engine**, not the parser.

```
[Any Parser] -> JSON12 Slots -> DROS/FMEP -> V-Axis Energy
                                                |
                                    Physics Layer (theta, m, v)
                                                |
                                    Shape + State4 + Zs
                                                |
                                    Mode-Aware Routing
                                                |
                                    MINI / STANDARD / PREMIUM
```

The built-in rule-based parser is a reference implementation.  
Production deployments can substitute LLM-based parsers or domain-specific NLU.

---

## 7. Cost Calculation

Cost savings are calculated using tier weights:

```
Baseline Cost = Total × PREMIUM_WEIGHT (100)
Actual Cost = MINI × 2 + STANDARD × 30 + PREMIUM × 100
Savings = (Baseline - Actual) / Baseline × 100%
```

### Benchmark Results (4,200 Samples)

| Mode | MINI | STANDARD | PREMIUM | Cost Savings |
|------|------|----------|---------|--------------|
| CONSERVATIVE | 0% | 90.7% | 9.3% | 63.5% |
| BALANCED | 24.3% | 68.4% | 7.3% | 71.7% |
| AGGRESSIVE | 61.8% | 33.0% | 5.2% | **83.7%** |

---

## 8. Safety Mechanisms

### high_stakes Detection
- Financial amounts, dates, legal terms
- Medical/health keywords
- Regulatory language

When `high_stakes=True`, MINI routing is blocked regardless of mode.

### Fracture Handling
- Structural defects trigger PREMIUM routing
- Ensures complex inputs receive full analysis

---

## 9. Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
├─────────────────────────────────────────────────────────────────┤
│                      MSR-V Gateway                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Handler   │  │   Handler   │  │   Handler   │             │
│  │    (LLM)    │  │  (Search)   │  │ (Embedding) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                      MSR-V Engine                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Parser    │  │   Physics   │  │  Gatekeeper │             │
│  │  (12-Slot)  │  │   Engine    │  │  (Routing)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                      LLM Providers                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │    MINI     │  │  STANDARD   │  │   PREMIUM   │             │
│  │ (Local/KR)  │  │  (Budget)   │  │  (Premium)  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10. Version History

| Version | Changes |
|---------|---------|
| v2.5.3 | Lever-D optimization, EN parser improvements |
| v2.5.5 | Route renaming (MINI/STANDARD/PREMIUM), 3-mode system |
