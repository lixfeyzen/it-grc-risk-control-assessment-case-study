# Remediation Plan / POA&M

## Purpose

This document translates the Step 6 gap analysis into a practical remediation tracker / Plan of Action and Milestones (POA&M) for the simulated IT GRC Risk & Control Assessment Case Study.

The goal is to show how assessment findings become trackable management actions:

```text
Gap -> Related Risk -> Related Control -> Remediation Action -> Owner -> Target Date -> Evidence -> Closure Criteria
```

This step prepares the project for Step 8: `evidence_tracker.csv` and `docs/09_evidence_tracker.md`.

---

## Input Artifacts

The remediation plan is based on the following artifacts:

| Artifact | How It Is Used |
|---|---|
| `data/risk_register.csv` | Provides related risk ID, risk owner, residual risk, priority, and risk response |
| `data/control_matrix.csv` | Provides expected control activity, owner, evidence requirement, and source mapping |
| `data/control_assessment_results.csv` | Provides finding, severity, recommendation, and evidence status |
| `docs/07_gap_analysis.md` | Provides current-vs-target gap and remediation direction |

---

## POA&M Method

Each POA&M item includes the following fields:

| Field | Meaning |
|---|---|
| POA&M ID | Unique remediation action ID |
| Related Gap ID | Gap from Step 6 that triggered the action |
| Related Risk ID | Risk register item affected by the gap |
| Related Control ID | Control that needs remediation or enhancement |
| Finding | Assessment finding or observation from Step 5 |
| Remediation Action | Action required to reduce the gap |
| Owner | Role accountable for action completion |
| Priority | High or Medium |
| Target Date | Simulated management target date |
| Status | Open, In Progress, or Planned |
| Evidence Required | Evidence needed to support closure |
| Closure Criteria | What must be true before the action can be closed |

This is a simulated remediation plan. It does not represent real audit remediation or legal compliance status.

---

## Remediation Summary

### Priority Summary

| Priority   |   Count |
|:-----------|--------:|
| Medium     |       8 |
| High       |       7 |

### Status Summary

| Status      |   Count |
|:------------|--------:|
| Planned     |       6 |
| Open        |       5 |
| In Progress |       4 |

### Owner Summary

| owner                                     |   Open_POAM_Items |
|:------------------------------------------|------------------:|
| Data Owner / Compliance Coordinator       |                 2 |
| Academic Operations / IT Operations       |                 1 |
| Academic Services Lead                    |                 1 |
| BI / Reporting Owner / Finance Data Owner |                 1 |
| Helpdesk Lead / IT Support                |                 1 |
| IT Admin / HR Coordinator / Data Owner    |                 1 |
| IT GRC Analyst / Control Owners           |                 1 |
| IT Manager / System Owner                 |                 1 |
| IT Operations Lead                        |                 1 |
| IT Security / HR Training Coordinator     |                 1 |
| IT Security / System Administrator        |                 1 |
| IT Security / Vendor Manager              |                 1 |
| System Owner / Change Manager             |                 1 |
| Vendor Manager / IT Manager               |                 1 |

---

## POA&M Tracker Overview

| poam_id   | related_gap_id   | related_control_id   | priority   | target_date   | status      | owner                                     | control_area                            |
|:----------|:-----------------|:---------------------|:-----------|:--------------|:------------|:------------------------------------------|:----------------------------------------|
| P-001     | G-001            | C-001                | High       | 2026-07-31    | Open        | IT Manager / System Owner                 | Access Management                       |
| P-002     | G-002            | C-002                | High       | 2026-08-07    | Open        | IT Admin / HR Coordinator / Data Owner    | Access Management / User Lifecycle      |
| P-003     | G-003            | C-003                | High       | 2026-08-14    | Open        | IT Security / System Administrator        | Logging & Monitoring                    |
| P-004     | G-004            | C-004                | High       | 2026-08-21    | In Progress | IT Operations Lead                        | Backup & Recovery                       |
| P-005     | G-005            | C-005                | High       | 2026-08-28    | In Progress | System Owner / Change Manager             | Change Management                       |
| P-006     | G-006            | C-006                | Medium     | 2026-09-11    | Planned     | Helpdesk Lead / IT Support                | Incident Handling                       |
| P-007     | G-007            | C-007                | Medium     | 2026-09-18    | Planned     | Vendor Manager / IT Manager               | Vendor / Third-Party Management         |
| P-008     | G-008            | C-008                | High       | 2026-08-21    | Open        | Data Owner / Compliance Coordinator       | Data Retention / Privacy                |
| P-009     | G-009            | C-009                | Medium     | 2026-09-25    | Planned     | IT Security / HR Training Coordinator     | Security Awareness                      |
| P-010     | G-010            | C-010                | Medium     | 2026-09-25    | In Progress | BI / Reporting Owner / Finance Data Owner | Data Quality / Data Integrity           |
| P-011     | G-011            | C-011                | Medium     | 2026-10-09    | Planned     | Academic Operations / IT Operations       | Business Continuity                     |
| P-012     | G-012            | C-012                | Medium     | 2026-10-02    | Planned     | Academic Services Lead                    | Workflow Evidence / Service Processing  |
| P-013     | G-013            | C-013                | High       | 2026-08-28    | Open        | IT Security / Vendor Manager              | Vulnerability Management                |
| P-014     | G-014            | C-014                | Medium     | 2026-10-16    | Planned     | Data Owner / Compliance Coordinator       | Personal Data Export Review             |
| P-015     | G-015            | C-015                | Medium     | 2026-09-18    | In Progress | IT GRC Analyst / Control Owners           | Centralized Control Evidence Repository |

