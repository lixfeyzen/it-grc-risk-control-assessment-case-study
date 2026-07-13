# Scope and Asset Inventory

## Purpose

This document defines the assessment scope and the assets included in the simulated IT GRC case study.

In IT GRC work, an asset inventory is important because risk assessment should be connected to what the organization actually uses, owns, operates, or depends on. This project uses an asset-based approach so that later artifacts can clearly connect:

```text
Asset → Risk → Control → Assessment Result → Gap → Remediation → Evidence
```

The asset inventory is synthetic and created for portfolio demonstration purposes. It does not represent a real organization, real campus system, real student record, real employee record, or real production environment.

---

## Assessment Scenario

The simulated organization uses an **Internal Academic Services System** to support student and academic administration processes.

The system includes modules and supporting assets for:

- student profile management,
- course registration,
- payment status visibility,
- academic document requests,
- administrative record management,
- academic database operations,
- management reporting,
- backup and recovery,
- identity and access management,
- change request documentation,
- incident ticketing,
- and vendor support coordination.

This scope was selected because academic services systems commonly involve personal data, privileged access, service availability, change control, incident response, reporting reliability, and recovery readiness.

---

## Scope Boundary

### In Scope

The assessment includes assets that are directly related to the simulated academic services workflow and its IT GRC risks.

| Scope Area | Included Examples | GRC Relevance |
|---|---|---|
| Application modules | Student profile, course registration, payment status, document request | Access control, privacy, availability, workflow control |
| Administrative interfaces | Admin portal and privileged user access | Privileged access, segregation of duties, monitoring |
| Data layer | Academic database and reporting data | Confidentiality, integrity, availability, data quality |
| Recovery assets | Backup storage and recovery dependency | Business continuity, recovery readiness |
| Governance records | Change requests, UAT evidence, incident tickets | Audit trail, control evidence, remediation tracking |
| Third-party dependency | Vendor/SaaS support portal | Vendor risk, SLA, escalation, support dependency |

### Out of Scope

This project does not assess:

- real infrastructure configurations,
- production databases,
- real user accounts,
- real vulnerability scan results,
- penetration testing results,
- financial payment processing systems,
- legal compliance opinion,
- or official certification readiness.

---

## Asset Classification Method

The asset inventory uses two simple assessment dimensions:

### 1. Data Sensitivity

| Rating | Meaning |
|---|---|
| High | Asset processes personal, sensitive, privileged, or security-relevant information |
| Medium | Asset processes internal operational data or limited sensitive information |
| Low | Asset processes general or low-impact operational information |

### 2. Business Criticality

| Rating | Meaning |
|---|---|
| High | Disruption could significantly affect academic operations, service delivery, access, or recovery |
| Medium | Disruption could affect process efficiency or management visibility, but workaround may exist |
| Low | Disruption has limited operational impact or is not critical to core academic services |

These ratings are qualitative and intended for portfolio demonstration. They are used to support later risk prioritization, not to claim a real business impact assessment.

---

## Asset Inventory Summary

The current scope includes **12 assets**.

| Asset ID | Asset Name | Asset Type | Data Sensitivity | Business Criticality | Asset Owner | Main GRC Exposure |
|---|---|---|---|---|---|---|
| A-001 | Student Profile Module | Application Module | High | High | Data Owner / Academic Services | Personal data exposure, access control, data quality |
| A-002 | Course Registration Module | Application Module | Medium | High | System Owner / Academic Operations | Service availability, change risk, operational continuity |
| A-003 | Payment Status Module | Application Module | High | Medium | Finance Data Owner / Academic Services | Sensitive status visibility, integrity, access control |
| A-004 | Document Request Module | Application Module | Medium | Medium | Academic Services Lead | Workflow evidence, request ownership, status tracking |
| A-005 | Admin Portal | Application / Privileged Interface | High | High | IT Manager / System Owner | Privileged access, segregation of duties, monitoring |
| A-006 | Academic Database | Database | High | High | Database Administrator / IT Operations | Data loss, unauthorized access, integrity and availability |
| A-007 | Reporting Dashboard | BI / Reporting | Medium | Medium | Management Reporting Owner | Data quality, report access, management decision risk |
| A-008 | Backup Storage | Infrastructure / Storage | High | High | IT Operations | Recovery failure, restore testing, backup exposure |
| A-009 | Identity and Access Management / User Directory | Identity Service | High | High | IT Admin / IAM Owner | Dormant accounts, excessive privileges, access review gaps |
| A-010 | Change Request Repository | Process Repository | Medium | Medium | System Owner / Change Coordinator | Missing approval, inconsistent UAT evidence, weak audit trail |
| A-011 | Incident Ticketing Log | Service Management Record | Medium | High | Helpdesk Lead / IT Operations | Escalation gaps, incident evidence, severity inconsistency |
| A-012 | Vendor / SaaS Support Portal | Third-Party Service Interface | Medium | Medium | Vendor Manager / IT Manager | Vendor dependency, SLA evidence, third-party access concerns |

