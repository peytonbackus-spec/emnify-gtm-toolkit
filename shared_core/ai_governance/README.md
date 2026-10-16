# AI Workflow Standard

![Shared](https://img.shields.io/badge/supports-BOTH%20roles-7B61FF)

Production AI work needs four things: **production-ready** workflows; defined **prompts, outputs, evaluation criteria and human-in-the-loop controls**; **governance** for data security; and **measured realized gains**. Every AI workflow in this repo follows this one standard, whichever role uses it.

| Workflow | Role | Code |
|---|---|---|
| Account research & qualification brief | 🟦 GTM Engineer | [`gtm_engineer/ai_research/`](../../gtm_engineer/ai_research/) |
| Deal-risk detection + forecast commentary | 🟩 Strategy & Ops | [`gtm_strategy_ops/ai_deal_risk/`](../../gtm_strategy_ops/ai_deal_risk/) |
| Renewal signal brief | 🟩 Strategy & Ops | [`gtm_strategy_ops/renewals/`](../../gtm_strategy_ops/renewals/) |

## The six parts every AI workflow must have

| # | Part | What "done" means | Where it lives |
|---|---|---|---|
| 1 | **Prompt spec** | Versioned file with id, version, owner, inputs, output schema and refusal rules | `*/prompts/*.md` |
| 2 | **Output contract** | JSON with declared keys. Anything else is rejected, never "best-effort parsed". | [`llm_client.py`](llm_client.py) `OutputContractError` |
| 3 | **Data boundary** | Field allow-list plus PII redaction before the model sees anything | [`pii_guard.py`](pii_guard.py) |
| 4 | **Eval set** | 5+ fixed cases with checks, run in CI on every prompt change | [`eval_harness.py`](eval_harness.py), `*/evals/*.json` |
| 5 | **HITL policy** | Which actions auto-apply and which wait for a person. **Fail closed:** if a hook or check that guards an action fails, times out or cannot run, the action waits for a person; it never goes ahead by default. | [`hitl.py`](hitl.py) |
| 6 | **Impact metric** | The business number the workflow should move, with a baseline captured *before* launch | Table below |

## Data security

Adjust the strictness to the company's data. If its product handles identity documents, financial records or health data, a GTM workflow that leaks prospect or customer data into a model is a compliance problem as well as a credibility one.

- **Deny by default.** Only fields on the allow-list in `pii_guard.PROMPT_SAFE_FIELDS` reach a prompt. Email addresses, phone numbers, account and routing numbers, card numbers and DOBs are redacted from free text.
- **No customer production data in prompts.** Renewal health uses aggregated usage trends (volume % change, utilization %), never record-level data.
- **Audit log.** Every call writes prompt id@version, mode, input field names (not values) and PII actions to `outputs/ai_audit_log.jsonl`.
- **Vendor posture.** In live mode, use a provider and tier with zero-retention terms approved by the company's security team. The client reads the model from `GTM_LLM_MODEL`, then `ANTHROPIC_MODEL`, then falls back to `claude-sonnet-5-5` with a logged warning; pin it explicitly per environment.

## Measuring realized gains

Measure realized gains in conversion, speed and team capacity, and workflow impact on forecast accuracy and seller capacity.

| Workflow | Leading metric | Business metric | Baseline window |
|---|---|---|---|
| Account research brief | Brief acceptance rate (HITL Accept %) | SDR research minutes per account; MQL→SQL conversion | 4 weeks pre-launch |
| Lead qualification assist | Override rate on AI-suggested disqualifications | Speed-to-lead; SAL→SQL conversion | 4 weeks |
| Deal-risk flags | % of flags the AE/manager agrees with | Slipped-deal rate; forecast accuracy at week 8 of quarter | Prior 2 quarters |
| Forecast commentary | Manager edit distance on generated commentary | Hours spent on forecast-call prep | 2 forecast cycles |
| Renewal signals | Lead time between flag and renewal date | Gross retention on flagged vs unflagged accounts | Prior 4 quarters |

Rollout: shadow mode (generate but don't show) → assisted (shown to the rep, rep decides) → auto-apply for low-impact actions only.

## Extending the standard: plugins, mods and sub-agent effort

Agent tooling now lets third-party plugins change agent behavior, installs them from marketplaces, and lets you set how hard a sub-agent works. Treat each like a workflow that needs the six parts above, with five admission questions answered in writing before it is installed:

1. **Scope:** what can it read and write? Anything that writes to CRM metadata or sends externally needs a HITL gate on every write.
2. **Kind:** does it add a command, or change behavior (hooks, permissions)? Behavior changes are a policy decision.
3. **Provenance:** which marketplace and which pinned version?
4. **Owner:** one named person reviews updates.
5. **Stop rule:** the condition under which it halts and hands back to a person, written before the first run. Record two fields with it: the **notification owner** (the named person who tells affected people or teams when it stops or misbehaves) and the **time limit** for doing so. Both are set before an incident, not during one.

**Sub-agent effort is a risk setting, not a speed setting.** Cheap, easily checked work gets low effort; work whose errors propagate into routing, scoring or forecasts gets high effort and still gets review; anything that writes to the CRM or sends externally needs approval at every effort level. Effort never replaces `hitl.py`.

**After any agent-tool upgrade, re-test the allow rules.** Check that each allow, ask and deny rule still matches only the server or tool it names, and that a blocked action is still blocked, before relying on them. A rule that looked right can change meaning between releases: one coding-agent release (Claude Code v2.1.299) tightened how a bare server-name rule matched.

### Four audit questions for any agent that can write or send

Answer each in writing. "Not sure" counts as a gap to close.

1. Which MCP servers can an agent reach today, and who added each one?
2. If a check or hook fails, does the action stop or go ahead?
3. Is there a spend cap per automation, and who is the named owner of it (the person told when it trips)?
4. Who can join the workspace without an invite?

_Notes: based on the Claude Code release notes for v2.1.295 (Oct 8, 2026) and v2.1.299 (Oct 14, 2026), Anthropic's Oct 2026 account of unintended model actions during evaluations, and Oct 2026 admin-control announcements from Salesforce, HubSpot and Clay, captured in private research notes dated 2026-10-13 and 2026-10-14. Vendor statuses are as announced (several are beta) and the controls were not tested here. The audit questions are this repo's own synthesis, not a vendor checklist._

## Earned autonomy

[earned-autonomy.md](earned-autonomy.md) defines how a low-impact task moves from full review to spot-check, exceptions-only and auto, the evidence each step needs, and the triggers that demote it automatically. It never applies to actions on `always_review_actions` or above `large_deal_threshold` (decision #22). Third-party skills reviewed against this standard are listed in the [swan crosswalk](../../docs/crosswalks/swan-gtm-skills.md).
