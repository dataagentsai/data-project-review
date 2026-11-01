# Pre-mortem: [project name]

Date: [date] · Stage: [n] · Facilitator: [name] · Attendees: [names, including people outside the weekly meeting]

## What good looks like

A pre-mortem imagines the project has already failed and asks why. Because the failure is treated as certain, people say the things they would otherwise keep quiet. A good one takes thirty minutes, includes someone from operations, security, a source system and the business, not only the project team, and ends with each top cause turned into a risk with an owner, a trigger and a mitigation, or into a fail-fast test to run this week. Run one before discovery sign-off and again before go-live. The `question` field of every delivery check in this bundle can be read out as a prompt.

## How to run it (30 minutes)

| Minutes | Step |
|---|---|
| 0 to 3 | The facilitator says: "It is [date six months from now]. The project has failed badly. It is late, over budget, or nobody uses it." |
| 3 to 10 | Everyone writes, alone and in silence, every reason it failed. One reason per note. No discussion yet. |
| 10 to 18 | Go round the room, one reason per person per turn, until every note is read. Group similar ones. Nobody defends the plan. |
| 18 to 23 | Each person gets three votes for the causes that are most likely and most damaging. |
| 23 to 30 | For the top five: name an owner, a trigger that would show it is happening, and the cheapest test or mitigation to start this week. |

## Prompts if the room goes quiet

- Which belief, if wrong, would sink the whole project, and have we tested it with real data?
- Whose "no" at go-live would stop us, and when did we last speak to them?
- Which number in the plan was a guess that became a promise?
- What does everyone in this room assume is out of scope, and is it written down?
- What do we know today that the sponsor does not?
- If the person who knows the most left next month, what would stop?
- Would the business recognise our numbers as right?
- Have we rehearsed both the cut-over and the rollback?

## Causes and actions

| # | Cause of failure | Votes | Owner | Trigger | Test or mitigation this week | Added to RAID log as |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## Follow-up

Reviewed again on: [date] · Causes that came true or were prevented: [notes]