The full dataset is available in:

```text
data/asset_inventory.csv
```

---

## Key Observations

### 1. High-sensitivity assets require stronger access control

The **Student Profile Module**, **Payment Status Module**, **Admin Portal**, **Academic Database**, **Backup Storage**, and **Identity and Access Management / User Directory** are classified as high sensitivity.

These assets will be important in the next step because they are likely to generate risks related to:

- unauthorized access,
- excessive privileges,
- personal data exposure,
- insufficient access review,
- and weak administrative activity monitoring.

### 2. High-criticality assets require continuity and recovery controls

The **Course Registration Module**, **Admin Portal**, **Academic Database**, **Backup Storage**, **IAM/User Directory**, and **Incident Ticketing Log** are classified as high business criticality.

These assets support daily academic operations, access, recovery, and incident response. They will influence risks related to:

- service disruption,
- recovery failure,
- delayed incident handling,
- and business continuity gaps.

### 3. Governance records are part of the control environment

The **Change Request Repository** and **Incident Ticketing Log** are not traditional infrastructure assets, but they are important for IT GRC because they hold evidence for:

- change approval,
- UAT documentation,
- incident escalation,
- resolution tracking,
- and audit-readiness.

### 4. Vendor support is included as a third-party dependency

The **Vendor / SaaS Support Portal** is included because many organizations depend on external providers for support, issue escalation, and service continuity.

This asset supports later risk mapping for vendor dependency, SLA review, and third-party support coordination.

---

## Source Alignment

The asset inventory is aligned to the project methodology and public references defined in `docs/02_methodology_and_source_mapping.md`.

| Source Area | How It Supports Asset Inventory |
|---|---|
| NIST CSF 2.0 Identify / Asset Management concepts | Supports defining assets and system dependencies before risk assessment |
| NIST SP 800-30 | Supports asset-based risk framing and risk context definition |
| NIST SP 800-53 | Supports later mapping from assets to control families such as Access Control, Audit and Accountability, Contingency Planning, Configuration Management, and Incident Response |
| ISO/IEC 27001 concepts | Supports sensitivity and criticality thinking through confidentiality, integrity, and availability |
| CIS Controls | Supports practical asset, account, data protection, logging, and recovery safeguard themes |
| COBIT governance concepts | Supports ownership, accountability, and IT governance context |
| Indonesia PDP Law | Supports data privacy relevance for assets processing personal or sensitive data |

---

## How This Asset Inventory Will Be Used Next

The next artifact is the **risk register**.

Each risk will reference one or more assets from this inventory through the `asset_id` field.

Example:

| Example Asset | Example Risk Direction |
|---|---|
| A-005 Admin Portal | Unauthorized admin access due to lack of periodic access review |
| A-006 Academic Database | Data loss or integrity issue due to weak backup and monitoring controls |
| A-010 Change Request Repository | System disruption due to undocumented changes and incomplete UAT evidence |
| A-011 Incident Ticketing Log | Delayed incident response due to missing severity and escalation rules |
| A-012 Vendor / SaaS Support Portal | Service recovery delay due to unclear vendor SLA and escalation evidence |

---

## Step 2 Status

```text
Step 2: Scope and asset inventory completed
```

Completed files:

- `data/asset_inventory.csv`
- `docs/03_scope_and_asset_inventory.md`

Next step:

```text
Step 3: Create risk register
```
