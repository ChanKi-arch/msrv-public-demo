#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""msrv_public_engine.py

Public-demo engine for MSR-V White Engine v2.5.5-final.

This is **NOT** the proprietary MSR-V core.
It provides a stable, deterministic interface and can replay
precomputed benchmark traces (route/state/Zs/theta) shipped in this repo.

Why:
- protects IP
- still demonstrates governance outputs + traceability

Changes in v2.5.5:
- Route naming: BYPASS→MINI, LITE→STANDARD, FULL→PREMIUM
- 3-Mode system: CONSERVATIVE, BALANCED, AGGRESSIVE
- Runtime mode switching support
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from enum import Enum
import json
import os
import difflib


class EngineMode(Enum):
    """Engine operation modes"""
    CONSERVATIVE = "conservative"  # MINI disabled, maximum safety
    BALANCED = "balanced"          # Default, cost-safety balance
    AGGRESSIVE = "aggressive"      # Maximum cost savings


class RouteTier(Enum):
    """Routing tiers (v2.5.5 naming)"""
    MINI = "MINI"           # Formerly BYPASS: Local/domestic LLM
    STANDARD = "STANDARD"   # Formerly LITE: Budget global LLM
    PREMIUM = "PREMIUM"     # Formerly FULL: Premium global LLM


@dataclass
class MSRVResult:
    text: str
    lang: str
    route: str
    state4: str
    zs: Optional[float] = None
    theta: Optional[float] = None
    shape: Optional[str] = None
    need: Optional[float] = None
    notes: Optional[str] = None


