#!/usr/bin/env python3
"""Compute and print baseline metrics over the labeled synthetic dataset.

Usage:
  python3 evaluate.py                 # print metrics
  python3 evaluate.py --json          # machine-readable
  python3 evaluate.py --out PATH.json # also write to a file
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from leadintel.metrics import compute_metrics


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Baseline metrics (SYNTHETIC data)")
    p.add_argument("--dataset", default=None, help="path to a labeled dataset JSON")
    p.add_argument("--config", default=None, help="path to a scoring config JSON")
    p.add_argument("--json", action="store_true", help="print JSON")
    p.add_argument("--out", default=None, help="write metrics JSON to this path")
    args = p.parse_args(argv)

    from leadintel.scoring.config import load_config
    config = load_config(args.config) if args.config else None
    metrics = compute_metrics(args.dataset, config)

    if args.out:
        Path(args.out).write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(metrics, ensure_ascii=False, indent=2))
        return 0

    cm = metrics["confusion_matrix"]
    print("Baseline metrics — SYNTHETIC data (NOT real-world evidence)")
    print(f"  dataset: {metrics['dataset']}  records: {metrics['records']}  "
          f"config: v{metrics['scoring_config_version']}")
    print(f"  confusion: TP={cm['tp']} FP={cm['fp']} FN={cm['fn']} TN={cm['tn']}")
    print(f"  qualification precision : {metrics['qualification_precision']}")
    print(f"  recall                  : {metrics['recall']}")
    print(f"  false-positive rate     : {metrics['false_positive_rate']}")
    print(f"  false-negative rate     : {metrics['false_negative_rate']}")
    print(f"  category accuracy       : {metrics['category_accuracy']}")
    print(f"  expected-behavior acc.  : {metrics['expected_behavior_accuracy']}")
    print(f"  avg data completeness   : {metrics['average_data_completeness']}")
    print(f"  provenance completeness : {metrics['provenance_completeness_rate']}")
    if metrics["mismatches"]:
        print(f"  mismatches ({len(metrics['mismatches'])}):")
        for m in metrics["mismatches"]:
            print(f"    - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
