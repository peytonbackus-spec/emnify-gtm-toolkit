"""Apply the field-mapping contract: build an upsert payload and say exactly why each field was or wasn't written."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

from emnify_gtm.company import vertical_keys

PATH = Path(__file__).resolve().parent / "field_mapping.yaml"
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def load_mapping(path: Path = PATH) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def coerce(value: Any, type_: str) -> Any:
    if type_ == "integer":
        return int(value)
    if type_ == "iso2":
        v = str(value).strip().upper()
        if len(v) != 2 or not v.isalpha():
            raise ValueError(f"not an ISO-2 country code: {value!r}")
        return v
    if type_ == "enum":
        if value not in vertical_keys():
            raise ValueError(f"{value!r} is not a known vertical key")
        return value
    if type_ == "email":
        if not EMAIL.match(str(value)):
            raise ValueError(f"not an email: {value!r}")
        return str(value).lower()
    return str(value).strip()


def build_payload(enriched: Dict[str, Any], crm_current: Optional[Dict[str, Any]] = None,
                  mapping: Optional[dict] = None) -> Dict[str, Any]:
    mapping = mapping or load_mapping()
    crm_current = crm_current or {}
    for req in mapping["required_for_upsert"]:
        if not enriched.get(req):
            return {"upsert": False, "reason": f"missing required {req}", "fields": {}, "decisions": []}
    fields: Dict[str, Any] = {}
    decisions = []
    for f in mapping["fields"]:
        src, sf = f["source"], f["sfdc"]
        if enriched.get(src) in (None, ""):
            decisions.append({"source": src, "decision": "skip", "why": "no value"})
            continue
        if sf is None or f["write_policy"] == "never":
            decisions.append({"source": src, "decision": "skip", "why": "write_policy never"})
            continue
        try:
            value = coerce(enriched[src], f["type"])
        except ValueError as exc:
            decisions.append({"source": src, "decision": "reject", "why": str(exc)})
            continue
        if f["write_policy"] == "fill_if_empty" and crm_current.get(sf) not in (None, ""):
            decisions.append({"source": src, "decision": "skip", "why": "CRM already has a value"})
            continue
        fields[sf] = value
        decisions.append({"source": src, "decision": "write", "sfdc": sf})
    ext = mapping["external_id"]
    return {"upsert": True, "object": mapping["object"], "external_id": {ext["sfdc"]: enriched[ext["source"]]},
            "fields": fields, "decisions": decisions}