class MSRVPublicEngine:
    """Public demo engine with 3-mode support"""
    
    # Mode-specific thresholds (simplified for demo)
    MODE_THRESHOLDS = {
        "conservative": {"mini_base": 0.05, "standard_base": 0.55},
        "balanced": {"mini_base": 0.25, "standard_base": 0.55},
        "aggressive": {"mini_base": 0.35, "standard_base": 0.55},
    }
    
    def __init__(self, samples_path: str = None, mode: str = "balanced"):
        if samples_path is None:
            samples_path = os.path.join(os.path.dirname(__file__), "public_samples.json")
        self.samples_path = samples_path
        self.samples: List[Dict[str, Any]] = []
        self._mode = mode

        if os.path.exists(samples_path):
            with open(samples_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.samples = self._normalize_samples(raw)

    @property
    def mode(self) -> str:
        return self._mode
    
    def set_mode(self, mode: str) -> None:
        """Switch engine mode at runtime"""
        if mode not in self.MODE_THRESHOLDS:
            raise ValueError(f"Invalid mode: {mode}. Use: conservative, balanced, aggressive")
        self._mode = mode

    def _normalize_samples(self, raw: Any) -> List[Dict[str, Any]]:
        """Normalize loaded samples into a flat list[dict]."""
        flat: List[Dict[str, Any]] = []

        def walk(x: Any) -> None:
            if isinstance(x, dict):
                flat.append(x)
                return
            if isinstance(x, list):
                for y in x:
                    walk(y)
                return

        walk(raw)

        cleaned: List[Dict[str, Any]] = []
        for s in flat:
            if "text" not in s:
                continue
            if "lang" not in s:
                s["lang"] = "EN"
            # Convert old route names to new
            if "route" in s:
                s["route"] = self._convert_route(s["route"])
            cleaned.append(s)

        return cleaned

    def _convert_route(self, route: str) -> str:
        """Convert old route names to new naming"""
        route_upper = (route or "").upper()
        if "BYPASS" in route_upper:
            return "MINI"
        elif "LITE" in route_upper:
            return "STANDARD"
        elif "FULL" in route_upper:
            return "PREMIUM"
        elif route_upper in ("MINI", "STANDARD", "PREMIUM"):
            return route_upper
        return "STANDARD"

    def inspect(self, text: str, lang: str = "EN") -> Dict[str, Any]:
        """Return a deterministic 'governance trace' for the given text.

        Strategy:
        1) exact match in shipped samples
        2) fuzzy nearest neighbor among shipped samples
        3) fallback heuristic that respects current mode
        """
        text_norm = (text or "").strip()
        if not text_norm:
            return self._pack(
                text, lang,
                route="MINI", state4="Harmony", zs=0.95,
                theta=0.0, shape="POINT", need=0.0,
                notes="Empty input -> MINI"
            )

        # exact match
        for s in self.samples:
            if s.get("lang", "").upper() == lang.upper() and (s.get("text", "").strip() == text_norm):
                return self._from_sample(s, match="exact")

        # fuzzy match (same language first)
        candidates = [s for s in self.samples if s.get("lang", "").upper() == lang.upper()]
        if not candidates:
            candidates = self.samples

        best: Optional[Dict[str, Any]] = None
        best_score = 0.0
        for s in candidates:
            t = (s.get("text", "") or "").strip()
            if not t:
                continue
            score = difflib.SequenceMatcher(a=text_norm, b=t).ratio()
            if score > best_score:
                best_score = score
                best = s

        if best is not None and best_score >= 0.72:
            out = self._from_sample(best, match=f"fuzzy:{best_score:.2f}")
            out["meta"]["nearest_text"] = best.get("text", "")
            return out

        # Mode-aware conservative fallback
        return self._fallback_heuristic(text_norm, lang)

    def _fallback_heuristic(self, text: str, lang: str) -> Dict[str, Any]:
        """Apply mode-aware fallback heuristic"""
        thresholds = self.MODE_THRESHOLDS[self._mode]
        mini_base = thresholds["mini_base"]
        standard_base = thresholds["standard_base"]
        
        lower = text.lower()
        has_numbers = any(ch.isdigit() for ch in text)
        risky_claim = any(k in lower for k in ["100%", "guarantee", "cure", "always", "never", "perfect"])
        negation = any(k in lower for k in ["not", "never", "no "]) or any(k in text for k in ["아니다", "않", "못", "없"])
        high_stakes = any(k in lower for k in ["법", "의료", "금융", "law", "medical", "financial"])

        # Calculate need score
        need = 0.35 + (0.15 if has_numbers else 0.0) + (0.15 if risky_claim else 0.0) + (0.10 if negation else 0.0)
        need = min(1.0, need)
        
        # Mode-aware routing
        if self._mode == "conservative":
            # MINI disabled in conservative mode
            if need <= standard_base:
                route = "STANDARD"
            else:
                route = "PREMIUM"
        else:
            # high_stakes blocks MINI
            if high_stakes:
                need = max(need, mini_base + 0.01)
            
            if need <= mini_base:
                route = "MINI"
            elif need <= standard_base:
                route = "STANDARD"
            else:
                route = "PREMIUM"
        
        # State4 classification
        if negation and risky_claim:
            state4 = "Fracture"
            zs = 0.35
        elif negation:
            state4 = "Divergence"
            zs = 0.55
        elif risky_claim:
            state4 = "Alignment"
            zs = 0.65
        else:
            state4 = "Harmony"
            zs = 0.72
        
        theta = 0.35 if risky_claim else 0.18
        shape = "TRIANGLE" if (has_numbers or risky_claim) else "LINE"

        return self._pack(
            text=text, lang=lang, route=route, state4=state4, zs=zs, theta=theta, shape=shape, need=need,
            notes=f"Public fallback heuristic (mode={self._mode}). For real evaluation, run the proprietary engine."
        )

    def _from_sample(self, s: Dict[str, Any], match: str) -> Dict[str, Any]:
        route = self._convert_route(s.get("route", "STANDARD"))
        
        # Apply mode constraint
        if self._mode == "conservative" and route == "MINI":
            route = "STANDARD"
        
        return self._pack(
            text=s.get("text", ""),
            lang=s.get("lang", "EN"),
            route=route,
            state4=s.get("state4") or "Harmony",
            zs=s.get("zs"),
            theta=s.get("theta"),
            shape=s.get("shape"),
            need=s.get("need"),
            notes=(s.get("notes") or "") + (f" | match={match} | mode={self._mode}" if match else "")
        )

    def _pack(
        self, text: str, lang: str, route: str, state4: str,
        zs: Optional[float], theta: Optional[float], shape: Optional[str],
        need: Optional[float], notes: str
    ) -> Dict[str, Any]:
        return {
            "input": {"text": text, "lang": lang},
            "output": {
                "route": route,
                "state4": state4,
                "Zs": zs,
                "theta": theta,
                "shape": shape,
                "need": need,
            },
            "meta": {
                "engine": "MSRV-Public-Demo-v2.5.5",
                "mode": self._mode,
                "proprietary_core": False,
                "notes": notes,
            }
        }
    
    def get_mode_info(self) -> Dict[str, Any]:
        """Get information about current mode"""
        return {
            "current_mode": self._mode,
            "thresholds": self.MODE_THRESHOLDS[self._mode],
            "modes_available": list(self.MODE_THRESHOLDS.keys()),
            "mode_descriptions": {
                "conservative": "MINI disabled, maximum safety for pilot/trust-building",
                "balanced": "Default mode, cost-safety balance for general operation",
                "aggressive": "Maximum MINI routing for cost optimization",
            }
        }
