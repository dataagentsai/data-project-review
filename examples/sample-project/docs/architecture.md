# Solution Architecture — Sales and Returns Insight

| | |
|---|---|
| Author | Tom Okafor (Technical Anchor) |
| Version | 0.9 |
| Last updated | Week 4 |

### 1. Overview

The solution lands data from StoreLink POS and Cartwell into the existing Azure Databricks platform, conforms it in silver, and publishes business-ready gold tables that feed a Power BI dashboard and a daily CSV extract for the Brightwave marketing tool. All tables live in Unity Catalog under the project schemas described in `platform-and-environments.md`.

```
StoreLink POS (SQL Server CDC) ──JDBC──► bronze.pos_*  ─┐
                                                        ├─► silver.* ──► gold.* ──► Power BI (Import, daily refresh)
Cartwell CSV ──► landing container ──Auto Loader──► bronze.cw_* ─┘                 └─► marketing extract (CSV → SFTP)
```

### 2. Ingestion

#### 2.1 POS (CDC)

- A Python notebook task connects over JDBC to the POS database using the project service account and calls `cdc.fn_cdc_get_net_changes_<table>` for each captured table, from the last processed LSN to the current maximum LSN.
- The last processed LSN per table is stored in `bronze._pos_watermark`.
- Rows are appended to `bronze.pos_<table>` with the operation code, LSN and extract timestamp.
- Reference tables `store` and `product` are small and are fully re-extracted each night.
- We originally planned Lakeflow Connect for SQL Server; this was dropped (see status report, week 3) because the ingestion gateway needs a network path the platform team cannot provide in time. The JDBC approach reuses the CDC tables already enabled.

#### 2.2 Cartwell (files)

- Cartwell pushes files to `landing/cartwell/<entity>/`.
- Auto Loader (`cloudFiles`, CSV, header on) reads each entity folder with `trigger(availableNow=True)` and appends to `bronze.cw_orders`, `bronze.cw_customers`, `bronze.cw_returns`.
- Schema is inferred by Auto Loader on first run and stored in the checkpoint schema location. File name and ingestion time are captured as `_source_file` and `_ingested_at`.

### 3. Transformation (silver)

| Silver table | Source | Logic |
|---|---|---|
| `silver.sales_line` | `bronze.pos_sales_line` + header | MERGE on `store_id, txn_id, line_no`. Rows with operation 2 (insert) are inserted; operation 4 (update after) updates the matching row. Ordered by LSN so the latest change wins. |
| `silver.online_order_line` | `bronze.cw_orders` | New bronze rows (since last run, by `_ingested_at`) are typed, cleaned and appended. |
| `silver.customer` | POS `customer` + `bronze.cw_customers` | Matched on loyalty number, else email. MERGE: matched rows updated with latest values, new rows inserted. |
| `silver.return_line` | POS `return_line` + `bronze.cw_returns` | Returns linked to original sale (POS txn or Cartwell order ref). MERGE on return id. |
| `silver.store`, `silver.product` | POS reference | Overwrite each night. |

Data quality rules (see `data-model.md` §5) run in silver using Lakeflow Declarative Pipelines expectations; failing rows are written to `silver._quarantine` with the rule name.

### 4. Gold

| Gold table | Grain | Build |
|---|---|---|
| `gold.dim_store` | store | Full rebuild |
| `gold.dim_product` | product | Full rebuild |
| `gold.dim_customer` | customer | Full rebuild from `silver.customer` |
| `gold.dim_date` | day | Static, generated once |
| `gold.fact_sales_daily` | store/online × day × product category | Incremental: each run recomputes `business_date = run_date - 1` and replaces that partition (`replaceWhere`) |
| `gold.fact_returns_daily` | store/online × original sale day × product category × reason | Incremental: returns received in the last run are aggregated to their original sale date and written for `business_date = run_date - 1` |

Gold facts are partitioned by `business_date`. Power BI uses Import mode with a scheduled refresh at 07:00.

### 5. Serving

- **Power BI** — one dataset over gold, row-level security by store and region using a mapping table maintained by finance.
- **Marketing extract** — a notebook task selects active customers from `gold.dim_customer` joined to last purchase, writes `hp_customers_YYYYMMDD.csv` and uploads it to the Brightwave SFTP.

### 6. Orchestration

A single Lakeflow Job, `hp_sales_daily`, scheduled at **05:00 UK time**:

1. `pos_extract` and `cartwell_autoloader` (in parallel)
2. `silver_pipeline` (depends on both)
3. `gold_build`
4. `marketing_extract`

Job clusters are defined in the asset bundle. Tasks run as the project service principal.

### 7. Design decisions

| # | Decision | Rationale |
|---|---|---|
| 1 | Medallion layers in Unity Catalog | Platform standard |
| 2 | JDBC over CDC tables instead of Lakeflow Connect | Network path not available in MVP timeframe |
| 3 | Daily batch at 05:00 | Fits finance's 09:00 review and store opening |
| 4 | Power BI Import mode | Faster dashboards; data changes once a day |
| 5 | Returns attributed to original sale date | Finance requirement (discovery §3) |
