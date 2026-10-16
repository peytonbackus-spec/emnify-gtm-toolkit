"""The three agent workflows. Mock mode (default) is deterministic and offline; GTM_LLM_MODE=anthropic runs the same
prompts live (needs ANTHROPIC_API_KEY, not used in this build)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

import agents  # noqa: F401  (extends the PII allow-list)
from emnify_gtm.company import get
from shared_core.ai_governance.hitl import HITLPolicy
from shared_core.ai_governance.llm_client import LLMClient, load_prompt

PROMPTS = Path(__file__).resolve().parent / "prompts"
HITL = HITLPolicy(always_review_actions=("send_message", "crm_write", "disqualify_account"))
INJECTION = re.compile(r"ignore (all |any )?(previous|prior) instructions|mark (this )?(deal )?(as )?closed|change (the )?stage|"
                       r"email (the )?ceo|system prompt", re.I)


def _system(name: str) -> tuple[str, str]:
    pid, text = load_prompt(PROMPTS / f"{name}.md")
    return pid, text.replace("{{COMPANY_NAME}}", get("company.name"))


def research_brief(record: Dict, client: LLMClient | None = None) -> Dict:
    pid, system = _system("research_brief")
    client = client or LLMClient()

    def mock(r: Dict) -> Dict:
        evidence = [{"claim": f"{k.replace('_', ' ')}: {r[k]}", "source_field": k}
                    for k in ("company", "iot_vertical", "employees", "region") if r.get(k) not in (None, "")]
        unknowns = [k for k in ("expected_device_count", "countries") if r.get(k) in (None, "")]
        vertical = r.get("iot_vertical") or "unknown"
        in_icp = vertical in [v["key"] for v in get("icp_hypotheses.verticals")]
        return {"summary": f"{r.get('company', 'Account')} ({vertical}); {len(unknowns)} qualification field(s) unknown.",
                "vertical": vertical, "evidence": evidence, "unknowns": unknowns,
                "qualification": {"fit_assessment": "possible fit (hypothesis: validate)" if in_icp else "no vertical match",
                                  "disqualify_flag": not in_icp},
                "next_action": "Confirm device count and countries on the first call" if in_icp else "Human review before dropping",
                "confidence": round(1 - len(unknowns) / 4 - (0 if in_icp else 0.25), 2)}

    return client.complete_json(prompt_id=pid, system=system, record=record, mock_responder=mock,
                                required_keys=["summary", "vertical", "evidence", "unknowns", "qualification", "next_action", "confidence"])


def qualification_signal(record: Dict, client: LLMClient | None = None) -> Dict:
    pid, system = _system("qualification_signal")
    client = client or LLMClient()

    def mock(r: Dict) -> Dict:
        text = r.get("notes", "") or ""
        proposals = []
        m = re.search(r"([\d,]{2,})\s+devices", text)
        if m:
            proposals.append({"field": "expected_device_count", "value": int(m.group(1).replace(",", "")), "quote": m.group(0)})
        m = re.search(r"deploy(?:ing|ed)? (?:in|across) ([A-Za-z, ]+?)(?:\.|;| with|$)", text)
        if m:
            proposals.append({"field": "countries", "value": [c.strip() for c in re.split(r",| and ", m.group(1)) if c.strip()], "quote": m.group(0)})
        m = re.search(r"(\d+)\s+months", text)
        if m:
            proposals.append({"field": "timeline_months", "value": int(m.group(1)), "quote": m.group(0)})
        have = {p["field"] for p in proposals}
        return {"proposals": proposals, "missing": [f for f in ("expected_device_count", "countries", "timeline_months") if f not in have],
                "injection_suspected": bool(INJECTION.search(text)), "requires_review": True}

    return client.complete_json(prompt_id=pid, system=system, record=record, mock_responder=mock,
                                required_keys=["proposals", "missing", "injection_suspected", "requires_review"])


def personalization(record: Dict, client: LLMClient | None = None) -> Dict:
    pid, system = _system("personalization")
    client = client or LLMClient()

    def mock(r: Dict) -> Dict:
        signal = (r.get("signal") or "").strip()
        if not signal:
            return {"subject": "", "body": "", "signal_used": "", "skip_reason": "no signal provided", "requires_review": True}
        company = r.get("company", "your team")
        return {"subject": f"{company}: connectivity for the new devices",
                "body": f"Saw that {signal}. When devices ship in more than one country, how are you planning connectivity and billing for it?",
                "signal_used": signal, "skip_reason": "", "requires_review": True}

    return client.complete_json(prompt_id=pid, system=system, record=record, mock_responder=mock,
                                required_keys=["subject", "body", "signal_used", "skip_reason", "requires_review"])


def gate(action: str, confidence: float = 1.0) -> str:
    """Every agent action goes through here. Returns 'human_review' or 'auto_apply'."""
    return HITL.decide(action, confidence)
