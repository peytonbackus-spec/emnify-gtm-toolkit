---
id: contract-crm-cleanup
type: contract-index
tags: [contract, workflow-contract, data-quality, crm]
last_modified: 2026-10-13
---

# CRM Cleanup Agent -- Workflow Contract

Companion note for [`crm-cleanup-contract.yaml`](crm-cleanup-contract.yaml).

**Objective:** turn data-quality findings into an operation-level correction plan. Only the operations a human approved by ID get applied, and the result is proven by re-running the same audit.

**Role map:**
1. `baseline_agent`: snapshot, with the checks written as rules.
2. `planner_agent`: one reviewable operation per change.
3. `executor_agent`: re-read before writing, skip stale values, apply approved IDs only.
4. `verifier_agent`: re-audit and reconcile.

**Reads:** [`dq_monitor.py`](../../shared_core/data_quality/dq_monitor.py) and its `outputs/dq_failures.csv`. **Writes:** a cleanup plan and an apply log in `outputs/`. **MCP tools:** `crm_read`, `crm_update_approved_ops`, `slack_notify`.

**Where it fits:** `dq_monitor.py` finds failures, and [CRM Health Scoring](../playbooks/CRM_Health_Scoring.md) measures the trend. This contract is the only path by which an agent changes the records behind either. Field-level write permissions come from [field and agent-write governance](../../shared_core/data_quality/field-and-agent-write-governance.md).

**Worked example (from the source):**
- **The defects:** 312 ownerless contacts, all from one form integration whose fallback owner was removed. The source gets fixed first.
- **The first batch:** 50 deterministic territory assignments. 12 conflicts go to people to decide.
- **At apply time:** one contact had gained an owner since planning. It was skipped as stale.
- **Reconciliation:** 50 planned, 49 applied, 1 stale, 0 unexplained.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/ryan-iyengar/governed-crm-cleanup` (MIT, © 2026 Swan). See the [crosswalk](../crosswalks/swan-gtm-skills.md)._

## See Also
[CRM_Health_Scoring](../playbooks/CRM_Health_Scoring.md) . [hitl.py](../../shared_core/ai_governance/hitl.py) . [decision log #6](../overview/decision-log.md)
