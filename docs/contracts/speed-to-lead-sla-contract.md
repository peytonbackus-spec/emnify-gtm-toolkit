---
id: contract-speed-to-lead-sla
type: contract-index
tags: [contract, workflow-contract, inbound-sdr]
last_modified: 2026-09-25
---

# Speed-to-Lead SLA Agent -- Workflow Contract

Companion note for `speed-to-lead-sla-contract.yaml` -- gives the YAML contract a markdown page so other notes can link to it with a real relative link instead of a bare filename.

**Real file:** `gtm-os/contracts/speed-to-lead-sla-contract.yaml`

**Objective:** Enforce SLA response windows on inbound leads by score tier, and trigger no-show recovery cadences for missed booked meetings. **Role map:** `sla_timer_agent` (per-tier SLA clock + escalation) -> `noshow_recovery_agent` (3-touch recovery cadence via milestone-sequencer). **Reads:** `wiki/skills/inbound-playbook`, `wiki/competitive/Chili Piper`. **Writes:** `intelligence/daily/`. **MCP tools:** `calendar_read`, `crm_read`, `slack_notify`, `sequencer_enqueue`. Promoted from the human-invoked [speed-to-lead-sla-enforcer](../agents/speed-to-lead-sla-enforcer.md) prompt agent.

> **Automation built (proof of concept):** [the speed-to-lead MCP server](../mcp/speed-to-lead/README.md) implements this contract's tools -- 1 of 5 is real logic, 4 are mocked pending CRM/calendar/Slack/sequencer credentials.

## See Also
[speed-to-lead-sla-enforcer](../agents/speed-to-lead-sla-enforcer.md) . [00-Agent-Router](../agents/00-Agent-Router.md) . [full-org-agent-taxonomy](../../wiki/concepts/full-org-agent-taxonomy.md)
