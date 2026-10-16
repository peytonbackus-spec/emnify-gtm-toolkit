# emnify GTM Toolkit Wiki

**An outbound engine and enrichment layer for consumption-based IoT connectivity.** This wiki is the narrative layer on top of the [repository](https://github.com/peytonbackus-spec/emnify-gtm-toolkit/blob/main/README.md). The repo holds the working code; the wiki explains the thinking.

> Everything about emnify here is a **hypothesis: validate**. I have no access to emnify's systems or data. Stack facts come from the posting, vertical facts from the public website, data is synthetic.

| Module | What it answers | Start with |
|---|---|---|
| Enrichment | How does a domain become a Salesforce-ready account without duplicates or silent overwrites? | [[Enrichment]] |
| Outbound | Which accounts first, and does the list cover the target when revenue is usage-based? | [[Outbound and Coverage]] |
| Agents | How do Claude agents help without writing to the CRM unreviewed? | [[Agents and Governance]] |
| Integrations | What are the contracts, retries and failure paths between systems? | [[Integrations]] |
| Knowledge | How do people and agents read the same process source? | [[Knowledge Layer]] |

## Pages

- [[Architecture]]: the flow from signal to Salesforce and where the human gate sits
- [[ICP Hypotheses]]: seven verticals from the public site, nothing ranked yet
- [[Decision Log]]: nine choices and six illustrative push-backs
- [[Roadmap]]: weeks 1-4, months 2-3, months 4-6
- [[Running the Toolkit]]: every command
- [[Glossary]]

## Ground rules

- **Synthetic data only.** Fixtures are fictional.
- **No overclaiming.** The only results quoted are four confirmed ones from a previous role, listed in the [README](https://github.com/peytonbackus-spec/emnify-gtm-toolkit/blob/main/README.md), never attributed to emnify.
