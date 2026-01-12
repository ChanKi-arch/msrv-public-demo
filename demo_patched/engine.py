#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""msrv_public_engine.py

Public-demo engine for MSR-V White Engine v2.5.5-patch.

This is **NOT** the proprietary MSR-V core.
It provides a stable, deterministic interface and can replay
precomputed benchmark traces (route/state/Zs/theta) shipped in this repo.

PATCH NOTES (v2.5.5-patch):
- Fracture → MINI prevention: Fracture state MUST route to STANDARD or PREMIUM
- Added route_reason with is_fracture, short_sig_cap_applied for white-box tracing
- Aligned with proprietary MSR-V White Engine governance rules

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
    """Public demo engine with 3-mode support and Fracture governance"""
    
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
            
            # PATCH: Enforce Fracture → STANDARD/PREMIUM rule in samples
            if s.get("state4") == "Fracture" and s.get("route") == "MINI":
                s["route"] = "STANDARD"
            
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
        3) fallback heuristic that respects current mode AND Fracture governance
        """
        text_norm = (text or "").strip()
        if not text_norm:
            return self._pack(
                text, lang,
                route="MINI", state4="Harmony", zs=0.95,
                theta=0.0, shape="POINT", need=0.0,
                is_fracture=False, short_sig_cap_applied=False,
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

        # Mode-aware conservative fallback with Fracture governance
        return self._fallback_heuristic(text_norm, lang)

    def _fallback_heuristic(self, text: str, lang: str) -> Dict[str, Any]:
        """Apply mode-aware fallback heuristic with Fracture governance"""
        thresholds = self.MODE_THRESHOLDS[self._mode]
        mini_base = thresholds["mini_base"]
        standard_base = thresholds["standard_base"]
        
        lower = text.lower()
        char_len = len(text)
        has_numbers = any(ch.isdigit() for ch in text)
        risky_claim = any(k in lower for k in ["100%", "guarantee", "cure", "always", "never", "perfect", "죽", "kill", "법적", "소송"])
        negation = any(k in lower for k in ["not", "never", "no "]) or any(k in text for k in ["아니다", "않", "못", "없"])
        high_stakes = any(k in lower for k in ["법", "의료", "금융", "law", "medical", "financial", "contract", "계약"])

        # Calculate need score
        need = 0.35 + (0.15 if has_numbers else 0.0) + (0.15 if risky_claim else 0.0) + (0.10 if negation else 0.0)
        need = min(1.0, need)
        
        # ================================================================
        # PATCH: State4 classification with proper Fracture detection
        # ================================================================
        # Fracture = structural breakdown (risky + negation combined)
        if negation and risky_claim:
            state4 = "Fracture"
            zs = 0.32
        elif risky_claim:
            state4 = "Alignment"
            zs = 0.55
        elif negation:
            state4 = "Divergence"
            zs = 0.60
        else:
            state4 = "Harmony"
            zs = 0.72
        
        # ================================================================
        # PATCH: Fracture governance rule (matches proprietary engine)
        # Fracture → MUST route to STANDARD or PREMIUM, never MINI
        # ================================================================
        is_fracture = (state4 == "Fracture")
        short_sig_cap_applied = False
        
        if is_fracture:
            # Fracture floor: need >= 0.65 (weak fracture minimum)
            need = max(need, 0.65)
            # Fracture MUST go to PREMIUM (or at least STANDARD)
            route = "PREMIUM"
        else:
            # Mode-aware routing for non-Fracture
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
                
                # Short signal cap (only for non-Fracture, non-high_stakes)
                if char_len < 30 and not high_stakes:
                    short_sig_cap_applied = True
                    # Allow MINI for very short, safe inputs
                    if need > mini_base:
                        need = mini_base
                
                if need <= mini_base:
                    route = "MINI"
                elif need <= standard_base:
                    route = "STANDARD"
                else:
                    route = "PREMIUM"
        
        theta = 0.35 if risky_claim else 0.18
        shape = "TRIANGLE" if (has_numbers or risky_claim) else "LINE"

        return self._pack(
            text=text, lang=lang, route=route, state4=state4, zs=zs, 
            theta=theta, shape=shape, need=need,
            is_fracture=is_fracture, short_sig_cap_applied=short_sig_cap_applied,
            notes=f"Public fallback heuristic (mode={self._mode}). Fracture governance enforced."
        )

    def _from_sample(self, s: Dict[str, Any], match: str) -> Dict[str, Any]:
        route = self._convert_route(s.get("route", "STANDARD"))
        state4 = s.get("state4") or "Harmony"
        is_fracture = (state4 == "Fracture")
        
        # PATCH: Enforce Fracture governance even for matched samples
        if is_fracture and route == "MINI":
            route = "STANDARD"
        
        # Apply mode constraint (conservative disables MINI)
        if self._mode == "conservative" and route == "MINI":
            route = "STANDARD"
        
        return self._pack(
            text=s.get("text", ""),
            lang=s.get("lang", "EN"),
            route=route,
            state4=state4,
            zs=s.get("zs"),
            theta=s.get("theta"),
            shape=s.get("shape"),
            need=s.get("need"),
            is_fracture=is_fracture,
            short_sig_cap_applied=False,
            notes=(s.get("notes") or "") + (f" | match={match} | mode={self._mode}" if match else "")
        )

    def _pack(
        self, text: str, lang: str, route: str, state4: str,
        zs: Optional[float], theta: Optional[float], shape: Optional[str],
        need: Optional[float], is_fracture: bool, short_sig_cap_applied: bool,
        notes: str
    ) -> Dict[str, Any]:
        """Pack result with route_reason for white-box tracing"""
        return {
            "input": {"text": text, "lang": lang},
            "output": {
                "route": route,
                "state4": state4,
                "Zs": zs,
                "theta": theta,
                "shape": shape,
                "need": need,
                "route_reason": {
                    "need": need,
                    "is_fracture": is_fracture,
                    "short_sig_cap_applied": short_sig_cap_applied,
                    "mode": self._mode,
                    "governance": "Fracture→MINI blocked" if is_fracture else "normal",
                }
            },
            "meta": {
                "engine": "MSRV-Public-Demo-v2.5.5-patch",
                "mode": self._mode,
                "proprietary_core": False,
                "fracture_governance": True,  # PATCH: Governance flag
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
            },
            "governance_rules": {
                "fracture_to_mini": "BLOCKED - Fracture state always routes to STANDARD or PREMIUM",
                "short_sig_cap": "Applied only when is_fracture=False and high_stakes=False",
            }
        }
