---
id: schema-speed-to-lead-sla
type: schema-index
tags: [schema, mcp]
last_modified: 2026-09-25
---

# Speed-to-Lead SLA -- Tool I/O Schema

Companion note for `speed-to-lead-sla.schema.json` -- gives the JSON schema a markdown page so other notes can link to it with a real relative link instead of a bare filename.

**Real file:** `gtm-os/schemas/speed-to-lead-sla.schema.json` -- JSON Schema definitions for every tool [the speed-to-lead MCP server](../mcp/00-Automation-Layer-Index.md) implements (`crm_read_new_leads`, `calendar_read_no_shows`, `evaluate_sla_breach`, `slack_notify`, `sequencer_enqueue`), so any MCP client can validate calls against the same shapes the server and the contract both assume.

## See Also
[00-Automation-Layer-Index](../mcp/00-Automation-Layer-Index.md) . [speed-to-lead-sla-contract](../contracts/speed-to-lead-sla-contract.md)
