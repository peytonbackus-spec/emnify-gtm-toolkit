"""emnify GTM agents: prompts, offline workflows, eval cases, human-review gate.

The inherited PII guard is deny-by-default. These fields are the emnify additions; they hold no personal data.
"""
from shared_core.ai_governance import pii_guard

pii_guard.PROMPT_SAFE_FIELDS.update({"iot_vertical", "expected_device_count", "countries", "signal"})
