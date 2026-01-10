#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSR-V v2.5.5 Unified 벤치마크 시스템
- 용어 변경: BYPASS→MINI, LITE→STANDARD, FULL→PREMIUM
- 3가지 모드: CONSERVATIVE, BALANCED, AGGRESSIVE
- 4,200 샘플 벤치마크
"""

import sys
import os
import json
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
from enum import Enum

# 패치된 엔진 로드
sys.path.insert(0, './msrv-public-demo')

# ============================================================================
# 새 용어 매핑
# ============================================================================

class RouteTier(Enum):
    """새 용어 체계"""
    MINI = "MINI"           # 기존 BYPASS
    STANDARD = "STANDARD"   # 기존 LITE
    PREMIUM = "PREMIUM"     # 기존 FULL

# 기존 → 신규 매핑 (하위호환성 유지 + 새 용어 직접 인식)
ROUTE_MAP = {
    # 기존 용어
    "BYPASS": "MINI",
    "LITE": "STANDARD", 
    "FULL": "PREMIUM",
    "Bypass (no MSR)": "MINI",
    "Lite (v1.5 minimal)": "STANDARD",
    "Full (v2.5+)": "PREMIUM",
    # 새 용어 (직접 반환)
    "MINI": "MINI",
    "STANDARD": "STANDARD",
    "PREMIUM": "PREMIUM",
}

def map_route(old_route: str) -> str:
    """기존 라우트를 새 용어로 변환 (또는 새 용어 그대로 반환)"""
    # 정확한 매칭 먼저
    if old_route in ROUTE_MAP:
        return ROUTE_MAP[old_route]
    # 부분 매칭
    for old, new in ROUTE_MAP.items():
        if old.upper() in old_route.upper():
            return new
    return "PREMIUM"  # 기본값

# ============================================================================
# 비용 가중치 (PREMIUM = 100 기준)
# ============================================================================

COST_WEIGHTS = {
    "MINI": 2,      # 초저가 (로컬/국내)
    "STANDARD": 30, # 저가 글로벌
    "PREMIUM": 100, # 고급 글로벌
}

def calculate_cost_savings(stats: Dict[str, int], total: int) -> float:
    """비용 절감률 계산"""
    if total == 0:
        return 0.0
    
    # 모두 PREMIUM일 때 비용
    baseline = total * COST_WEIGHTS["PREMIUM"]
    
    # 실제 비용
    actual = (
        stats.get("MINI", 0) * COST_WEIGHTS["MINI"] +
        stats.get("STANDARD", 0) * COST_WEIGHTS["STANDARD"] +
        stats.get("PREMIUM", 0) * COST_WEIGHTS["PREMIUM"]
    )
    
    return (1 - actual / baseline) * 100

# ============================================================================
# 데이터셋 로더
# ============================================================================

def load_jsonl_samples(path: str) -> List[Dict]:
    """JSONL 파일 로드"""
    samples = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    samples.append(json.loads(line))
    except Exception as e:
        print(f"Error loading {path}: {e}")
    return samples

# ============================================================================
# 벤치마크 결과 데이터 구조
# ============================================================================

@dataclass
class SampleResult:
    """개별 샘플 결과"""
    id: str
    text: str
    lang: str
    dataset: str
    route: str
    latency_ms: float
    white_trace: Dict[str, Any]

@dataclass
class ModeResult:
    """모드별 결과"""
    mode: str
    total_samples: int
    route_counts: Dict[str, int]
    route_pcts: Dict[str, float]
    cost_savings_pct: float
    avg_latency_ms: float
    total_time_sec: float
    samples: List[SampleResult]

# ============================================================================
# 메인 벤치마크 함수
# ============================================================================

def run_benchmark(engine_path: str, datasets: List[tuple], modes: List[str]) -> Dict[str, ModeResult]:
    """전체 벤치마크 실행"""
    
    # 엔진 코드 로드
    with open(engine_path, "r") as f:
        code = f.read().split("if __name__ ==")[0]
        exec(code, globals())
    
    # 샘플 로드
    all_samples = []
    for ds_name, path, lang in datasets:
        for sample in load_jsonl_samples(path):
            sample["lang"] = lang
            sample["dataset"] = ds_name
            all_samples.append(sample)
    
    print(f"\n📁 로드된 샘플: {len(all_samples)}개")
    
    results = {}
    
    for mode in modes:
        print(f"\n{'='*80}")
        print(f"🔧 모드: {mode.upper()}")
        print("="*80)
        
        # 엔진 생성 + 모드 설정
        cfg = globals()["ThresholdConfig"]()
        engine = globals()["MSRVEngineV25"](cfg)
        engine.set_mode(mode)
        
        # 설정 출력
        print(f"   T_BYPASS_BASE: {engine.cfg.T_BYPASS_BASE}")
        print(f"   KO_BYPASS_BASE: {engine.cfg.KO_BYPASS_BASE}")
        print(f"   EN_BYPASS_BASE: {engine.cfg.EN_BYPASS_BASE}")
        print(f"   DISABLE_SHORT_SIG_CAP: {engine.cfg.DISABLE_SHORT_SIG_CAP}")
        
        stats = {"MINI": 0, "STANDARD": 0, "PREMIUM": 0}
        latencies = []
        sample_results = []
        
        start_total = time.perf_counter()
        
        for i, sample in enumerate(all_samples):
            text = sample.get("text", "")
            lang = sample.get("lang", "EN")
            ds_name = sample.get("dataset", "unknown")
            
            start = time.perf_counter()
            result = engine.inspect(text, lang=lang)
            elapsed = (time.perf_counter() - start) * 1000
            latencies.append(elapsed)
            
            # 라우트 변환
            old_route = result["output"]["route"]
            new_route = map_route(old_route)
            stats[new_route] += 1
            
            # 화이트 트레이스 추출
            output = result.get("output", {})
            white_trace = {
                "Zs": output.get("Zs"),
                "state4": output.get("state4"),
                "shape": output.get("shape"),
                "theta": output.get("theta"),
                "route_reason": output.get("route_reason", {}),
            }
            
            # high_stakes, residual_ratio 추출
            route_reason = output.get("route_reason", {})
            if isinstance(route_reason, str):
                try:
                    route_reason = json.loads(route_reason)
                except:
                    route_reason = {}
            
            white_trace["high_stakes"] = route_reason.get("high_stakes", False)
            white_trace["residual_ratio"] = route_reason.get("residual_ratio")
            white_trace["need"] = route_reason.get("need")
            white_trace["short_sig"] = route_reason.get("short_sig")
            
            sample_results.append(SampleResult(
                id=f"{ds_name}_{i:04d}",
                text=text[:100] + "..." if len(text) > 100 else text,
                lang=lang,
                dataset=ds_name,
                route=new_route,
                latency_ms=elapsed,
                white_trace=white_trace
            ))
        
        total_time = (time.perf_counter() - start_total)
        t = len(all_samples)
        avg_latency = sum(latencies) / len(latencies)
        cost_savings = calculate_cost_savings(stats, t)
        
        route_pcts = {k: v/t*100 for k, v in stats.items()}
        
        results[mode] = ModeResult(
            mode=mode,
            total_samples=t,
            route_counts=stats,
            route_pcts=route_pcts,
            cost_savings_pct=cost_savings,
            avg_latency_ms=avg_latency,
            total_time_sec=total_time,
            samples=sample_results
        )
        
        print(f"\n📊 결과:")
        print(f"   MINI:     {stats['MINI']:>5} ({route_pcts['MINI']:>5.1f}%)")
        print(f"   STANDARD: {stats['STANDARD']:>5} ({route_pcts['STANDARD']:>5.1f}%)")
        print(f"   PREMIUM:  {stats['PREMIUM']:>5} ({route_pcts['PREMIUM']:>5.1f}%)")
        print(f"   비용 절감: {cost_savings:.1f}%")
        print(f"   평균 지연: {avg_latency:.2f}ms")
        print(f"   총 시간: {total_time:.1f}s")
    
    return results

# ============================================================================
# 리포트 생성
# ============================================================================

def generate_json_report(result: ModeResult, output_dir: str):
    """JSON 리포트 생성"""
    data = {
        "mode": result.mode,
        "timestamp": datetime.now().isoformat(),
        "total_samples": result.total_samples,
        "route_counts": result.route_counts,
        "route_pcts": result.route_pcts,
        "cost_savings_pct": result.cost_savings_pct,
        "avg_latency_ms": result.avg_latency_ms,
        "total_time_sec": result.total_time_sec,
    }
    
    path = os.path.join(output_dir, f"benchmark_{result.mode}_summary.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path

def generate_jsonl_report(result: ModeResult, output_dir: str):
    """JSONL 상세 리포트 생성"""
    path = os.path.join(output_dir, f"benchmark_{result.mode}_details.jsonl")
    with open(path, 'w', encoding='utf-8') as f:
        for sample in result.samples:
            line = {
                "id": sample.id,
                "text": sample.text,
                "lang": sample.lang,
                "dataset": sample.dataset,
                "route": sample.route,
                "latency_ms": sample.latency_ms,
                "white_trace": sample.white_trace,
            }
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
    return path

def generate_md_report(results: Dict[str, ModeResult], output_dir: str):
    """마크다운 리포트 생성"""
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""# MSR-V v2.5.5 Unified 벤치마크 리포트

**생성일시**: {ts}  
**총 샘플**: 4,200개  
**엔진 버전**: 2.5.5-unified-patched

---

## 📋 용어 변경

| 기존 | 신규 | 의미 |
|------|------|------|
| BYPASS | **MINI** | 초저가/내부/국내 모델 |
| LITE | **STANDARD** | 저가 글로벌 모델 |
| FULL | **PREMIUM** | 고급 글로벌 모델 |

---

## 📊 비용 가중치

| 티어 | 비용 가중치 |
|------|------------|
| MINI | 2 |
| STANDARD | 30 |
| PREMIUM | 100 |

---

## 📈 모드별 결과 요약

| 모드 | MINI | STANDARD | PREMIUM | 비용 절감 | 평균 지연 | 총 시간 |
|------|------|----------|---------|----------|----------|---------|
"""
    
    for mode, r in results.items():
        content += f"| **{mode.upper()}** | {r.route_counts['MINI']} ({r.route_pcts['MINI']:.1f}%) | {r.route_counts['STANDARD']} ({r.route_pcts['STANDARD']:.1f}%) | {r.route_counts['PREMIUM']} ({r.route_pcts['PREMIUM']:.1f}%) | {r.cost_savings_pct:.1f}% | {r.avg_latency_ms:.2f}ms | {r.total_time_sec:.1f}s |\n"
    
    content += """
---

## 🎛️ 모드 설명

### 🔒 CONSERVATIVE (파일럿/신뢰구축)
- MINI 라우팅 비활성화
- 모든 문장 최소 STANDARD 이상 검증
- 안전 우선, 비용 절감 최소화

### ⚖️ BALANCED (권장 운영)
- 비용과 안전의 균형
- 적절한 MINI 라우팅 허용
- 일반 운영 환경 권장

### 🚀 AGGRESSIVE (비용 최적화)
- MINI 라우팅 극대화
- 최대 비용 절감
- 신뢰된 MINI 제공자 필요

---

## 📁 데이터셋 구성

| 언어 | 유형 | 샘플 수 |
|------|------|---------|
| KO | 일반 (norm) | 1,000 |
| KO | 부정 (neg) | 1,000 |
| KO | 고난도 (hard) | 100 |
| EN | 일반 (norm) | 1,000 |
| EN | 부정 (neg) | 1,000 |
| EN | 고난도 (hard) | 100 |
| **총합** | | **4,200** |

---

## 🔧 사용법

```python
from msrv_v255_unified_final import MSRVEngineV25, ThresholdConfig

engine = MSRVEngineV25(ThresholdConfig())

# 모드 전환
engine.set_mode("conservative")   # 파일럿
engine.set_mode("balanced")       # 권장
engine.set_mode("aggressive")     # 최대 절감

# 분석
result = engine.inspect("문장", lang="KO")
print(result["output"]["route"])  # MINI/STANDARD/PREMIUM
```

---

## 📊 화이트 로직 트레이스 예시

각 샘플에서 추출되는 화이트 트레이스:

```json
{
  "Zs": 0.63,
  "state4": "Alignment",
  "shape": "△",
  "theta": 0.357,
  "high_stakes": false,
  "residual_ratio": 0.24,
  "need": 0.55,
  "short_sig": false
}
```

---

## ✅ 결론

"""
    
    for mode, r in results.items():
        content += f"- **{mode.upper()}**: {r.cost_savings_pct:.1f}% 비용 절감, {r.route_pcts['MINI']:.1f}% MINI 라우팅\n"
    
    path = os.path.join(output_dir, "benchmark_report.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path

# ============================================================================
# 메인 실행
# ============================================================================

if __name__ == "__main__":
    
    # 설정
    ENGINE_PATH = "/home/claude/msrv_v255_unified_final.py"
    OUTPUT_DIR = "/home/claude/benchmark_results"
    
    DATASETS = [
        ("ko-norm", "/mnt/user-data/uploads/results_ko-norm_20251231_175834.jsonl", "KO"),
        ("ko-neg", "/mnt/user-data/uploads/results_ko-neg_20251231_175834.jsonl", "KO"),
        ("ko-hard", "/mnt/user-data/uploads/results_ko-hard_20251231_175834.jsonl", "KO"),
        ("en-norm", "/mnt/user-data/uploads/results_en-norm_20251231_175834.jsonl", "EN"),
        ("en-neg", "/mnt/user-data/uploads/results_en-neg_20251231_175834.jsonl", "EN"),
        ("en-hard", "/mnt/user-data/uploads/results_en-hard_20251231_175834.jsonl", "EN"),
    ]
    
    MODES = ["conservative", "balanced", "aggressive"]
    
    # 출력 디렉토리 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 100)
    print("📊 MSR-V v2.5.5 Unified 벤치마크 시스템")
    print("   용어 체계: MINI / STANDARD / PREMIUM")
    print("=" * 100)
    
    # 벤치마크 실행
    results = run_benchmark(ENGINE_PATH, DATASETS, MODES)
    
    # 리포트 생성
    print("\n" + "=" * 100)
    print("📁 리포트 생성")
    print("=" * 100)
    
    generated_files = []
    
    for mode, result in results.items():
        json_path = generate_json_report(result, OUTPUT_DIR)
        jsonl_path = generate_jsonl_report(result, OUTPUT_DIR)
        generated_files.extend([json_path, jsonl_path])
        print(f"  ✅ {mode}: JSON + JSONL 생성")
    
    md_path = generate_md_report(results, OUTPUT_DIR)
    generated_files.append(md_path)
    print(f"  ✅ 마크다운 리포트 생성")
    
    # 최종 결과 출력
    print("\n" + "=" * 100)
    print("📋 최종 비교표")
    print("=" * 100)
    
    print(f"""
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  모드              │ MINI            │ STANDARD       │ PREMIUM       │ 비용 절감 │ 평균지연 │ 총시간     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────┤""")
    
    for mode, r in results.items():
        icon = {"conservative": "🔒", "balanced": "⚖️", "aggressive": "🚀"}[mode]
        print(f"│  {icon} {mode.upper():12} │ {r.route_counts['MINI']:>5} ({r.route_pcts['MINI']:>5.1f}%)   │ {r.route_counts['STANDARD']:>5} ({r.route_pcts['STANDARD']:>5.1f}%)  │ {r.route_counts['PREMIUM']:>4} ({r.route_pcts['PREMIUM']:>4.1f}%)  │ {r.cost_savings_pct:>7.1f}%  │ {r.avg_latency_ms:>6.2f}ms │ {r.total_time_sec:>5.1f}s     │")
    
    print("└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘")
    
    print(f"\n📁 생성된 파일:")
    for f in generated_files:
        print(f"   - {f}")
