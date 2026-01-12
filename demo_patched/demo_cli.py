#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI demo for MSR-V Public Demo Engine v2.5.5-patch."""

import argparse
import json
from engine import MSRVPublicEngine


def main():
    ap = argparse.ArgumentParser(description="MSR-V Public Demo CLI v2.5.5-patch")
    ap.add_argument("--lang", default="EN", choices=["EN", "KO"], help="Language (EN or KO)")
    ap.add_argument("--text", default=None, help="Input text to inspect")
    ap.add_argument("--mode", default="balanced", choices=["conservative", "balanced", "aggressive"],
                    help="Engine mode (default: balanced)")
    ap.add_argument("--interactive", action="store_true", help="Interactive loop mode")
    ap.add_argument("--info", action="store_true", help="Show mode information")
    ap.add_argument("--governance", action="store_true", help="Show governance rules")
    args = ap.parse_args()

    eng = MSRVPublicEngine(mode=args.mode)

    if args.info:
        print(json.dumps(eng.get_mode_info(), ensure_ascii=False, indent=2))
        return

    if args.governance:
        print("=" * 60)
        print("MSR-V Governance Rules (v2.5.5-patch)")
        print("=" * 60)
        print("""
🔒 FRACTURE → MINI PREVENTION
   - Fracture state MUST route to STANDARD or PREMIUM
   - Never routed to MINI regardless of mode
   - Matches proprietary MSR-V White Engine rules

📊 SHORT_SIG_CAP
   - Only applied when is_fracture=False
   - Blocked for high_stakes inputs
   - Allows cost optimization for safe, short inputs

✅ VALIDATION
   - 382 Fracture samples in benchmark
   - 0 routed to MINI across all modes
   - 100% governance compliance
        """)
        return

    if args.interactive or not args.text:
        print("=" * 70)
        print(f"MSR-V Public Demo v2.5.5-patch (mode: {args.mode})")
        print("Commands: 'exit' to quit, 'mode <n>' to switch mode, 'gov' for governance")
        print("Routes: MINI (low-cost) / STANDARD (balanced) / PREMIUM (full)")
        print("🔒 Fracture → MINI: BLOCKED (governance enforced)")
        print("=" * 70)
        while True:
            try:
                t = input(f"[{eng.mode}]> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break
            if t.lower() in ("exit", "quit", "q"):
                break
            if t.lower().startswith("mode "):
                new_mode = t.split()[1].lower()
                try:
                    eng.set_mode(new_mode)
                    print(f"Mode switched to: {new_mode}")
                except ValueError as e:
                    print(f"Error: {e}")
                continue
            if t.lower() == "info":
                print(json.dumps(eng.get_mode_info(), ensure_ascii=False, indent=2))
                continue
            if t.lower() in ("gov", "governance"):
                info = eng.get_mode_info()
                print("\n🔒 Governance Rules:")
                print(json.dumps(info.get("governance_rules", {}), ensure_ascii=False, indent=2))
                continue
            out = eng.inspect(t, lang=args.lang)
            
            # Highlight governance enforcement
            route_reason = out.get("output", {}).get("route_reason", {})
            is_fracture = route_reason.get("is_fracture", False)
            route = out.get("output", {}).get("route", "STANDARD")
            
            if is_fracture:
                print(f"🔒 Fracture detected → Routed to {route} (MINI blocked)")
            
            print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        out = eng.inspect(args.text, lang=args.lang)
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
