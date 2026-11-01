# Weekly Status Report — Week 5 of 12

**Project:** Sales and Returns Insight MVP 1  
**Prepared by:** Sarah Lindqvist (PM)  
**Distribution:** Claire Whitlow, Mark Haddad, Helen Osei, Daniel Reyes, core team

### 1. Overall status

| Area | RAG | Comment |
|---|---|---|
| Overall | 🟢 Green | On track for week-12 go-live |
| Scope | 🟢 Green | No change |
| Schedule | 🟢 Green | Sprint 3 started Monday as planned |
| Resources | 🟢 Green | Full team in place |
| Risks and issues | 🟢 Green | Being managed |

### 2. Summary

Good progress this week. Bronze ingestion for all Cartwell entities is running nightly in dev, and the silver sales line merge is complete with unit tests. The team demoed the first silver tables to Mark and the finance analysts at Wednesday's sprint review and the feedback was positive. Sprint 3 (silver customer and returns) is under way.

### 3. Progress against milestones

| Milestone | Target week | Status | Comment |
|---|---|---|---|
| M1 Team mobilised, environments ready, source access | 1 | Complete | Environments ready; POS work proceeding using DBA extract |
| M2 Bronze ingestion live in dev | 3 | Complete | Cartwell live in dev; POS bronze loading from static extract |
| M3 Silver sales, online orders, customers | 5 | In progress | Sales lines done; online orders 80%; customers 40% |
| M4 Silver returns; gold model | 7 | Not started | |
| M5 Dashboard and extract | 10 | Not started | Power BI wireframes reviewed |
| M6 SIT and performance | 11 | Not started | |
| M7 UAT and go-live | 12 | Not started | |

### 4. Completed this week

- `silver.sales_line` MERGE complete, 14 unit test cases passing in CI.
- Cartwell orders, customers and returns landing nightly in dev via Auto Loader.
- DQ rules DQ-01 to DQ-04 implemented as pipeline expectations.
- Power BI wireframes reviewed with Mark Haddad.
- Early performance run on the 1% sample: 9 minutes end to end.

### 5. Planned next week

- Customer merge workshop with finance (multiple loyalty cards per email).
- Complete `silver.online_order_line`.
- Start `silver.return_line`.
- Continue chasing POS service account approval.

### 6. Key risks and issues

| ID | Description | Status |
|---|---|---|
| I-02 | POS service account still awaiting InfoSec approval. Team using static extract from POS DBA meanwhile. | Chasing weekly |
| I-04 | Customer merge more complex than expected | Workshop booked |
| R-07 | Developer leave weeks 8–9 | Planned for |

### 7. Notes from this week's meetings

**Tuesday — technical sync (Tom, Aisha, Marcus, Jun)**
- Agreed to keep POS on the JDBC/CDC-functions approach for MVP 1; revisit Lakeflow Connect for MVP 2.
- Agreed that the marketing extract will be a full file every day rather than changes only, as Brightwave's import overwrites.
- Marcus to handle both date formats in Cartwell files (closed I-03).

**Wednesday — sprint review (team, Mark, finance analysts)**
- Mark confirmed returns are attributed to the original sale date, as in discovery.
- Mark asked whether click-and-collect returned in store shows as Online — agreed yes, it stays with the original channel.
- Finance analysts asked for a "returns by reason" page; BA to check against FR-05.

**Thursday — steering (Claire, Sarah, Tom)**
- Claire happy with progress. Asked for the dashboard to be ready for the January trading review.
- Agreed that store managers will only see the dashboard after the first week of production running, so finance can check numbers first.

### 8. Decisions needed

None this week.
