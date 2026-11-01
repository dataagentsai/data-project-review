# Project Plan — Sales and Returns Insight MVP 1

| | |
|---|---|
| Owner | Sarah Lindqvist (PM) |
| Version | 1.1 |
| Baseline | Week 0 |
| Delivery approach | Two-week sprints, 6 sprints |

### 1. Goal

Deliver the daily sales and returns dashboard for finance and store managers, and the daily marketing customer extract, in production by the end of week 12.

### 2. Milestones

| # | Milestone | Target week | Exit criteria |
|---|---|---|---|
| M1 | Team mobilised, environments ready, source access in place | 1 | Developers can query POS test instance and read Cartwell sample files from dev |
| M2 | Bronze ingestion live in dev for POS and Cartwell | 3 | Nightly POS CDC and Cartwell loads running in dev from real test sources |
| M3 | Silver sales, online orders and customers complete | 5 | Tables built, DQ rules running, reviewed by BA |
| M4 | Silver returns complete; gold model built | 7 | Gold facts and dims populated in dev |
| M5 | Dashboard and marketing extract complete in test | 10 | All report pages built, RLS working, extract delivered to Brightwave sandbox |
| M6 | System integration and performance testing complete | 11 | SIT exit criteria met (see test strategy) |
| M7 | UAT sign-off and production go-live | 12 | Sponsor sign-off; first production run successful |

### 3. Sprint plan

| Sprint | Weeks | Focus | Key deliverables |
|---|---|---|---|
| 1 | 1–2 | Mobilise, access, ingestion patterns | Source access and connectivity confirmed (week 1); bundle and CI pipeline set up; POS watermark pattern; Auto Loader for Cartwell orders |
| 2 | 3–4 | Bronze complete, silver start | All POS tables and Cartwell entities landing nightly in dev; silver sales lines and online order lines |
| 3 | 5–6 | Silver | Silver customer merge; silver returns; DQ rules and quarantine |
| 4 | 7–8 | Gold | Dimensions; fact_sales_daily; fact_returns_daily; promote to test |
| 5 | 9–10 | Serving | Power BI dataset, RLS, report pages; marketing extract and SFTP |
| 6 | 11–12 | Test and go-live | SIT and performance (week 11); UAT and production deployment (week 12) |

### 4. Dependencies

| Dependency | Needed by | Provider |
|---|---|---|
| POS service account and firewall rule | Week 1 | Platform Team / InfoSec |
| Cartwell staging tenant pushing to test landing | Week 3 | Cartwell via e-commerce team |
| RLS mapping table (store manager → store) | Week 9 | Finance |
| Brightwave SFTP sandbox credentials | Week 9 | Brightwave |
| Retail calendar file | Week 7 | Finance |

### 5. Ceremonies

| Ceremony | Frequency | Attendees |
|---|---|---|
| Daily stand-up | Daily, 15 min | Project team |
| Sprint planning | Every 2 weeks | Project team, BA leads |
| Sprint review / demo | Every 2 weeks | Project team, finance controller |
| Steering update | Fortnightly | Sponsor, PM, Technical Anchor |
| Status report | Weekly (Friday) | Circulated by PM to stakeholder list |

### 6. Critical path

Source access → POS bronze → silver sales and customer → gold facts → dashboard → SIT → UAT → go-live.

Any slip in source access or silver customer merge moves go-live day for day, since the gold build and dashboard depend directly on them.

### 7. Go-live

- Production deployment in week 12 after UAT sign-off.
- First production run the following night; dashboard shared with finance and store managers once the first refresh has completed.
- Store managers receive a short "how to use the dashboard" guide prepared by the BA.
