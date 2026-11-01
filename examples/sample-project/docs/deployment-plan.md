# Deployment Plan — Sales and Returns Insight MVP 1

| | |
|---|---|
| Author | Jun Park (Developer), reviewed by Tom Okafor |
| Version | 0.8 |
| Last updated | Week 5 |

### 1. Purpose

Describe how code and configuration move from development to production, and the steps for the week-12 go-live.

### 2. Repository and branching

- Single Azure DevOps repo: `hp-sales-insight`.
- Layout:

```
hp-sales-insight/
  databricks.yml            # Databricks Asset Bundle, targets dev / test / prod
  resources/                # job and pipeline definitions
  src/hp_sales/             # Python modules (ingestion, silver, gold, extract)
  notebooks/                # thin entry-point notebooks calling src modules
  conf/                     # environment settings (dev.yaml, test.yaml, prod.yaml)
  powerbi/                  # PBIP project for the dataset and report
  tests/                    # unit tests and fixtures
```

- Trunk-based: short-lived feature branches off `main`, merged by pull request.
- Pull requests need one approving review (Technical Anchor or another developer) and a green CI build.
- `main` is protected; no direct pushes.

### 3. Configuration

Environment-specific settings live in `conf/<env>.yaml` and are read by the entry-point notebooks at runtime:

| Setting | Example (dev) |
|---|---|
| `catalog` | `hp_dev` |
| `pos.jdbc_host` | `stlk-tst01.hp.local` |
| `pos.user` / `pos.password` | service account credentials for the POS instance |
| `sftp.host` / `sftp.user` / `sftp.key_path` | Brightwave SFTP details |
| `landing_path` | `/Volumes/hp_dev/bronze/landing/cartwell` |

### 4. CI/CD pipeline

| Stage | Trigger | Steps |
|---|---|---|
| CI | Every pull request | Lint (ruff), unit tests (pytest), `databricks bundle validate` for all targets |
| Deploy dev | Merge to `main` | `databricks bundle deploy -t dev` |
| Deploy test | Manual approval by Technical Anchor | `databricks bundle deploy -t test`; Power BI dataset published to Test workspace via deployment pipeline |
| Deploy prod | Manual approval by Technical Anchor and PM; release tag `vX.Y.Z` on `main` | `databricks bundle deploy -t prod` using the prod service principal; Power BI deployment pipeline promotes Test → Prod |

The pipeline uses the Platform Team's YAML templates. Prod deployment runs as `sp-hp-sales-prod`; no individual has deploy rights to prod.

### 5. Go-live steps (week 12)

| # | Step | Who | When |
|---|---|---|---|
| 1 | UAT sign-off received from Sponsor | PM | Wk 12, Tue |
| 2 | Tag release `v1.0.0` on `main` | Technical Anchor | Wk 12, Wed |
| 3 | Run prod deployment pipeline | Technical Anchor | Wk 12, Wed |
| 4 | Confirm schemas, volumes and grants created in `hp_prod` | Developer | Wk 12, Wed |
| 5 | Confirm Cartwell production is pushing to `hp_prod` landing | Developer + e-commerce team | Wk 12, Wed |
| 6 | Enable `hp_sales_daily` schedule | Technical Anchor | Wk 12, Wed |
| 7 | First nightly run; check job succeeded and row counts are non-zero | Developer | Wk 12, Thu 05:00–07:00 |
| 8 | Power BI refresh completes; share app with finance and store managers | BA | Wk 12, Thu |
| 9 | First marketing extract delivered to Brightwave production folder | Developer | Wk 12, Thu |
| 10 | Go-live confirmation email to stakeholders | PM | Wk 12, Thu |

### 6. Monitoring after go-live

- Job failure notifications from Lakeflow Jobs are sent by email to the `hp-sales-dev` distribution list.
- The DQ results page in the dashboard shows quarantine counts per run.

### 7. Release notes

Each production release gets a short release note in the repo wiki: version, date, changes, and any manual steps.
