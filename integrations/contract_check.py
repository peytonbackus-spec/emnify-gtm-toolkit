"""Validate a payload against an integrations/contracts/*.yaml file. Offline, no dependencies beyond PyYAML."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List

import yaml

from emnify_gtm.company import get

CONTRACTS = Path(__file__).resolve().parent / "contracts"
TYPES = {"string": str, "integer": int, "object": dict, "array": list}


def load_contract(name: str) -> dict:
    return yaml.safe_load((CONTRACTS / f"{name}.yaml").read_text(encoding="utf-8"))


def check(payload: Dict[str, Any], contract: dict) -> List[str]:
    errors = []
    for fname, spec in contract["fields"].items():
        if fname not in payload or payload[fname] in (None, ""):
            if spec.get("required"):
                errors.append(f"{fname}: required")
            continue
        v = payload[fname]
        t = TYPES[spec["type"]]
        if not isinstance(v, t) or (t is int and isinstance(v, bool)):
            errors.append(f"{fname}: expected {spec['type']}")
            continue
        if "pattern" in spec and not re.match(spec["pattern"], v):
            errors.append(f"{fname}: does not match pattern")
        if "min" in spec and v < spec["min"]:
            errors.append(f"{fname}: below {spec['min']}")
        if "enum" in spec and v not in spec["enum"]:
            errors.append(f"{fname}: not in enum")
        if spec.get("enum_from") == "icp_hypotheses.verticals":
            if v not in [x["key"] for x in get("icp_hypotheses.verticals")]:
                errors.append(f"{fname}: unknown vertical")
    return errors
