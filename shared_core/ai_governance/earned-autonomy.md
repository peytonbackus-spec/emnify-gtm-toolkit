# Earned Autonomy

Governance note for `shared_core/ai_governance`. It defines how a task (not an agent) earns less human review, and how it loses that autonomy automatically. It refines the `auto_apply` branch of [`hitl.py`](hitl.py).

**Scope limit (decision log #22):** earned autonomy never lifts decision #6. Every action on `HITLPolicy.always_review_actions`, every action at or above `large_deal_threshold`, and every revenue-affecting action stays at L0. The ladder applies only to low-impact actions that would otherwise run through the confidence threshold.

## The ladder

| Level | What ships without a human | What reaches the human |
|---|---|---|
| L0 Draft | Nothing with words in it | Every worded item, before it goes |
| L1 Spot-check | Items that passed the quality gate | A random sample, plus every low-confidence item |
| L2 Exceptions only | Items that passed the gate | Flagged, edge-case and high-risk items |
| L3 Auto | Scheduled runs that pass the gate | A periodic digest, plus any guardrail trip |

Actions with no words in them, and no claim (for example a profile view or a connection request with no note), may run at L0 within their rate limits. Anything worded waits at L0.

## Promotion is an argument from a log

| Criterion | L0 to L1 | L1 to L2 | L2 to L3 |
|---|---|---|---|
| Volume | 30 items reviewed | 50 items at L1 | Continuous |
| Quality | Edit or reject rate under 10% | Sampled gate-pass rate of 95% or more | Gate-pass rate holds |
| Outcome metric | Not required | Defined before reaching L2 | At or above target for 4 consecutive weeks |
| Guardrail breaches | None | None in the window | Zero |
| Logged refusal | Not required | At least one | At least one |

Further rules:
- **Separation of duties:** the agent never proposes its own promotion. A reviewer proposes; the person who carries the consequences approves.
- **Judgment steps are trusted separately.** Choosing the contact, choosing the angle and calling an account a fit each get their own count. A miss that costs credibility (wrong person, or a premise that shows no homework was done) resets that count to zero. A weak but harmless output doesn't.
- **Refusal as evidence.** The window must contain at least one substantive case where the task declined or flagged something inside its own authority. If that criterion is waived for a narrow mechanical task, the waiver is logged. A manufactured refusal counts as a breach.
- **Risk tags.** Tag every output low, medium or high risk when it ships. Read the distribution at promotion time; never average it away. A task hitting its numbers while emitting a disproportionate share of high-risk output gets split or held. The risk tag must not quietly bring back full review on work the task has already earned.

## Demotion is automatic

No approval is needed. Any one of these drops the task a level:
- the gate-pass rate falls below 90% over the last 20 items;
- the outcome metric misses target two weeks running.

Any guardrail breach drops the task straight to L0, with a notification.

## Guardrails no level crosses

- Channel volume caps.
- Suppression and do-not-contact lists.
- No unverified or stale claims; anything that needs legal or compliance sign-off goes to a human.
- The rubric's automatic-fail rules.
- A kill switch that freezes any task, or everything, to L0.
- **Live-reply floor:** responding to a live inbound conversation never runs above L0. On a reply, the sequence stops and routes to a human.

## Record keeping

Each task's current level, the date, the numbers that cleared it and the approver's name sit next to the review queue (`outputs/review_queue_*.csv`). Demotions appear in the record as often as promotions do. If nothing has ever been demoted automatically, the triggers are decoration.

_Source: adapted in our own words from swan-gtm/gtm-skills `skills/nadav-david/earned-autonomy` (MIT, © 2026 Swan). See the [crosswalk](../../docs/crosswalks/swan-gtm-skills.md)._
