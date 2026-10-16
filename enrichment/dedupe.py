"""Account dedupe: normalized-domain clusters first, then conservative name+country matching.

Output is a merge PLAN (survivor + losers + reason). It never writes to a CRM. A human approves merges.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any, Dict, List

LEGAL_SUFFIXES = re.compile(r"\b(gmbh|ag|inc|llc|ltd|limited|bv|b\.v\.|sa|sas|plc|corp|corporation|co|kg|ug)\b\.?", re.I)
GENERIC_DOMAINS = {"gmail.com", "outlook.com", "yahoo.com", "hotmail.com", "linkedin.com", "facebook.com"}
NAME_THRESHOLD = 0.92   # hypothesis: validate on real duplicate pairs before lowering


def norm_domain(value: str) -> str:
    v = (value or "").strip().lower()
    v = re.sub(r"^https?://", "", v)
    v = re.sub(r"^www\.", "", v)
    return v.split("/")[0].split("?")[0]


def norm_name(value: str) -> str:
    v = LEGAL_SUFFIXES.sub(" ", (value or "").lower())
    return re.sub(r"[^a-z0-9 ]", "", v).strip()


def completeness(rec: Dict[str, Any]) -> int:
    return sum(1 for v in rec.values() if v not in (None, ""))


def survivor(cluster: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Most complete record wins; ties go to the oldest created_date, then the lowest id."""
    return sorted(cluster, key=lambda r: (-completeness(r), r.get("created_date", "9999"), str(r.get("id", ""))))[0]


def find_clusters(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    parent = list(range(len(records)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    reasons: Dict[frozenset, str] = {}

    def union(a: int, b: int, why: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            reasons[frozenset((a, b))] = why

    by_domain: Dict[str, int] = {}
    for i, r in enumerate(records):
        d = norm_domain(r.get("domain", ""))
        if d and d not in GENERIC_DOMAINS:
            if d in by_domain:
                union(by_domain[d], i, "same domain")
            else:
                by_domain[d] = i
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            a, b = records[i], records[j]
            if find(i) == find(j) or not a.get("country") or a.get("country") != b.get("country"):
                continue
            na, nb = norm_name(a.get("name", "")), norm_name(b.get("name", ""))
            if na and nb and SequenceMatcher(None, na, nb).ratio() >= NAME_THRESHOLD:
                union(i, j, "same country and near-identical name")

    groups: Dict[int, List[int]] = {}
    for i in range(len(records)):
        groups.setdefault(find(i), []).append(i)
    plans = []
    for idxs in groups.values():
        if len(idxs) < 2:
            continue
        cluster = [records[i] for i in idxs]
        keep = survivor(cluster)
        why = sorted({reasons[k] for k in reasons if k <= set(idxs)})
        plans.append({"survivor_id": keep.get("id"), "merge_ids": [r.get("id") for r in cluster if r is not keep],
                      "reasons": why, "action": "propose_merge_for_human_approval"})
    return plans
