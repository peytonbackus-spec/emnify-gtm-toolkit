---
id: contract-pipeline-risk
type: contract-index
tags: [contract, workflow-contract, revops]
last_modified: 2026-09-25
---

# Pipeline Risk Agent -- Workflow Contract

Companion note for `pipeline-risk-contract.yaml` -- gives the YAML contract a markdown page so other notes can link to it with a real relative link instead of a bare filename.

**Real file:** `gtm-os/contracts/pipeline-risk-contract.yaml`

**Objective:** Identify stalled enterprise deals in SFDC with zero Gong call activity for 14+ days. **Role map:** `data_audit_agent` (SFDC field history + stage velocity) -> `synthesis_agent`. **Reads:** `wiki/accounts/`, `raw-sources/transcripts/`. **Writes:** `intelligence/daily/`. **MCP tools:** `sfdc_read`, `gong_search`, `slack_notify`. This is the precedent contract every other role_map in this repo is modeled on.

## See Also
[00-Prompt-Library-Index](../agents/00-Prompt-Library-Index.md) . [full-org-agent-taxonomy](../../wiki/concepts/full-org-agent-taxonomy.md) . [00-Agent-Router](../agents/00-Agent-Router.md)
