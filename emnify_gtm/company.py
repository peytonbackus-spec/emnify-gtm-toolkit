"""Load company.yaml, the single variables file every emnify module draws from."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
COMPANY_PATH = ROOT / "company.yaml"


@lru_cache(maxsize=1)
def load_company(path: str | None = None) -> dict:
    with open(path or COMPANY_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def get(dotted: str, default: Any = None) -> Any:
    """company.get('stack.crm.tool') -> 'Salesforce'. Lists are not indexable; use the list itself."""
    node: Any = load_company()
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def tools() -> dict[str, str]:
    return {k: v["tool"] for k, v in load_company()["stack"].items()}


def vertical_keys() -> list[str]:
    return [v["key"] for v in load_company()["icp_hypotheses"]["verticals"]]
