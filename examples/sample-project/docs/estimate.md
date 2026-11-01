# Estimate — Sales and Returns Insight MVP 1

| | |
|---|---|
| Author | Tom Okafor (Technical Anchor) |
| Prepared | End of discovery (week 0) |
| Reviewed with | Sarah Lindqvist (PM) |

### 1. Summary

**MVP 1 duration: 12 weeks** with the proposed team (technical anchor, 3 developers, BA, PM, part-time tester).

This is based on the feature breakdown below, using the team's experience on the 2025 Inventory Insight project, which delivered a similar scope (two sources, silver/gold, one Power BI dashboard) on the same platform.

### 2. Breakdown by feature

| # | Feature | Size | Developer-weeks | Notes |
|---|---|---|---|---|
| 1 | POS CDC ingestion (7 tables, watermark handling) | L | 6 | Reuse JDBC pattern from Inventory Insight |
| 2 | Cartwell file ingestion (3 entities, Auto Loader) | M | 3 | |
| 3 | Silver: sales lines and online order lines | M | 4 | |
| 4 | Silver: customer merge (POS + Cartwell) | L | 5 | Matching rules need BA input |
| 5 | Silver: returns with link to original sale | M | 4 | |
| 6 | Data quality rules and quarantine | S | 2 | Using pipeline expectations |
| 7 | Gold dimensions and facts | M | 4 | |
| 8 | Power BI dataset, RLS and 4 report pages | L | 5 | |
| 9 | Marketing extract and SFTP delivery | S | 2 | |
| | **Total** | | **35** | |

### 3. How the duration was derived

- 35 developer-weeks across 3 developers ≈ 11.7 weeks, rounded to **12 weeks**.
- The technical anchor reviews designs and code, unblocks the team and picks up build work where needed; not counted in the developer-weeks above.
- BA and PM effort runs alongside the build for the full 12 weeks.
- Part-time tester (2 days/week) from week 3.

### 4. Sizing guide used

| Size | Developer-weeks | Typical example |
|---|---|---|
| S | 1–2 | Single table transformation, simple extract |
| M | 3–4 | New source entity with cleaning and merge |
| L | 5–6 | Multi-table source, matching logic, or a full dashboard |

### 5. Comparison with Inventory Insight

| | Inventory Insight (2025) | Sales and Returns MVP 1 |
|---|---|---|
| Sources | 2 (ERP, WMS) | 2 (POS, Cartwell) |
| Silver tables | 6 | 6 |
| Gold tables | 5 | 6 |
| Dashboards | 1 | 1 |
| Duration | 11 weeks | 12 weeks |

### 6. Team and timeline

| Role | Allocation | Weeks |
|---|---|---|
| Technical anchor | 100% | 1–12 |
| Developers × 3 | 100% | 1–12 |
| Business analyst | 100% | 1–12 |
| Project manager | 50% | 1–12 |
| Tester | 40% | 3–12 |

### 7. Approval

Estimate presented with the discovery summary and accepted by the Sponsor at discovery sign-off.
