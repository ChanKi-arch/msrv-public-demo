# FAQ

### Q: Is the proprietary MSR-V core engine included in this repository?

**A:** No. This repository provides an **IP-safe public demo** for validating governance behavior.  
The proprietary core engine is intentionally excluded to protect intellectual property.

---

### Q: What changed in v2.5.5?

**A:** Two major changes:
1. **Route naming**: BYPASS→MINI, LITE→STANDARD, FULL→PREMIUM
2. **3-Mode system**: CONSERVATIVE, BALANCED, AGGRESSIVE modes for runtime switching

---

### Q: What do MINI, STANDARD, and PREMIUM mean?

**A:** They are routing tiers that determine which LLM provider handles the request:

| Tier | Cost Weight | Example Models |
|------|-------------|----------------|
| **MINI** | 2 | HyperCLOVA X, local LLMs |
| **STANDARD** | 30 | GPT-3.5, Claude Haiku |
| **PREMIUM** | 100 | GPT-4o, Claude Sonnet/Opus |

---

### Q: How do I choose between modes?

**A:** 

| Mode | When to Use |
|------|-------------|
| 🔒 **CONSERVATIVE** | Pilot phase, building trust, regulated environments |
| ⚖️ **BALANCED** | General production use (recommended default) |
| 🚀 **AGGRESSIVE** | Cost-critical deployments with trusted MINI provider |

---

### Q: Is MSR-V a language model?

**A:** No. MSR-V does not generate text. It is a **deterministic governance layer** that controls reasoning execution depth.

---

### Q: Is MSR-V a fact-checker?

**A:** No. MSR-V does not judge factual truth.  
It detects **structural defects** and governs routing decisions.

---

### Q: Can MSR-V detect hallucinations?

**A:** No. MSR-V cannot detect factual hallucinations.  
If a sentence is structurally complete (e.g., "The Earth is flat"), MSR-V will pass it.  
MSR-V governs **structural integrity**, not factual correctness.

---

### Q: What does "Fracture" mean?

**A:** Fracture indicates a **structural defect**:
- Parsing failure
- Missing essential slots
- Unstable structural signals

It does NOT mean "factually false".

---

### Q: Why does routing differ between Korean and English?

**A:** Korean (agglutinative) often enables safer shallow passes (higher MINI in AGGRESSIVE mode).  
English (inflectional) tends to require more structural verification (higher STANDARD/PREMIUM).  
This reflects linguistic structure, not model bias.

---

### Q: What do Zs and Theta represent?

**A:** They are **internal governance signals**:
- **Zs**: Structural stability index (higher = more stable)
- **Theta (θ)**: Internal tension/torsion index (higher = more energy imbalance)

They are not probability-based confidence scores.

---

### Q: How is cost reduction calculated?

**A:** Cost reduction uses tier weights:

| Tier | Cost Weight |
|------|-------------|
| MINI | 2 |
| STANDARD | 30 |
| PREMIUM | 100 |

Formula:
```
Baseline = Total × 100 (all PREMIUM)
Actual = MINI × 2 + STANDARD × 30 + PREMIUM × 100
Savings = (Baseline - Actual) / Baseline × 100%
```

---

### Q: Can I switch modes at runtime?

**A:** Yes. The engine supports runtime mode switching:

```python
engine = MSRVPublicEngine(mode="balanced")
engine.set_mode("aggressive")  # Switch to aggressive
engine.set_mode("conservative")  # Switch to conservative
```

---

### Q: What happens to MINI routing in CONSERVATIVE mode?

**A:** MINI routing is **completely disabled** in CONSERVATIVE mode.  
All inputs are routed to STANDARD or PREMIUM only, ensuring maximum safety.

---

### Q: What is the "high_stakes" flag?

**A:** `high_stakes` is set when input contains sensitive patterns:
- Financial amounts (금액, 날짜)
- Legal/medical terms
- Regulatory language

When `high_stakes=True`, MINI routing is blocked even in BALANCED/AGGRESSIVE modes.

---

### Q: How do I get the best cost savings?

**A:** 
1. Use **AGGRESSIVE mode** for maximum savings (83.7%)
2. Ensure your MINI provider is reliable
3. Monitor Fracture rates to ensure quality
4. Start with BALANCED, gradually move to AGGRESSIVE

---

### Q: Is MSR-V compatible with any LLM provider?

**A:** Yes. MSR-V is provider-agnostic. The routing decision (MINI/STANDARD/PREMIUM) can be mapped to any LLM providers you use:
- MINI → Your low-cost option (local, domestic, etc.)
- STANDARD → Your mid-tier option
- PREMIUM → Your high-quality option
