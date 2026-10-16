"""Offline waterfall engine: ordered providers per field, structured conditions, credit budget, full trace.

Providers are objects with `lookup(record, field) -> (value, confidence) | None`. The fixture provider below
runs offline; live providers (ZoomInfo, Clay, Amplemarket) are stubs in integrations/ and need credentials.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple

import yaml

from emnify_gtm.company import get
from enrichment.dedupe import norm_domain

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE / "waterfall_rules.yaml"
FIXTURE_PATH = HERE / "fixtures" / "provider_fixtures.json"


class Provider(Protocol):
    def lookup(self, record: Dict[str, Any], field_name: str) -> Optional[Tuple[Any, float]]: ...


class FixtureProvider:
    """Reads (provider, domain, field) -> [value, confidence] from a JSON fixture. Synthetic data only."""

    def __init__(self, name: str, table: Dict[str, Dict[str, Dict[str, list]]]):
        self.name = name
        self.rows = table.get(name, {})

    def lookup(self, record: Dict[str, Any], field_name: str) -> Optional[Tuple[Any, float]]:
        hit = self.rows.get(record.get("domain", ""), {}).get(field_name)
        return (hit[0], float(hit[1])) if hit else None


def load_rules(path: Path = RULES_PATH) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_fixture_providers(path: Path = FIXTURE_PATH) -> Dict[str, FixtureProvider]:
    table = json.loads(path.read_text(encoding="utf-8"))
    names = {"zoominfo", "clay_native", "first_party", "website_scrape", "amplemarket_lookup"}
    return {n: FixtureProvider(n, table) for n in names}


def check_predicate(pred: Dict[str, Any], record: Dict[str, Any]) -> bool:
    value = record.get(pred["field"])
    op = pred["op"]
    if op == "present":
        return value not in (None, "")
    if op == "absent":
        return value in (None, "")
    if value in (None, ""):
        return False
    if op == "eq":
        return value == pred["value"]
    if op == "in":
        return value in pred["value"]
    if op == "gte":
        return float(value) >= float(pred["value"])
    raise ValueError(f"unknown op {op!r}")


def classify_vertical(description: str, keywords: Dict[str, List[str]]) -> Optional[str]:
    """First vertical with the most keyword hits. Returns None when nothing matches (no guessing)."""
    text = (description or "").lower()
    scored = [(sum(k in text for k in kws), key) for key, kws in keywords.items()]
    best = max(scored, default=(0, None))
    return best[1] if best[0] > 0 else None


@dataclass
class EnrichResult:
    record: Dict[str, Any]
    trace: List[Dict[str, Any]] = field(default_factory=list)
    credits_spent: int = 0
    provenance: Dict[str, str] = field(default_factory=dict)


def enrich(record: Dict[str, Any], providers: Dict[str, Provider], rules: Optional[dict] = None,
           budget: Optional[int] = None) -> EnrichResult:
    rules = rules or load_rules()
    budget = budget if budget is not None else int(get("guardrails.max_enrichment_credits_per_run", 500))
    min_conf = float(rules["defaults"]["min_confidence"])
    out = EnrichResult(record=dict(record))
    if out.record.get("domain"):
        out.record["domain"] = norm_domain(out.record["domain"])
    for field_name, steps in rules["fields"].items():
        if out.record.get(field_name) not in (None, ""):
            out.trace.append({"field": field_name, "step": "skip", "reason": "already populated"})
            continue
        for step in steps:
            name = step["provider"]
            if not all(check_predicate(p, out.record) for p in step.get("when", [])):
                out.trace.append({"field": field_name, "provider": name, "step": "skip", "reason": "condition not met"})
                continue
            if out.credits_spent + step["cost"] > budget:
                out.trace.append({"field": field_name, "provider": name, "step": "skip", "reason": "credit budget"})
                continue
            out.credits_spent += step["cost"]
            hit = providers[name].lookup(out.record, field_name) if name in providers else None
            if hit and hit[1] >= min_conf:
                out.record[field_name] = hit[0]
                out.provenance[field_name] = name
                out.trace.append({"field": field_name, "provider": name, "step": "accepted", "confidence": hit[1]})
                break
            out.trace.append({"field": field_name, "provider": name, "step": "miss",
                              "confidence": hit[1] if hit else None})
        if field_name == "company_description" and out.record.get("company_description"):
            vertical = classify_vertical(out.record["company_description"], rules["vertical_keywords"])
            if vertical:
                out.record["iot_vertical"] = vertical
                out.provenance["iot_vertical"] = "classify_vertical (hypothesis: validate keywords)"
    return out
