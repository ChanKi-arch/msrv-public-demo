#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI demo for MSR-V Public Demo Engine v2.5.5."""

import argparse
import json
from engine import MSRVPublicEngine


def main():
    ap = argparse.ArgumentParser(description="MSR-V Public Demo CLI v2.5.5")
    ap.add_argument("--lang", default="EN", choices=["EN", "KO"], help="Language (EN or KO)")
    ap.add_argument("--text", default=None, help="Input text to inspect")
    ap.add_argument("--mode", default="balanced", choices=["conservative", "balanced", "aggressive"],
                    help="Engine mode (default: balanced)")
    ap.add_argument("--interactive", action="store_true", help="Interactive loop mode")
    ap.add_argument("--info", action="store_true", help="Show mode information")
    args = ap.parse_args()

    eng = MSRVPublicEngine(mode=args.mode)

    if args.info:
        print(json.dumps(eng.get_mode_info(), ensure_ascii=False, indent=2))
        return

    if args.interactive or not args.text:
        print("=" * 70)
        print(f"MSR-V Public Demo v2.5.5 (mode: {args.mode})")
        print("Commands: 'exit' to quit, 'mode <name>' to switch mode")
        print("Routes: MINI (low-cost) / STANDARD (balanced) / PREMIUM (full)")
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
            out = eng.inspect(t, lang=args.lang)
            print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        out = eng.inspect(args.text, lang=args.lang)
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