---

## High-Priority POA&M Items

The following high-priority actions should be addressed first because they relate to privileged access, personal data protection, logging, backup recovery, change management, data retention, or vulnerability tracking.

| poam_id   | related_control_id   | related_risk_id   | control_area                       | owner                                  | target_date   | status      | remediation_action                                                                                                                            |
|:----------|:---------------------|:------------------|:-----------------------------------|:---------------------------------------|:--------------|:------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| P-001     | C-001                | R-001             | Access Management                  | IT Manager / System Owner              | 2026-07-31    | Open        | Formalize quarterly user access review with reviewer sign-off, exception tracking, removal evidence, and management approval.                 |
| P-002     | C-002                | R-002; R-010      | Access Management / User Lifecycle | IT Admin / HR Coordinator / Data Owner | 2026-08-07    | Open        | Implement a monthly joiner-mover-leaver reconciliation and require access removal evidence for role changes and terminations.                 |
| P-003     | C-003                | R-006             | Logging & Monitoring               | IT Security / System Administrator     | 2026-08-14    | Open        | Define a monthly admin log review procedure, exception criteria, reviewer responsibility, and escalation workflow.                            |
| P-004     | C-004                | R-003             | Backup & Recovery                  | IT Operations Lead                     | 2026-08-21    | In Progress | Perform quarterly backup restoration testing and document test scope, result, issues, remediation, and sign-off.                              |
| P-005     | C-005                | R-004             | Change Management                  | System Owner / Change Manager          | 2026-08-28    | In Progress | Standardize change request documentation, UAT sign-off, rollback plan, and post-implementation review before production release.              |
| P-008     | C-008                | R-013             | Data Retention / Privacy           | Data Owner / Compliance Coordinator    | 2026-08-21    | Open        | Define data retention rules, deletion review process, data owner approval, and evidence documentation for personal data lifecycle governance. |
| P-013     | C-013                | R-015             | Vulnerability Management           | IT Security / Vendor Manager           | 2026-08-28    | Open        | Create a vulnerability backlog linked to asset inventory, severity, owner, due date, remediation status, and closure evidence.                |

---

## Closure Logic

A POA&M item should not be closed only because an action was discussed or assigned.

Closure requires evidence. For this project, each POA&M item should meet the following closure logic:

1. The remediation action is completed by the assigned owner.
2. Required evidence is created and stored.
3. Evidence is reviewed by the relevant reviewer or management role.
4. The related control matrix entry is updated if the implementation status changes.
5. The related control assessment result can be re-tested in a future assessment cycle.

---

## Key Remediation Themes

| Theme | Related POA&M Items | Management Interpretation |
|---|---|---|
| Access and privacy governance | P-001, P-002, P-008, P-014 | Sensitive data access and personal data handling require stronger review evidence and ownership. |
| Detection and monitoring | P-003, P-013 | Admin activity and vulnerability exposure need defined monitoring and tracking procedures. |
| Resilience and recovery | P-004, P-011 | Backup restoration and continuity walkthrough evidence are needed to support service recovery confidence. |
| Change and workflow control | P-005, P-012 | Changes and service workflow closure need stronger UAT, approval, and closure evidence. |
| Operational governance | P-006, P-007, P-009, P-010, P-015 | Incident handling, vendor SLA, training, reporting validation, and evidence repository practices need standardization. |

---

## Source Alignment

This remediation plan is source-aligned, not arbitrary.

| Reference | How It Supports the POA&M |
|---|---|
| NIST CSF 2.0 | Supports governance, protection, detection, response, and recovery action planning |
| NIST SP 800-30 Rev. 1 | Supports risk-based prioritization and treatment planning |
| NIST SP 800-53 Rev. 5 | Supports control-family mapping and expected control evidence |
| NIST SP 800-53A Rev. 5 | Supports assessment-to-finding-to-remediation workflow |
| ISO/IEC 27001 concepts | Supports risk treatment, evidence, and management review thinking |
| CIS Controls v8.1 | Supports practical safeguards for access, logs, recovery, vulnerability, and awareness controls |
| COBIT governance concepts | Supports accountability, control ownership, management monitoring, and improvement planning |
| Indonesia PDP Law | Supports personal data protection relevance for access, retention, and export controls |

---

## Limitations

This POA&M is a portfolio artifact using synthetic data. It does not prove real control effectiveness and should not be interpreted as an official audit remediation plan.

The target dates, owners, findings, and evidence requirements are simulated to demonstrate junior IT GRC documentation capability.

---

## Completion Status

The evidence-tracking step has been completed in:

```text
data/evidence_tracker.csv
docs/09_evidence_tracker.md
```

The tracker converts every evidence requirement into an audit-ready inventory with owner, frequency, availability, repository status, reviewer, and review status. Because this is a synthetic case study, unavailable evidence is labelled explicitly instead of being fabricated.
