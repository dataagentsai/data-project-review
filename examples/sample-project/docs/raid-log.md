# RAID Log — Sales and Returns Insight MVP 1

Maintained by: Sarah Lindqvist (PM). Last updated: week 5.

## Risks

| ID | Raised | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|
| R-01 | Wk 0 | POS access approval is slow: InfoSec approval for a new service account plus a firewall change typically takes about 6 weeks end to end | High | High | Request submitted in week 1; escalate through Platform Team if not approved by week 4 | | Open |
| R-02 | Wk 0 | Customer matching between POS loyalty and Cartwell produces false matches | Medium | Medium | BA to agree matching rules with finance; DQ checks on match rate | | Open |
| R-03 | Wk 1 | Cartwell staging tenant cannot push to our test landing container in time | Medium | Medium | Use sample files from production (masked) until ready | | Open |
| R-04 | Wk 2 | December peak volume (2.3× normal) may extend nightly run | Low | Medium | Autoscaling job clusters | | Open |
| R-05 | Wk 2 | Store managers find Power BI hard to use | Medium | Low | BA to prepare guide; demo at regional managers' meeting | Priya | Open |
| R-06 | Wk 3 | Finance retail calendar for 2027 not yet published | Low | Medium | Use 2026 pattern as placeholder | | Open |
| R-07 | Wk 4 | Developer annual leave in weeks 8–9 (one developer, 2 weeks) | Certain | Medium | Front-load gold design | | Open |

## Assumptions

| ID | Assumption | Validated? |
|---|---|---|
| A-01 | Existing Databricks platform and Power BI capacity have room for the new workload | Yes — Platform Team, week 1 |
| A-02 | POS test instance holds production-like data refreshed monthly | Partly — last refresh was 4 months ago |
| A-03 | Finance will provide the RLS mapping of managers to stores | Not yet |
| A-04 | Cartwell file layouts are as documented in their spec v3.2 | Yes |
| A-05 | Business users already have Power BI Pro licences | Yes |

## Issues

| ID | Raised | Issue | Impact | Action | Owner | Status |
|---|---|---|---|---|---|---|
| I-01 | Wk 2 | Lakeflow Connect ingestion gateway needs a network path not available this quarter | POS ingestion design change | Switched to JDBC over CDC functions (week 3) | Tom | Closed |
| I-02 | Wk 3 | POS service account not yet approved; developers working from a static extract supplied by the POS DBA | POS CDC logic cannot be tested against a live source | Chase InfoSec weekly | Sarah | Open |
| I-03 | Wk 4 | Cartwell sample files use a different date format (dd/MM/yyyy) to the spec (ISO) | Parsing failures in bronze → silver | Handle both formats in silver | Marcus | Closed |
| I-04 | Wk 5 | Customer merge logic more complex than expected (multiple loyalty cards per email) | Silver customer later than planned | BA workshop with finance, week 6 | Jun | Open |

## Dependencies

| ID | Dependency | On | Needed by | Status |
|---|---|---|---|---|
| D-01 | POS service account (InfoSec approval) | InfoSec | Week 1 | Submitted week 1, pending |
| D-02 | Firewall rule workspace subnets → POS port 1433 | Platform Team | Week 1 | Submitted week 1, waiting for service account approval |
| D-03 | Cartwell staging tenant push to test landing | E-commerce team / Cartwell | Week 3 | In progress |
| D-04 | RLS mapping table | Finance | Week 9 | Not started |
| D-05 | Brightwave SFTP sandbox credentials | Brightwave | Week 9 | Not started |
| D-06 | Retail calendar file | Finance | Week 7 | Not started |
