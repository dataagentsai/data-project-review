# Harbor & Pine — Sales and Returns Insight (MVP 1)
## Business Requirements

| | |
|---|---|
| Document owner | Priya Raman (Business Analyst) |
| Version | 1.2 |
| Status | Approved |
| Approved by | Claire Whitlow, Finance Director (Sponsor) — week 0 |

### 1. Background

Harbor & Pine runs 42 stores and an e-commerce site. Today, finance builds the weekly sales and returns pack by hand from two separate exports: one from the StoreLink POS system and one from the Cartwell e-commerce platform. The pack takes two analysts most of Monday and Tuesday, and store managers only see their numbers once a week, usually with errors that are corrected the following week.

This project will bring store and online sales, customers and returns together on the existing Databricks platform and give finance and store managers a single, trusted daily view.

### 2. Business objectives

| # | Objective | Measure |
|---|---|---|
| O1 | Remove the manual weekly pack | Analyst effort on the pack reduced from ~3 days to under half a day |
| O2 | Give store managers timely sight of their sales and returns | Store managers use the dashboard at least 3 times a week (Power BI usage stats) |
| O3 | One version of revenue across store and online | Finance stops reconciling two exports by hand |
| O4 | Feed marketing with customer purchase data | Marketing tool receives a customer extract every day |

### 3. Users

- **Finance analysts and controllers** — daily and weekly sales, returns and revenue by channel, store, region and product category.
- **Store managers (42)** — their own store's sales, returns and top returned products.
- **Regional managers (5)** — stores in their region compared side by side.
- **Marketing** — receives a customer extract for campaign targeting.

### 4. Functional requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Ingest sales, customers and returns from StoreLink POS | Must |
| FR-02 | Ingest orders, customers and returns from the Cartwell nightly files | Must |
| FR-03 | Combine store and online sales into one view with a channel attribute | Must |
| FR-04 | Show revenue, units, average basket value and returns rate by day, week, month, store, region, channel and product category | Must |
| FR-05 | Show returns by reason code and by original sale week | Must |
| FR-06 | Show sales by customer home region, with trend over the last 12 months | Should |
| FR-07 | Year-on-year comparison for all measures | Must |
| FR-08 | Store managers see only their own store; regional managers see their region; finance sees all | Must |
| FR-09 | Produce a daily customer extract (CSV) for the marketing tool, including contact details and last purchase information | Must |
| FR-10 | Load all historical data so trends and year-on-year comparisons work from day one | Must |
| FR-11 | Top 20 returned products per store per week | Should |

### 5. Business definitions

| Term | Definition |
|---|---|
| Revenue | Net sales: value of goods sold after line discounts and after returns, **excluding VAT**. This is the figure finance reports to the board. |
| Units | Number of items sold, net of returned items |
| Average basket value | Revenue divided by number of transactions (store) or orders (online) |
| Returns rate | Returned value divided by gross sales value for the same period of original sale |
| Channel | "Store" for POS transactions, "Online" for Cartwell orders. Click-and-collect counts as Online. |
| Region | Store's trading region for store metrics; customer's home region (from address) for customer metrics |

### 6. Non-functional requirements

| ID | Requirement |
|---|---|
| NFR-01 | Dashboard data should be near real-time so store managers can act on the day's trading |
| NFR-02 | Dashboard pages load in under 5 seconds |
| NFR-03 | Data must be accurate and consistent with the finance ledger |
| NFR-04 | Solution must follow Harbor & Pine data platform standards (Unity Catalog, Power BI workspace standards) |
| NFR-05 | Dashboard available during store trading hours (08:00–21:00) |

### 7. In scope

- StoreLink POS: sales header and lines, customers, returns
- Cartwell: orders, customers, returns files
- Silver and gold layers on the existing Databricks platform
- One Power BI dashboard (3–4 pages) for finance, regional and store managers
- One daily CSV customer extract for the marketing tool
- Row-level security in Power BI as per FR-08

### 8. Assumptions

- The existing Databricks platform, Power BI tenant and Unity Catalog setup are available and maintained by the platform team.
- Product and store reference data is available from the POS database.
- Users have Power BI Pro licences already.

### 9. Approval

Approved by the Sponsor on behalf of the business at the end of week 0.
