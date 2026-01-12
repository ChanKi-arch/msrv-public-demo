#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streamlit Web UI for MSR-V Public Demo v2.5.5-patch."""

import json
import glob
import os
import streamlit as st
from engine import MSRVPublicEngine

st.set_page_config(page_title="MSR-V Public Demo v2.5.5", layout="wide")
st.title("MSR-V White Engine - Public Demo v2.5.5")

st.info(
    "**This demo enforces the same Fracture→PREMIUM governance rule** "
    "as the proprietary MSR-V White Engine. "
    "Fracture state inputs are always routed to STANDARD or PREMIUM, never MINI."
)

# Mode selection
st.sidebar.header("⚙️ Engine Settings")
mode = st.sidebar.selectbox(
    "Engine Mode",
    ["conservative", "balanced", "aggressive"],
    index=1,
    help="CONSERVATIVE: Maximum safety | BALANCED: Default | AGGRESSIVE: Maximum cost savings"
)

mode_descriptions = {
    "conservative": "🔒 **CONSERVATIVE**: MINI disabled, all inputs verified at STANDARD+",
    "balanced": "⚖️ **BALANCED**: Cost-safety balance, recommended for general use",
    "aggressive": "🚀 **AGGRESSIVE**: Maximum MINI routing for cost optimization",
}
st.sidebar.markdown(mode_descriptions[mode])

eng = MSRVPublicEngine(mode=mode)

# Mode info
with st.sidebar.expander("📊 Mode Thresholds"):
    info = eng.get_mode_info()
    st.json(info["thresholds"])

# Governance rules
with st.sidebar.expander("🔒 Governance Rules"):
    st.markdown("""
    **Fracture → MINI: BLOCKED**
    - Fracture state always routes to STANDARD or PREMIUM
    - Matches proprietary MSR-V White Engine rules
    
    **short_sig_cap:**
    - Only applied when is_fracture=False
    - Blocked for high_stakes inputs
    """)

st.sidebar.divider()
st.sidebar.markdown("""
### Route Tiers (v2.5.5)
| Tier | Cost | Description |
|------|------|-------------|
| **MINI** | 2% | Local/domestic LLM |
| **STANDARD** | 30% | Budget global LLM |
| **PREMIUM** | 100% | Premium global LLM |
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    lang = st.selectbox("Language", ["EN", "KO"], index=0)
    text = st.text_area("Input", height=140, placeholder="Paste a sentence...")
    run = st.button("🔍 Inspect", type="primary")

with col2:
    st.subheader("Output Fields")
    st.markdown(
        """
- **Route**: MINI / STANDARD / PREMIUM
- **State4**: Harmony / Divergence / Alignment / Fracture
- **Zs**: Structural stability index
- **Theta**: Internal tension index
- **is_fracture**: Fracture state indicator
- **short_sig_cap_applied**: Short-signal cap status
"""
    )

if run:
    if not text.strip():
        st.warning("Please enter input text first.")
    else:
        out = eng.inspect(text, lang=lang)
        
        # Route indicator
        route = out["output"]["route"]
        state4 = out["output"]["state4"]
        route_colors = {"MINI": "green", "STANDARD": "blue", "PREMIUM": "red"}
        route_icons = {"MINI": "🟢", "STANDARD": "🔵", "PREMIUM": "🔴"}
        
        st.subheader("Result")
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.metric("Route", f"{route_icons.get(route, '')} {route}")
        with col_r2:
            st.metric("State4", state4)
        with col_r3:
            st.metric("Zs", f"{out['output'].get('Zs', 0):.4f}")
        with col_r4:
            is_fracture = out["output"].get("route_reason", {}).get("is_fracture", False)
            st.metric("Fracture", "⚠️ YES" if is_fracture else "✅ NO")
        
        # Governance check
        if is_fracture and route == "MINI":
            st.error("⚠️ GOVERNANCE VIOLATION: Fracture routed to MINI!")
        elif is_fracture:
            st.success(f"✅ Governance enforced: Fracture → {route}")
        
        st.json(out)

st.divider()

# Benchmark summary - UPDATED WITH PATCHED RESULTS
st.subheader("📊 Benchmark Results (4,200 Samples)")

benchmark_data = {
    "Mode": ["🔒 CONSERVATIVE", "⚖️ BALANCED", "🚀 AGGRESSIVE"],
    "MINI": ["0 (0.0%)", "961 (22.9%)", "2,444 (58.2%)"],
    "STANDARD": ["3,817 (90.9%)", "2,856 (68.0%)", "1,374 (32.7%)"],
    "PREMIUM": ["383 (9.1%)", "383 (9.1%)", "382 (9.1%)"],
    "Cost Savings": ["63.6%", "70.0%", "79.9%"],
    "Fracture→MINI": ["0 ✅", "0 ✅", "0 ✅"],
}

import pandas as pd
df = pd.DataFrame(benchmark_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.success("✅ **All 382 Fracture samples correctly routed to STANDARD/PREMIUM across all modes.**")

st.divider()
st.subheader("📁 Bundled Reports")

# Look for reports in report directory
report_dir = os.path.join(os.path.dirname(__file__), "..", "report")
if os.path.exists(report_dir):
    reports = glob.glob(os.path.join(report_dir, "*.md"))
    reports = sorted(reports)
    
    if reports:
        choice = st.selectbox("Select Report", [os.path.basename(r) for r in reports], index=0)
        for r in reports:
            if os.path.basename(r) == choice:
                with open(r, "r", encoding="utf-8") as f:
                    st.markdown(f.read())
                break
    else:
        st.info("No report files found in report directory.")
else:
    st.info("Report directory not found.")
