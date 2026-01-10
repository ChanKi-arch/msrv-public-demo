#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Streamlit Web UI for MSR-V Public Demo v2.5.5."""

import json
import glob
import os
import streamlit as st
from engine import MSRVPublicEngine

st.set_page_config(page_title="MSR-V Public Demo v2.5.5", layout="wide")
st.title("MSR-V White Engine - Public Demo v2.5.5")

st.warning(
    "**This demo does NOT run the real MSR-V engine.** "
    "It replays precomputed traces or applies conservative heuristics. "
    "The proprietary core is excluded to protect IP."
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
- **Shape**: Structural shape indicator
- **Mode**: Current engine mode
"""
    )

if run:
    if not text.strip():
        st.warning("Please enter input text first.")
    else:
        out = eng.inspect(text, lang=lang)
        
        # Route indicator
        route = out["output"]["route"]
        route_colors = {"MINI": "green", "STANDARD": "blue", "PREMIUM": "red"}
        route_icons = {"MINI": "🟢", "STANDARD": "🔵", "PREMIUM": "🔴"}
        
        st.subheader("Result")
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Route", f"{route_icons.get(route, '')} {route}")
        with col_r2:
            st.metric("State4", out["output"]["state4"])
        with col_r3:
            st.metric("Zs", f"{out['output'].get('Zs', 0):.4f}")
        
        st.json(out)

st.divider()

# Benchmark summary
st.subheader("📊 Benchmark Results (4,200 Samples)")

benchmark_data = {
    "Mode": ["🔒 CONSERVATIVE", "⚖️ BALANCED", "🚀 AGGRESSIVE"],
    "MINI": ["0 (0.0%)", "1,019 (24.3%)", "2,595 (61.8%)"],
    "STANDARD": ["3,810 (90.7%)", "2,873 (68.4%)", "1,387 (33.0%)"],
    "PREMIUM": ["390 (9.3%)", "308 (7.3%)", "218 (5.2%)"],
    "Cost Savings": ["63.5%", "71.7%", "83.7%"],
    "Use Case": ["Pilot/Trust", "General Ops", "Cost Optimize"],
}

import pandas as pd
df = pd.DataFrame(benchmark_data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("📁 Bundled Reports")

# Look for reports in current directory
report_patterns = ["REPORT_*.md", "BENCHMARK_*.md", "*.md"]
reports = []
for pattern in report_patterns:
    reports.extend(glob.glob(pattern))

# Filter out README
reports = [r for r in reports if "README" not in r]
reports = sorted(set(reports))

if reports:
    choice = st.selectbox("Select Report", [os.path.basename(r) for r in reports], index=0)
    for r in reports:
        if os.path.basename(r) == choice:
            with open(r, "r", encoding="utf-8") as f:
                st.markdown(f.read())
            break
else:
    st.info("No report files found in current directory.")
