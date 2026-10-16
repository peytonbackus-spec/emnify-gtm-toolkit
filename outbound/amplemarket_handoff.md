# Amplemarket handoff spec

Status: spec plus an offline builder ([handoff.py](handoff.py)). The Amplemarket push is a stub ([integrations/clients.py](../integrations/clients.py)); no list was sent anywhere. How emnify uses Amplemarket today (lists, sequences, ownership) is hypothesis: validate.

## Flow

1. [scoring.py](scoring.py) ranks accounts; suppressed accounts (customer, open opportunity, do-not-contact) are dropped before ranking matters.
2. [handoff.py](handoff.py) builds one row per account at or above the minimum tier and validates it against [the contract](../integrations/contracts/amplemarket_handoff.yaml).
3. A row with no `approved_by`, or any contract error, goes to `held`, never `ready`.
4. A human approves the list and the first messages from [agents/personalization](../agents/prompts/personalization.md).
5. The n8n step pushes `ready` rows ([integrations/n8n](../integrations/n8n/enrichment-intake.json) pattern) and records the push against the Salesforce account.

## Open questions for the team

- Who owns a sequence once the account has a rep?
- Does Amplemarket write activity to Salesforce directly, or does Weflow capture it?
- What is the do-not-contact source of truth?
- Which first-touch metric is trusted: reply rate, meeting rate, or pipeline created per 100 accounts worked?
