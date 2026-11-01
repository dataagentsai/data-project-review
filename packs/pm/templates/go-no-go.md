# Go or no-go checklist: [project name], release [name or number]

Agreed on: [date, at least two weeks before cut-over] by [business owner] · Decision meeting: [date and time] · Decider: [one named person]

## What good looks like

The criteria are written and agreed with the business owner weeks before cut-over, so the go or no-go meeting checks evidence instead of debating the date. Every line names the evidence that proves it and the person who confirms it, and says in advance what happens if it fails: delay, go with a stated workaround, or release only part. Data criteria come first, because data releases rarely fail on code alone: numbers reconciled against figures the business already trusts, the history load complete and checked, and the first loads timed against the cut-over window. Business readiness counts as much as technical readiness: users told and trained, the service desk briefed, every consumer of the old data warned, and a parallel run that covers a month-end. One person decides, and the decision and its reasons are recorded the same day.

## Data and testing

| # | Criterion | Evidence | Confirmed by | Met? (Y/N) | If not met |
|---|---|---|---|---|---|
| D1 | Key numbers reconcile with the business's trusted figures, within the agreed tolerance, for [periods] | Reconciliation report | Business owner, test lead | | |
| D2 | History load complete and checked for every year in scope | History load reconciliation | Technical anchor | | |
| D3 | No open critical or high defects; medium defects have an agreed workaround | Defect list | Test lead | | |
| D4 | User acceptance signed by the named testers | Sign-off record | Business owner | | |
| D5 | Final loads timed in a rehearsal and fit the cut-over window with margin | Rehearsal log | Technical anchor | | |

## Release and rollback

| # | Criterion | Evidence | Confirmed by | Met? | If not met |
|---|---|---|---|---|---|
| R1 | Cut-over plan with timed steps, owners and a go-back deadline | Cut-over runbook | Project manager | | |
| R2 | Rollback of code and data rehearsed | Rehearsal log | Release and DevOps | | |
| R3 | No clashing release to sources, platform or shared data in the window | Change calendar | Technical anchor | | |
| R4 | Business freeze agreed for the cut-over window | Written agreement | Business owner | | |

## Support and operations

| # | Criterion | Evidence | Confirmed by | Met? | If not met |
|---|---|---|---|---|---|
| S1 | Support team has accepted the system, hours and response times | Signed support model | Operations lead | | |
| S2 | Runbook reviewed and used by support in a rehearsal | Runbook, rehearsal notes | Operations lead | | |
| S3 | Alerts reach a named person out of hours | Test alert record | Operations lead | | |
| S4 | Project team booked for early-life support past the first month-end | Plan, bookings | Project manager | | |

## Business readiness

| # | Criterion | Evidence | Confirmed by | Met? | If not met |
|---|---|---|---|---|---|
| B1 | Users told what changes and when, including definitions that changed and why numbers differ | Communications sent | Business analyst | | |
| B2 | Users trained | Attendance list | Business owner | | |
| B3 | Service desk briefed | Briefing note | Project manager | | |
| B4 | Every consumer of replaced tables and feeds told, including those found in access logs | Consumer list with confirmations | Project manager | | |
| B5 | Parallel run planned through [month-end], with a person comparing old and new | Plan | Business owner | | |
| B6 | Switch-off dates agreed for the old reports and feeds | Switch-off list | Business owner | | |

## Approvals

| # | Criterion | Evidence | Confirmed by | Met? | If not met |
|---|---|---|---|---|---|
| A1 | Security and privacy approvals in place | Approval records | Security | | |
| A2 | Change board approval for the release window | Change record | Release and DevOps | | |
| A3 | Conditions from earlier gates closed | Gate conditions list | Project manager | | |

## Decision

Decision: Go / Go with conditions / No-go · Decided by: [name] · Date: [date]

Reasons, and any criterion not met with the workaround accepted:

Conditions, each with owner and date:
