#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSR-V Gateway v1.1.1 + Engine v2.5.5-patch-fracture 통합 벤치마크

테스트 항목:
1) backward-compat: BYPASS/LITE/FULL 문자열 처리 검증
2) 게이트웨이 라우팅 정확도 검증
3) 비용 절감 및 안전성 분석
"""

import sys
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Any

# ============================================================================
# 벤치마크 설정
# ============================================================================

ENGINE_PATH = "/home/claude/msrv_v255_unified_patched.py"
GATEWAY_PATH = "/home/claude/msrv_gateway_v11_patched.py"
SAMPLES_PATH = "/mnt/user-data/uploads/benchmark_balanced_details.jsonl"
OUTPUT_DIR = "/home/claude/gateway_benchmark_results"

MODES = ["conservative", "balanced", "aggressive"]

# ============================================================================
# 엔진 및 게이트웨이 로드
# ============================================================================

def load_modules():
    """엔진과 게이트웨이 모듈 로드"""
    
    # 엔진 로드
    with open(ENGINE_PATH, "r") as f:
        engine_code = f.read().split("if __name__ ==")[0]
        exec(engine_code, globals())
    
    # 게이트웨이 로드
    with open(GATEWAY_PATH, "r") as f:
        gateway_code = f.read().split("if __name__ ==")[0]
        exec(gateway_code, globals())
    
    print(f"✅ 엔진 버전: {globals().get('__version__', 'unknown')}")

# ============================================================================
# backward-compat 테스트
# ============================================================================

def test_backward_compat():
    """BYPASS/LITE/FULL 문자열 변환 테스트"""
    print("\n" + "=" * 80)
    print("🔄 backward-compat 테스트: BYPASS/LITE/FULL → MINI/STANDARD/PREMIUM")
    print("=" * 80)
    
    # 임시 게이트웨이 생성 (엔진 없이 _safe_route_from_str 테스트)
    cfg = globals()["ThresholdConfig"]()
    engine = globals()["MSRVEngineV25"](cfg)
    gateway = globals()["MSRVGateway"](engine)
    
    test_cases = [
        # 레거시 용어 (구버전)
        ("BYPASS", "MINI"),
        ("Bypass (no MSR)", "MINI"),
        ("bypass", "MINI"),
        ("LITE", "STANDARD"),
        ("Lite (v1.5 minimal)", "STANDARD"),
        ("lite", "STANDARD"),
        ("FULL", "PREMIUM"),
        ("Full (v2.5+)", "PREMIUM"),
        ("full", "PREMIUM"),
        # 신규 용어
        ("MINI", "MINI"),
        ("STANDARD", "STANDARD"),
        ("PREMIUM", "PREMIUM"),
        # 엣지 케이스
        (None, "STANDARD"),
        ("UNKNOWN", "STANDARD"),
        ("", "STANDARD"),
    ]
    
    print(f"\n{'입력':30} {'예상':12} {'실제':12} {'결과'}")
    print("-" * 70)
    
    all_pass = True
    for input_val, expected in test_cases:
        result = gateway._safe_route_from_str(input_val)
        actual = result.value
        status = "✅" if actual == expected else "❌"
        if actual != expected:
            all_pass = False
        
        display_input = str(input_val)[:28] if input_val else "None"
        print(f"{display_input:30} {expected:12} {actual:12} {status}")
    
    print("-" * 70)
    if all_pass:
        print("✅ 모든 backward-compat 테스트 통과!")
    else:
        print("❌ 일부 테스트 실패!")
    
    return all_pass

# ============================================================================
# 게이트웨이 벤치마크
# ============================================================================

def run_gateway_benchmark():
    """게이트웨이 + 엔진 통합 벤치마크"""
    print("\n" + "=" * 80)
    print("📊 게이트웨이 통합 벤치마크 (4,200개 샘플)")
    print("=" * 80)
    
    # 샘플 로드
    samples = []
    with open(SAMPLES_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))
    
    print(f"\n📁 로드된 샘플: {len(samples)}개")
    
    results = {}
    
    for mode in MODES:
        print(f"\n{'─' * 60}")
        print(f"🔧 모드: {mode.upper()}")
        print("─" * 60)
        
        # 엔진 + 게이트웨이 생성
        cfg = globals()["ThresholdConfig"]()
        engine = globals()["MSRVEngineV25"](cfg)
        engine.set_mode(mode)
        
        gw_cfg = globals()["GatewayConfig"](
            log_level="WARNING",
            engine_mode=mode
        )
        gateway = globals()["MSRVGateway"](engine, gw_cfg)
        
        # 통계
        route_counts = {"MINI": 0, "STANDARD": 0, "PREMIUM": 0}
        latencies = []
        sample_results = []
        
        # Fracture 안전성 체크
        fracture_count = 0
        fracture_mini = 0
        
        start_total = time.perf_counter()
        
        for i, sample in enumerate(samples):
            text = sample.get("text", "")
            lang = sample.get("lang", "EN")
            
            start = time.perf_counter()
            result = gateway.process(text=text, lang=lang, api_type="llm")
            elapsed = (time.perf_counter() - start) * 1000
            
            latencies.append(elapsed)
            route = result.route.value
            route_counts[route] += 1
            
            # 거버넌스 트레이스에서 is_fracture 확인
            gov_trace = result.governance_trace
            route_reason = gov_trace.get("output", {}).get("route_reason", {})
            is_fracture = route_reason.get("is_fracture", False)
            
            if is_fracture:
                fracture_count += 1
                if route == "MINI":
                    fracture_mini += 1
            
            sample_results.append({
                "id": sample.get("id"),
                "route": route,
                "latency_ms": round(elapsed, 4),
                "api_called": result.api_called,
                "is_fracture": is_fracture,
            })
        
        total_time = time.perf_counter() - start_total
        total = len(samples)
        
        # 비용 절감 계산
        cost_weights = {"MINI": 2, "STANDARD": 30, "PREMIUM": 100}
        baseline = total * cost_weights["PREMIUM"]
        actual = sum(route_counts[k] * cost_weights[k] for k in route_counts)
        cost_savings = (1 - actual / baseline) * 100
        
        route_pcts = {k: v/total*100 for k, v in route_counts.items()}
        avg_latency = sum(latencies) / len(latencies)
        
        results[mode] = {
            "mode": mode,
            "total_samples": total,
            "route_counts": route_counts,
            "route_pcts": route_pcts,
            "cost_savings_pct": round(cost_savings, 2),
            "avg_latency_ms": round(avg_latency, 4),
            "total_time_sec": round(total_time, 3),
            "fracture_count": fracture_count,
            "fracture_mini": fracture_mini,
            "samples": sample_results,
        }
        
        print(f"   MINI:     {route_counts['MINI']:>5} ({route_pcts['MINI']:>5.1f}%)")
        print(f"   STANDARD: {route_counts['STANDARD']:>5} ({route_pcts['STANDARD']:>5.1f}%)")
        print(f"   PREMIUM:  {route_counts['PREMIUM']:>5} ({route_pcts['PREMIUM']:>5.1f}%)")
        print(f"   비용 절감: {cost_savings:.1f}%")
        print(f"   평균 지연: {avg_latency:.3f}ms")
        print(f"\n   🔒 안전성: Fracture {fracture_count}개 → MINI {fracture_mini}개 {'✅' if fracture_mini == 0 else '⚠️'}")
    
    return results

# ============================================================================
# 리포트 생성
# ============================================================================

def generate_reports(results: Dict[str, Any], compat_pass: bool):
    """리포트 파일 생성"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # JSON 요약
    for mode, data in results.items():
        summary = {k: v for k, v in data.items() if k != "samples"}
        summary["timestamp"] = ts
        summary["gateway_version"] = "1.1.1"
        summary["engine_version"] = "2.5.5-patch-fracture"
        
        path = os.path.join(OUTPUT_DIR, f"gateway_{mode}_summary.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # JSONL 상세
    for mode, data in results.items():
        path = os.path.join(OUTPUT_DIR, f"gateway_{mode}_details.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for sample in data["samples"]:
                f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    
    # 마크다운 리포트
    md_content = f"""# MSR-V Gateway v1.1.1 + Engine v2.5.5-patch-fracture 통합 벤치마크

**생성일시**: {ts}  
**총 샘플**: 4,200개  
**게이트웨이 버전**: 1.1.1  
**엔진 버전**: 2.5.5-patch-fracture

---

## 📋 패치 내용

### Gateway v1.1.1 패치
```python
# _safe_route_from_str() backward-compat 추가

# ✅ 레거시 용어 지원
if "BYPASS" in route_upper:
    return RouteDecision.MINI
if "LITE" in route_upper:
    return RouteDecision.STANDARD
if "FULL" in route_upper:
    return RouteDecision.PREMIUM

# 신규 용어
if "MINI" in route_upper:
    return RouteDecision.MINI
# ...
```

### backward-compat 테스트
| 상태 | 결과 |
|------|------|
| 테스트 통과 | {'✅ PASS' if compat_pass else '❌ FAIL'} |

---

## 📈 모드별 결과 요약

| 모드 | MINI | STANDARD | PREMIUM | 비용 절감 | 평균 지연 | Fracture→MINI |
|------|------|----------|---------|----------|----------|---------------|
"""
    
    for mode, r in results.items():
        fracture_status = "✅ 0" if r["fracture_mini"] == 0 else f"⚠️ {r['fracture_mini']}"
        md_content += f"| **{mode.upper()}** | {r['route_counts']['MINI']} ({r['route_pcts']['MINI']:.1f}%) | {r['route_counts']['STANDARD']} ({r['route_pcts']['STANDARD']:.1f}%) | {r['route_counts']['PREMIUM']} ({r['route_pcts']['PREMIUM']:.1f}%) | {r['cost_savings_pct']:.1f}% | {r['avg_latency_ms']:.3f}ms | {fracture_status} |\n"
    
    md_content += """
---

## 🔒 안전성 검증

| 모드 | Fracture 샘플 | Fracture→MINI | 검증 |
|------|--------------|---------------|------|
"""
    
    for mode, r in results.items():
        status = "✅ PASS" if r["fracture_mini"] == 0 else "⚠️ FAIL"
        md_content += f"| {mode.upper()} | {r['fracture_count']} | {r['fracture_mini']} | {status} |\n"
    
    md_content += """
---

## 🏗️ 아키텍처

```
User Request
     ↓
┌─────────────────┐
│  MSR-V Gateway  │  ← backward-compat 레이어
│    v1.1.1       │     BYPASS/LITE/FULL → MINI/STANDARD/PREMIUM
└─────────────────┘
     ↓
┌─────────────────┐
│  MSR-V Engine   │  ← Fracture cap 패치
│  v2.5.5-patch   │     is_fracture → cap 금지
└─────────────────┘
     ↓
┌────┴────┬────────┐
↓         ↓        ↓
MINI   STANDARD  PREMIUM
(skip)  (cheap)  (premium)
```

---

## ✅ 결론

"""
    
    for mode, r in results.items():
        md_content += f"- **{mode.upper()}**: {r['cost_savings_pct']:.1f}% 비용 절감, {r['route_pcts']['MINI']:.1f}% MINI 라우팅\n"
    
    all_safe = all(r["fracture_mini"] == 0 for r in results.values())
    if all_safe and compat_pass:
        md_content += "\n### ✅ 모든 검증 통과\n- backward-compat 테스트 통과\n- Fracture→MINI 라우팅 없음\n- 거버넌스 신뢰 보장\n"
    else:
        md_content += "\n### ⚠️ 일부 검증 실패\n추가 점검 필요\n"
    
    path = os.path.join(OUTPUT_DIR, "gateway_benchmark_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    return OUTPUT_DIR

# ============================================================================
# 메인
# ============================================================================

if __name__ == "__main__":
    print("=" * 100)
    print("📊 MSR-V Gateway v1.1.1 + Engine v2.5.5-patch-fracture 통합 벤치마크")
    print("=" * 100)
    
    # 모듈 로드
    load_modules()
    
    # backward-compat 테스트
    compat_pass = test_backward_compat()
    
    # 게이트웨이 벤치마크
    results = run_gateway_benchmark()
    
    # 리포트 생성
    output_dir = generate_reports(results, compat_pass)
    
    # 최종 결과
    print("\n" + "=" * 100)
    print("📋 최종 비교표")
    print("=" * 100)
    
    print(f"""
┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  모드              │ MINI            │ STANDARD        │ PREMIUM        │ 비용 절감  │ 평균지연    │ Fracture→MINI │
├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤""")
    
    for mode, r in results.items():
        icon = {"conservative": "🔒", "balanced": "⚖️", "aggressive": "🚀"}[mode]
        f_status = "✅ 0" if r["fracture_mini"] == 0 else f"⚠️ {r['fracture_mini']}"
        print(f"│  {icon} {mode.upper():12} │ {r['route_counts']['MINI']:>5} ({r['route_pcts']['MINI']:>5.1f}%)   │ {r['route_counts']['STANDARD']:>5} ({r['route_pcts']['STANDARD']:>5.1f}%)   │ {r['route_counts']['PREMIUM']:>4} ({r['route_pcts']['PREMIUM']:>5.1f}%)  │ {r['cost_savings_pct']:>8.1f}%  │ {r['avg_latency_ms']:>9.3f}ms │ {f_status:>13} │")
    
    print("└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
    
    print(f"\n📁 생성된 파일:")
    for f in os.listdir(output_dir):
        print(f"   - {output_dir}/{f}")
