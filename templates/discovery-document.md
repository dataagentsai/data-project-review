# Discovery document: [project name]

Version: [n] · Date: [date] · Stage: [3 Discovery / 4 Sign-off] · Owners: [business analyst], [technical anchor], [project manager]

## What good looks like

One document with three owners (business analyst, technical anchor, project manager) in which every section is based on real data, not guesses. Real data from every source has been profiled and shown to the business owner. A thin slice (one table through every layer to one report) has run in a production-like environment, or the gap is a named risk. Scope is written as in, out and later, including the ten scope traps. The estimate is a range built from the thin slice's real rate. Reviewers had the document at least three days before sign-off, and their findings are answered in writing. The sponsor then decides: go, go with changes, or stop.

## 1. Business goals and success measures
*Owner: business analyst. Reviewed by: business owner.*

| Goal | Measure | Today's value (baseline) | Target | Where the data comes from |
|---|---|---|---|---|
| [goal] | [measure] | [value] | [value] | [source] |

## 2. Requirements and acceptance criteria
*Owner: business analyst. Reviewed by: business owner, test lead.*

| Id | Requirement (no vague words) | Acceptance criteria: given this data, the result is | Users who need it |
|---|---|---|---|
| R-1 | [requirement] | [testable criteria, ideally a figure the business already trusts] | [users] |

## 3. Sources and data profiling
*Owners: business analyst and technical anchor. Reviewed by: source system owners.*

| Source | Owner | Volume and growth | Keys | Deletes | Late or corrected rows | Quality findings | Shown to business owner on |
|---|---|---|---|---|---|---|---|
| [source] | [name] | [rows/day] | [key] | [how] | [how] | [nulls, duplicates, broken keys] | [date] |

## 4. Definitions and data model
*Owners: business analyst and technical anchor. Reviewed by: data consumers, domain owner.*

| Term | Exact rule | Grain | Owner who signed | Date |
|---|---|---|---|---|
| [term] | [rule] | [grain] | [name] | [date] |

## 5. In scope and out of scope
*Business analyst writes, anchor checks. Reviewed by: business owner, project manager.* See [scope.md](scope.md).

## 6. Application architecture
*Owner: technical anchor. Reviewed by: architect, a peer anchor.*

- Data flows and layers: [link or one-page drawing]
- Patterns per source: [batch / change capture / files / API …]
- Non-functional needs: freshness [ ], volume [ ], recovery time [ ], acceptable data loss [ ], retention [ ]
- Decision records: [links, see [decision-record.md](decision-record.md)]
- Thin slice result: [what ran, where, how long, what broke]

## 7. Platform architecture
*Owner: technical anchor with the platform team. Reviewed by: platform team, security, operations.*

Environments [ ] · Network [ ] · Identity and access [ ] · Security [ ] · Release pipeline [ ] · Monitoring [ ] · Running cost [ ]

## 8. Estimation
*Owners: technical anchor (effort), project manager (plan). Reviewed by: project manager, a peer anchor.* See [estimate.md](estimate.md).

## 9. Plan, MVPs and team
*Owner: project manager. Reviewed by: delivery lead, business owner.*

| MVP | Contents | Why this order | Target date | Depends on |
|---|---|---|---|---|
| MVP 1 | [smallest slice with real value] | [value / riskiest beliefs] | [date] | [dependencies] |

Team: [role: name, availability] · Estimate assumptions this plan uses: [list]

## 10. Test strategy
*Owner: technical anchor with the test lead. Reviewed by: test lead, business users.* See [test-strategy.md](test-strategy.md).

## 11. Release and run approach
*Owner: technical anchor. Reviewed by: operations, release manager.* See [release-and-cutover.md](release-and-cutover.md).

## 12. Risks, assumptions, issues, dependencies
*Owners: project manager (log), technical anchor (technical items). Reviewed by: all reviewers.* See [raid-log.md](raid-log.md). Riskiest assumptions and how each was tested: [list]

## 13. Stakeholder map and communication
*Owner: project manager. Reviewed by: delivery lead.* See [stakeholder-map.md](stakeholder-map.md).

## 14. Decisions, change process and sign-off
*Owner: project manager. Reviewed by: business owner.*

- Decision log: [link]. Open decisions each have an owner, a deadline and a default.
- Change process: who raises, who sizes, who decides, how plan and estimate change.
- Reviewer findings and answers: [table or link]
- Sign-off: [name, role, date, decision: go / go with changes / stop, conditions]
