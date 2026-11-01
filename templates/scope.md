# Scope: [project name]

Version: [n] · Date: [date] · Signed by business owner: [name, date]

## What good looks like

Scope is written as three lists (in, out and later), each item specific enough that a stranger could say which list a new request belongs to. The ten data scope traps each have an explicit answer, because anything not written as out of scope will be assumed to be in. Every "later" item says whether the first release depends on it, so "phase 2" does not hide work the project cannot live without. The business owner has signed this version, and any change after sign-off goes through the change process and the change log below.

## In scope

| # | Item | Requirement ids |
|---|---|---|
| I1 | [item] | [R-1] |

## Out of scope

| # | Item | Why out | Agreed by |
|---|---|---|---|
| O1 | [item] | [reason] | [name] |

## Later (not in this release)

| # | Item | Does the first release depend on it? | Owner | Funded? |
|---|---|---|---|---|
| L1 | [item] | Yes / No | [name] | Yes / No |

## The ten data scope traps

| Trap | Question | Answer: in / out / later, and detail | Decided by |
|---|---|---|---|
| History and backfill | Load how many years? Who checks the old numbers? | | |
| Deletes at the source | Disappear here, be flagged, or stay? | | |
| Late and corrected data | Which days do we rebuild when data is corrected? | | |
| Changes over time | Keep history of changes, or only the latest value? | | |
| Bad rows | Reject the batch, quarantine the rows, or load and flag? Who fixes them? | | |
| Data quality at the source | Fix the source's mistakes, or report them? | | |
| Personal data | Masking, retention, right to be forgotten: ours or someone else's? | | |
| Reports and dashboards | Are the reports in scope, or only the tables? | | |
| Access and onboarding | Who requests and approves user access? | | |
| Recovery | How fast must it recover, and how much data may be lost? | | |

## Change log

| # | Date | Requested by | Change | Effect on effort and date | Decision | Decided by |
|---|---|---|---|---|---|---|
| C1 | | | | | Accepted / Rejected / Later | |
