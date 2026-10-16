"""Knowledge tools: validate documents, build INDEX.yaml, look things up for agents. Read-only except `build`.

    python -m knowledge.tools validate
    python -m knowledge.tools build
    python -m knowledge.tools lookup "enrich accounts"
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from typing import Dict, List, Optional

import yaml

from emnify_gtm.company import ROOT, get

KNOW = ROOT / "knowledge"
REQUIRED = ("id", "type", "tags", "last_modified", "confidence_score", "status")
SKIP = {"INDEX.yaml"}


def documents() -> List[dict]:
    docs = []
    for p in sorted(KNOW.rglob("*.yaml")):
        if p.name in SKIP or "proposals" in p.parts:
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        d["_path"] = str(p.relative_to(ROOT))
        docs.append(d)
    return docs


def validate(as_of: Optional[date] = None) -> List[str]:
    as_of = as_of or date.today()
    stale_after = int(get("knowledge.stale_after_days", 120))
    problems, seen = [], set()
    for d in documents():
        where = d["_path"]
        for k in REQUIRED:
            if k not in d:
                problems.append(f"{where}: missing {k}")
        if d.get("id") in seen:
            problems.append(f"{where}: duplicate id {d.get('id')}")
        seen.add(d.get("id"))
        cs = d.get("confidence_score")
        if cs is not None and not (isinstance(cs, (int, float)) and 0 <= cs <= 1):
            problems.append(f"{where}: confidence_score must be 0-1")
        lm = d.get("last_modified")
        if isinstance(lm, date) and (as_of - lm).days > stale_after:
            problems.append(f"{where}: stale ({(as_of - lm).days} days)")
        if d.get("type") == "workflow-contract" and "hitl" not in d:
            problems.append(f"{where}: workflow contract without hitl block")
    ids = {d.get("id") for d in documents()}
    router = next((d for d in documents() if d.get("type") == "router"), None)
    for r in (router or {}).get("routes", []):
        if r["contract"] not in ids:
            problems.append(f"router: unknown contract {r['contract']}")
    return problems


def build_index() -> dict:
    entries = [{"id": d["id"], "type": d["type"], "path": d["_path"], "tags": d.get("tags", []),
                "status": d.get("status"), "confidence_score": d.get("confidence_score"),
                "last_modified": d.get("last_modified")} for d in documents()]
    index = {"generated_by": "python -m knowledge.tools build", "documents": entries}
    (KNOW / "INDEX.yaml").write_text(yaml.safe_dump(index, sort_keys=False), encoding="utf-8")
    return index


def lookup(query: str) -> List[Dict[str, str]]:
    """Router-first: score each route by keyword overlap, return citations (id + path). No match returns []."""
    words = {w.strip(",.").lower() for w in query.split() if len(w) > 2}
    by_id = {d["id"]: d for d in documents()}
    router = next(d for d in documents() if d.get("type") == "router")
    hits = []
    for r in router["routes"]:
        terms = {t.strip().lower() for t in r["matches"].split(",")}
        score = sum(1 for t in terms if t in query.lower() or any(w in t.split() for w in words))
        if score:
            doc = by_id[r["contract"]]
            hits.append((score, {"id": doc["id"], "path": doc["_path"], "status": str(doc.get("status")),
                                 "confidence_score": str(doc.get("confidence_score"))}))
    return [h for _, h in sorted(hits, key=lambda x: -x[0])]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["validate", "build", "lookup"])
    ap.add_argument("query", nargs="?", default="")
    a = ap.parse_args()
    if a.cmd == "validate":
        probs = validate()
        print("\n".join(probs) or "ok")
        return 1 if probs else 0
    if a.cmd == "build":
        print(f"indexed {len(build_index()['documents'])} documents")
        return 0
    print(yaml.safe_dump(lookup(a.query), sort_keys=False) or "no route: log a gap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
