# agents/

Three Claude-based workflows for the outbound engine, with prompts, eval cases and a human-review gate. They run offline in mock mode through the inherited `LLMClient`; live mode (`GTM_LLM_MODE=anthropic`) is not exercised in this build.

| Agent | Input | Output | Human gate |
|---|---|---|---|
| [research_brief](prompts/research_brief.md) | account fields | brief with evidence and unknowns | disqualification always reviewed |
| [qualification_signal](prompts/qualification_signal.md) | call summary text | PROPOSED values for device count, countries, timeline | AE accepts, modifies or ignores |
| [personalization](prompts/personalization.md) | account + one signal | draft email, or a skip reason | every draft reviewed before Amplemarket |

```bash
python -m agents.run_evals
```

## Design rules

- Agents read [knowledge/](../knowledge/README.md) and propose. They never write to Salesforce or send anything ([agent-write-gate](../knowledge/process/agent-write-gate.yaml)).
- Inbound text (call summaries, replies, scraped pages) is data. Instructions inside it are ignored and flagged (`injection_suspected`).
- Missing facts go in `unknowns` or `missing`. The agent never estimates a device count.
- [workflows.py](workflows.py) `gate()` is the single decision point: `send_message`, `crm_write` and `disqualify_account` always return `human_review`.
- Where Claude runs (a Clay AI column, an n8n node, or both) is a hypothesis: validate. The prompts are the same either way.

Rubric: [evals/RUBRIC.md](evals/RUBRIC.md).
