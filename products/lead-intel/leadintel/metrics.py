"""Baseline metrics over the LABELED synthetic dataset.

Answers "how do we know whether the system is accurate?" — on synthetic data.
Metrics: qualification precision, false-positive rate, false-negative rate,
category accuracy, data completeness, provenance completeness.

IMPORTANT: these are computed on SYNTHETIC data and are NOT real-world evidence.
They establish a governance baseline and a regression guard; real numbers will
differ once a live provider is approved (MISSION-003).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .enrich import enrich
from .models import Query, Status
from .normalize import normalize
from .providers.base import RawBusiness
from .scoring.config import ScoringConfig, load_config
from .scoring.engine import qualify

_DEFAULT_DATASET = (
    Path(__file__).resolve().parents[1] / "data" / "fixtures" / "synthetic_leads.json"
)
# Location-neutral query: every record shares region CO, so location contributes
# uniformly and does not confound category qualification metrics.
_METRICS_QUERY = Query(market="electrical contractors", location="CO")


def _raw_from_record(r: dict) -> RawBusiness:
    return RawBusiness(
        name=r.get("name", ""), website=r.get("website"),
        city=r.get("city"), region=r.get("region"), country=r.get("country"),
        categories=list(r.get("categories", [])),
        phone=r.get("phone"), email=r.get("email"), contact_form_url=r.get("contact_form_url"),
        socials=list(r.get("socials", [])),
        employees=r.get("employees"), review_count=r.get("review_count"),
        years_in_business=r.get("years_in_business"), rating=r.get("rating"),
        decision_makers=list(r.get("decision_makers", [])),
        source_url=r.get("source_url"), notes=r.get("notes", ""),
    )


def compute_metrics(
    dataset_path: Optional[Path | str] = None,
    config: Optional[ScoringConfig] = None,
) -> dict:
    dataset_path = Path(dataset_path) if dataset_path else _DEFAULT_DATASET
    config = config or load_config()
    payload = json.loads(Path(dataset_path).read_text(encoding="utf-8"))
    records = payload.get("businesses", [])

    tp = fp = fn = tn = 0
    category_correct = 0
    expected_behavior_correct = 0
    completeness_sum = 0.0
    provenance_complete = 0
    mismatches: list[dict] = []

    for r in records:
        gt = r.get("ground_truth", {})
        is_target = bool(gt.get("is_target"))
        expected_category = gt.get("expected_category")
        expected_qualified = bool(gt.get("expected_qualified"))

        nb = normalize(_raw_from_record(r), "fixture", is_synthetic=True)
        lead = enrich(nb)
        qualify(lead, _METRICS_QUERY, config)

        predicted_qualified = lead.status == Status.QUALIFIED

        if predicted_qualified and is_target:
            tp += 1
        elif predicted_qualified and not is_target:
            fp += 1
        elif not predicted_qualified and is_target:
            fn += 1
        else:
            tn += 1

        if lead.category_verdict.value == expected_category:
            category_correct += 1
        else:
            mismatches.append({"company": lead.company, "kind": "category",
                               "expected": expected_category, "got": lead.category_verdict.value})
        if predicted_qualified == expected_qualified:
            expected_behavior_correct += 1
        else:
            mismatches.append({"company": lead.company, "kind": "qualification",
                               "expected_qualified": expected_qualified,
                               "got_status": lead.status.value})

        completeness_sum += lead.data_completeness
        if lead.provenance_complete:
            provenance_complete += 1

    n = len(records)
    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    fp_rate = _safe_div(fp, fp + tn)
    fn_rate = _safe_div(fn, fn + tp)

    return {
        "_disclaimer": "SYNTHETIC baseline — NOT real-world evidence (MISSION-003).",
        "dataset": str(dataset_path.name),
        "scoring_config_version": config.version,
        "records": n,
        "confusion_matrix": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "qualification_precision": precision,
        "recall": recall,
        "false_positive_rate": fp_rate,
        "false_negative_rate": fn_rate,
        "category_accuracy": _safe_div(category_correct, n),
        "expected_behavior_accuracy": _safe_div(expected_behavior_correct, n),
        "average_data_completeness": round(completeness_sum / n, 3) if n else 0.0,
        "provenance_completeness_rate": _safe_div(provenance_complete, n),
        "mismatches": mismatches,
    }


def _safe_div(a: int, b: int) -> float:
    return round(a / b, 3) if b else 0.0
