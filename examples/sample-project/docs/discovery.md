# Discovery Summary — Sales and Returns Insight

| | |
|---|---|
| Author | Tom Okafor (Technical Anchor), with Priya Raman (BA) |
| Discovery period | 3 weeks before project start |
| Status | **Signed off — week 0** (Claire Whitlow, Sponsor) |

### 1. Purpose

Confirm the sources, volumes and behaviour of the data needed for MVP 1, identify constraints, and agree a target approach on the existing Databricks platform.

### 2. Sources

#### 2.1 StoreLink POS (on-prem)

| Item | Finding |
|---|---|
| Technology | SQL Server 2016 Enterprise, HQ data centre (Leeds) |
| Tables of interest | `sales_header`, `sales_line`, `customer`, `return_header`, `return_line`, `store`, `product` |
| Change capture | SQL Server CDC is already enabled on `sales_header`, `sales_line`, `customer` and `return_*` for an older reporting feed. Retention on CDC tables is 3 days. |
| Volumes | ~180,000 sales lines per day across 42 stores; peak ~420,000/day in December. ~6,500 return lines per day. |
| History | 7 years retained in POS. Finance needs **3 years** for year-on-year and trend reporting (approx. 200M sales lines). |
| Customer records | ~1.1M loyalty customers. Around 2% update their address or contact details each month (loyalty app sync). |
| End-of-day process | Runs 23:30. Voided transactions are removed from `sales_line` and `sales_header` by the end-of-day process (physical delete). Price corrections are applied as updates to existing lines. |
| Access | Read access to CDC functions requires an InfoSec-approved service account and a firewall rule from the platform's Azure subnet to the HQ data centre. |

#### 2.2 Cartwell e-commerce (SaaS)

| Item | Finding |
|---|---|
| Delivery | Nightly CSV files pushed by Cartwell to an Azure storage container provided by us: `orders_YYYYMMDD.csv`, `customers_YYYYMMDD.csv`, `returns_YYYYMMDD.csv` |
| Arrival | Normally by 02:00 UK time. Arrived after 06:00 on 9 days in the last quarter (latest 07:30). |
| Content | Orders file is a full extract of the previous day's orders; customers file contains new and changed customers only. |
| Resends | If Cartwell's internal validation fails, they resend the day's files, sometimes the following day, either with the same name or with a `_v2` suffix. This happened 4 times in the last 6 months. |
| Volumes | ~12,000 orders/day (~31,000 lines), up to 60,000 orders/day in Black Friday week |
| Layout changes | Cartwell changed the orders file layout twice in the past 12 months (added two columns; renamed `promo_cd` to `promotion_code`), with about one week's notice by email to the e-commerce team. |
| History | Cartwell can provide a one-off extract of historical orders on request. |

### 3. Returns behaviour

- In-store returns are accepted up to 28 days after purchase (60 days for loyalty members).
- Online returns can be logged up to 60 days after the order is delivered; refunds are processed when the parcel is received at the warehouse.
- Online orders can be returned in store; these appear in POS `return_line` with a Cartwell order reference.
- Finance wants returns attributed to the **original sale date** so that returns rate is measured against the sales it relates to.

### 4. Reporting consumers

- Finance: daily review each morning by 09:00; weekly pack on Monday.
- Store managers: check the previous day's trading at store opening.
- Marketing: Brightwave campaign tool imports a CSV from SFTP.

### 5. Target approach (agreed)

- Land POS changes nightly using the existing SQL Server CDC tables; land Cartwell files using Auto Loader.
- Medallion layers (bronze, silver, gold) in Unity Catalog on the existing platform.
- Orchestrate with Lakeflow Jobs.
- Power BI dashboard on gold, using the existing Power BI Premium capacity.
- Marketing extract written as CSV to the Brightwave SFTP.

### 6. Constraints

- Must use the existing Azure Databricks platform and its standards.
- No direct connection from Power BI to the POS database.
- POS CDC retention of 3 days means extraction must not be down for more than 2 consecutive days.

### 7. Recommendation

Proceed to MVP 1 (12 weeks) with a team of a technical anchor, three developers, a BA, a PM and a part-time tester.

### 8. Sign-off

| Name | Role | Date |
|---|---|---|
| Claire Whitlow | Finance Director, Sponsor | Week 0 |
