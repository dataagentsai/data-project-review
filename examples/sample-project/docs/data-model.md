# Data Model — Sales and Returns Insight

| | |
|---|---|
| Authors | Aisha Bello (Developer), Priya Raman (BA) |
| Version | 0.7 |
| Last updated | Week 5 |

### 1. Scope

This document describes the silver and gold tables, the business meaning of gold measures, the marketing extract layout, and the data quality rules applied in silver. Bronze tables mirror the source and are not described here.

### 2. Silver tables (summary)

| Table | Key | Notes |
|---|---|---|
| `silver.sales_line` | `store_id, txn_id, line_no` | One row per POS sales line; amounts in GBP including VAT; `discount_amount` per line |
| `silver.online_order_line` | `order_id, line_no` | One row per Cartwell order line; same amount conventions as POS |
| `silver.customer` | `customer_id` (surrogate) | Merged POS loyalty and Cartwell customers; `loyalty_no`, `email`, `phone`, `first_name`, `last_name`, address lines, `postcode`, `home_region`, `marketing_opt_in` |
| `silver.return_line` | `return_id, line_no` | `original_channel`, `original_txn_ref`, `original_sale_date`, `return_date`, `reason_code`, `refund_amount` |
| `silver.store`, `silver.product` | natural keys | Reference data from POS |

### 3. Gold model

Star schema for Power BI.

#### 3.1 Dimensions

| Dimension | Grain | Key attributes | Notes |
|---|---|---|---|
| `dim_date` | day | date, week (Mon–Sun), retail period, fiscal year (starts 1 Feb) | Generated 2020–2030 |
| `dim_store` | store | store_id, name, trading_region, format, open_date | 42 stores + "Online" pseudo-store |
| `dim_product` | product | sku, description, category, sub_category, brand | |
| `dim_customer` | customer | customer_key, home_region, postcode_district, loyalty_tier, first_purchase_date | One row per customer, rebuilt nightly from `silver.customer`; attributes hold the latest values from source |
| `dim_channel` | channel | Store, Online | |

#### 3.2 Facts

**`fact_sales_daily`** — grain: business_date × store × product category × channel.

| Column | Definition |
|---|---|
| `business_date` | Trading date of the sale (POS txn date; Cartwell order date) |
| `transactions` | Count of distinct POS transactions / Cartwell orders |
| `units` | Sum of quantity sold |
| `gross_sales` | Sum of line amount before discount, including VAT |
| `discount` | Sum of line discount |
| `revenue` | `gross_sales - discount` (i.e. amount paid by the customer, including VAT) |
| `vat` | VAT element of revenue |

**`fact_returns_daily`** — grain: original sale date × store × product category × channel × reason code.

| Column | Definition |
|---|---|
| `original_sale_date` | Date of the original sale |
| `returned_units` | Sum of returned quantity |
| `returned_value` | Sum of refund amount including VAT |

#### 3.3 Power BI measures

| Measure | DAX logic (summary) |
|---|---|
| Revenue | `SUM(fact_sales_daily[revenue])` |
| Average basket value | Revenue / transactions |
| Returns rate | returned_value / gross_sales for the same original sale period |
| Revenue YoY % | Revenue vs same retail period last year |

### 4. Marketing extract layout

File `hp_customers_YYYYMMDD.csv`, comma-separated, UTF-8, header row, one row per active customer (purchase in last 24 months).

| Column | Source |
|---|---|
| customer_id | `silver.customer.customer_id` |
| first_name | `silver.customer.first_name` |
| last_name | `silver.customer.last_name` |
| email | `silver.customer.email` |
| phone | `silver.customer.phone` |
| postcode | `silver.customer.postcode` |
| loyalty_tier | `dim_customer.loyalty_tier` |
| last_purchase_date | max business_date across channels |
| last_purchase_channel | Store / Online |
| spend_12m | Sum of revenue in last 12 months |
| top_category_12m | Category with highest revenue in last 12 months |

### 5. Data quality rules (silver)

| ID | Table | Rule | Severity | Action on failure | Threshold to stop the pipeline | Owner |
|---|---|---|---|---|---|---|
| DQ-01 | sales_line | `store_id` exists in `silver.store` | Error | Quarantine row | > 0.5% of day's rows | Aisha |
| DQ-02 | sales_line | `quantity` <> 0 and between -50 and 500 | Error | Quarantine row | > 0.5% | Aisha |
| DQ-03 | sales_line, online_order_line | `line_amount` >= 0 and < 10,000 | Error | Quarantine row | > 0.5% | Aisha |
| DQ-04 | all facts | business date not in the future and not before 2020-01-01 | Error | Quarantine row | > 0.1% | Marcus |
| DQ-05 | online_order_line | `sku` exists in `silver.product` | Warning | Keep row, product = "Unknown" | > 2% | Marcus |
| DQ-06 | customer | `email` matches basic pattern when present | Warning | Keep row, email set to null | — | Jun |
| DQ-07 | customer | `customer_id` unique | Error | Fail pipeline | any | Jun |
| DQ-08 | return_line | `original_txn_ref` resolves to a sale | Warning | Keep row, original_sale_date = return_date | > 5% | Marcus |
| DQ-09 | return_line | `reason_code` in agreed list (12 codes) | Warning | Map to "Other" | > 3% | Marcus |
| DQ-10 | store, product | Row count within ±10% of previous load | Error | Fail pipeline | any | Aisha |

- Quarantined rows land in `silver._quarantine` with rule ID, table, row payload and run ID.
- The BA reviews quarantine counts weekly with finance; reason codes and thresholds were agreed with the finance controller in week 3.
- Rule results are written to `silver._dq_results` per run and shown on a DQ page in the dev dashboard.

### 6. Open points

- Product category hierarchy for online-only SKUs — waiting on the e-commerce team.
- Retail period calendar file from finance for 2027 onwards.
