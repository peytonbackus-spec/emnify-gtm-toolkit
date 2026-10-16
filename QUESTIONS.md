# Questions for the team

Collected from the open items across [DECISIONS](DECISIONS.md), [ROADMAP](ROADMAP.md) and the [Amplemarket spec](outbound/amplemarket_handoff.md). Each one is a hypothesis in this repo that a single answer would confirm or replace.

## Data and systems
1. Which Salesforce objects and fields hold device count, countries and go-live date today? Are they populated?
2. How are Clay, ZoomInfo and Amplemarket used today: tables, credit model, who owns them?
3. Does Amplemarket write activity to Salesforce directly, or does Weflow capture it?
4. Where do Attention call summaries land, and who owns them?
5. Is n8n self-hosted or cloud, and who can approve a new workflow?
6. What is the do-not-contact source of truth?

## Revenue and forecasting
7. Which revenue metric is this role measured on, and what is the first target?
8. How is a usage-based opportunity forecast today? What is the realized-versus-expected history?
9. What is the fiscal calendar and territory model?

## Motion and ICP
10. Which verticals produce the most realized usage revenue, and which are on the website but not in the pipeline?
11. Which signals, if any, have preceded a connectivity decision before?
12. Who owns a sequence once an account has a rep?

## Guardrails
13. What may be written to Salesforce without review, and by whom is it approved?
14. What are the data-handling terms for sending account data to Claude?
