# Platform and Environments — Sales and Returns Insight

| | |
|---|---|
| Author | Tom Okafor (Technical Anchor), reviewed by Daniel Reyes (Platform Team Lead) |
| Version | 1.0 |
| Last updated | Week 2 |

### 1. Existing platform

The project runs on the Harbor & Pine data platform, which is owned and operated by the Platform Team. The platform provides:

- Azure Databricks (Premium), one workspace per environment, Unity Catalog enabled with a single metastore (UK South)
- ADLS Gen2 storage accounts per environment, registered as Unity Catalog external locations
- Azure DevOps for repos and pipelines
- Power BI Premium capacity, with workspaces per environment
- Entra ID groups for access, managed via the platform's access request process

The project does not create new workspaces, storage accounts or networks. It creates schemas, volumes, jobs and Power BI artefacts inside the existing environments.

### 2. Environments

| Environment | Databricks workspace | UC catalog | Power BI workspace | Purpose | Data |
|---|---|---|---|---|---|
| Dev | `hp-dbx-dev` | `hp_dev` | HP Sales Insight [Dev] | Development and unit testing | Synthetic + masked sample |
| Test | `hp-dbx-test` | `hp_test` | HP Sales Insight [Test] | System integration, performance and UAT | Copy of production-shaped data from source test systems |
| Prod | `hp-dbx-prod` | `hp_prod` | HP Sales Insight | Live reporting | Production |

Each catalog contains the schemas `bronze`, `silver`, `gold` and a volume `landing` for Cartwell files. Schema names are the same in every environment; only the catalog changes, set by the bundle target.

### 3. Source connectivity per environment

| Source | Dev | Test | Prod |
|---|---|---|---|
| StoreLink POS | POS test instance (`STLK-TST01`) | POS test instance (`STLK-TST01`) | POS production (`STLK-PRD01`) |
| Cartwell | Sample files placed manually | Cartwell staging tenant pushes to `hp_test` landing | Cartwell production pushes to `hp_prod` landing |
| Brightwave SFTP | Not connected | Brightwave sandbox folder | Brightwave production folder |

### 4. Access model

| Group / principal | Dev | Test | Prod |
|---|---|---|---|
| `grp-hp-sales-dev` (project developers) | Owner of project schemas | Read + run jobs | Read on gold only |
| `grp-hp-sales-test` (tester, BA) | Read | Read + run jobs | Read on gold |
| `grp-finance-analysts` | — | Read on gold (UAT) | Read on gold |
| `sp-hp-sales-<env>` (service principal) | Runs jobs | Runs jobs | Runs jobs; owner of project schemas |
| Platform Team | Admin | Admin | Admin |

- Production jobs run only as the production service principal. Developers cannot run or edit production jobs.
- Changes to production reach the workspace only through the release pipeline (see `deployment-plan.md`).
- Power BI row-level security handles store and region filtering for business users; Unity Catalog grants handle table access.

### 5. Compute

| Workload | Compute |
|---|---|
| Development | Shared all-purpose cluster per developer group, auto-terminate 30 min |
| Scheduled jobs | Job clusters defined in the bundle (Standard_D8ds_v5, 2–6 workers, autoscale) |
| Silver pipeline | Lakeflow Declarative Pipeline, serverless |
| Power BI refresh | Databricks SQL warehouse `hp-sales-sql` (Small, serverless) |

### 6. Network

- Workspaces are VNet-injected; outbound traffic to the HQ data centre goes through the platform hub firewall.
- A firewall rule from the prod and test workspace subnets to the POS database port (1433) is required. Request raised in week 1 (see RAID D-02).
- Cartwell pushes files using a SAS token scoped to the landing container, rotated by the Platform Team every 90 days.
- SFTP to Brightwave goes out through the hub firewall to a fixed IP allow-listed by Brightwave.

### 7. Responsibilities

| Area | Platform Team | Project team |
|---|---|---|
| Workspaces, metastore, storage, network | Owns | Requests |
| Entra groups and membership | Owns | Requests |
| Project schemas, jobs, pipelines | Advises | Owns |
| Release pipeline template | Owns | Uses and configures |
| Power BI capacity | Owns | Uses |
