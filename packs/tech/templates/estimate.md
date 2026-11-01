# Estimate: [project name]

Version: [n] · Date: [date] · Stage: [2 rough / 3 discovery / 6 re-estimate] · Prepared by: [name] · Replaces version: [n-1]

## What good looks like

The estimate is counted, not guessed: it lists the things the project will deliver, multiplies by a rate, and says where the rate came from (ideally the thin slice). It is a range, not one number, and the range narrows as evidence arrives. Its assumptions are written down, the most sensitive ones are marked, and each is also in the RAID log. It includes the work that is not building (access, environments, testing, data fixes, history load, cut-over, handover). It is dated and versioned, and it is redone against actual progress at least every two weeks during build, so nobody quotes a stale number as a promise.

## 1. Counted items

| Item type | Count | Complexity (S/M/L) | Rate per item (days) | Effort (days) |
|---|---|---|---|---|
| Sources to ingest | [n] | | | |
| Tables to build or change | [n] | | | |
| Data quality rules | [n] | | | |
| Reports, extracts or interfaces | [n] | | | |
| **Build subtotal** | | | | [ ] |

Where the rate came from: [thin slice on date / past project / expert guess, to be replaced by the thin slice]

## 2. Invisible work (do not delete a line; write 0 and why)

| Work | Effort (days) |
|---|---|
| Access and onboarding (requests, approvals, waiting) | |
| Environments and release pipeline | |
| Testing: reconciliation, data quality, performance, reruns | |
| User acceptance support | |
| Data fixes and handling bad rows | |
| History load and checking old numbers with the business | |
| Cut-over and rollback rehearsal | |
| Runbook, documentation and handover | |
| Early-life support after go-live | |
| Project management and meetings | |
| **Invisible work subtotal** | [ ] |

## 3. Range

| | Low | Most likely | High |
|---|---|---|---|
| Effort (days) | | | |
| Duration (weeks) with team of [n] | | | |

What moves it toward the high end: [ ] · What moves it toward the low end: [ ]

## 4. Assumptions

| # | Assumption | Effect if wrong | Most sensitive? | Owner | In RAID log? |
|---|---|---|---|---|---|
| A1 | [for example: read access to all sources by week 1] | [+n weeks] | Yes / No | [name] | Yes / No |

## 5. History of this estimate

| Version | Date | Range | Why it changed |
|---|---|---|---|
| 1 | [date] | [range] | Rough estimate before discovery |
