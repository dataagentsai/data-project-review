# Stakeholders and RACI — Sales and Returns Insight MVP 1

| | |
|---|---|
| Owner | Sarah Lindqvist (PM) |
| Version | 1.0 |
| Last updated | Week 1 |

### 1. Stakeholder map

| Stakeholder | Role / area | Interest | Influence | What they need from us | Engagement |
|---|---|---|---|---|---|
| Claire Whitlow | Finance Director — **Sponsor** | High | High | Trusted daily revenue view; end to the manual pack | Fortnightly steering; weekly status report |
| Mark Haddad | Financial Controller | High | High | Correct definitions; returns by original sale week | Sprint reviews; definition workshops |
| Finance analysts (2) | Produce the weekly pack today | High | Medium | Time back; numbers they can explain | Sprint reviews; UAT |
| Helen Osei | Head of Store Performance (regional managers report to her) | High | Medium | Store comparisons; adoption by store managers | Monthly update; UAT |
| Regional managers (5) | Oversee 8–9 stores each | Medium | Medium | Region view | Demo at regional meeting; UAT (one rep) |
| Store managers (42) | Run individual stores | Medium | Low | Simple daily view of their store | Guide; go-live comms |
| Leo Grant | E-commerce Manager (owns Cartwell relationship) | Medium | Medium | Minimal effort for his team | Ad hoc; Cartwell file issues |
| Daniel Reyes | Platform Team Lead | Medium | High | Project follows platform standards | Fortnightly check-in with Technical Anchor |
| InfoSec (Nadia Kowalski) | Approves service accounts and firewall changes | Low | High | Correct requests with justification | Via access request process |

### 2. Core team

| Name | Role |
|---|---|
| Sarah Lindqvist | Project Manager (50%) |
| Tom Okafor | Technical Anchor |
| Aisha Bello | Developer (POS ingestion, silver sales) |
| Marcus Chen | Developer (Cartwell ingestion, returns, gold) |
| Jun Park | Developer (customer merge, extract, CI/CD) |
| Priya Raman | Business Analyst |
| Ravi Menon | Tester (part-time, from week 3) |

### 3. RACI — core deliverables

R = Responsible, A = Accountable, C = Consulted, I = Informed

| Deliverable | Sponsor | Fin. Controller | PM | Tech Anchor | Developers | BA | Tester | Platform Team |
|---|---|---|---|---|---|---|---|---|
| Requirements and definitions | A | C | I | C | I | R | C | — |
| Solution architecture | I | — | I | A/R | C | C | I | C |
| Ingestion pipelines | — | — | I | A | R | I | C | C |
| Silver and gold models | — | C | I | A | R | C | C | — |
| Data quality rules | — | C | I | A | R | R | C | — |
| Power BI dashboard | I | C | I | A | R | C | C | — |
| Marketing extract | — | — | I | A | R | C | C | — |
| Test strategy and execution | — | — | I | C | C | C | A/R | — |
| Environments and access | — | — | I | A | C | — | — | R |
| Release to production | I | — | C | A | R | I | C | C |
| Plan, RAID, status | I | — | A/R | C | I | C | I | — |
| UAT sign-off | A/R | C | C | I | I | C | C | — |

### 4. Communication plan

| What | Audience | Frequency | Channel | Owner |
|---|---|---|---|---|
| Status report | Sponsor, Financial Controller, Head of Store Performance, Platform Team Lead, core team | Weekly (Friday) | Email + Teams channel | PM |
| Steering update | Sponsor, PM, Technical Anchor | Fortnightly | 30-min meeting | PM |
| Sprint review / demo | Financial Controller, finance analysts, core team | Every 2 weeks | Teams | BA |
| Definitions workshops | Financial Controller, BA | As needed | Workshop | BA |
| Platform check-in | Platform Team Lead, Technical Anchor | Fortnightly | Meeting | Technical Anchor |
| Go-live announcement | All business users | Once, week 12 | Email from Sponsor | PM |

### 5. Escalation path

Team member → Technical Anchor / PM → Sponsor. Platform or access blockers go to the Platform Team Lead first, then to the Sponsor at steering.
