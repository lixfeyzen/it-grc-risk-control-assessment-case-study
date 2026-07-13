# Control Matrix

## Purpose

This document explains the control matrix created for the simulated **IT GRC Risk & Control Assessment Case Study**.

The control matrix maps each risk from the risk register to practical control objectives, control activities, owners, frequency, required evidence, implementation status, and industry reference alignment.

The purpose is to show how a junior IT GRC analyst can translate risk statements into actionable controls and audit-ready evidence expectations.

---

## Important Note

This is a simulated portfolio case study. The control matrix does not represent a real company control environment, official audit result, certification assessment, or legal opinion.

The controls are designed using synthetic data and public reference frameworks to demonstrate IT GRC documentation capability.

---

## Control Matrix Summary

| Metric | Value |
| --- | ---: |
| Total controls | 15 |
| Partial controls | 8 |
| Weak controls | 2 |
| Missing controls | 3 |
| Planned enhancement controls | 2 |
| Mapped risks covered | 15 simulated risks |

---

## Implementation Status Summary

| Implementation Status | Count |
| --- | ---: |
| Partial | 8 |
| Weak | 2 |
| Missing | 3 |
| Planned | 2 |

Interpretation:

- **Partial** means the control concept exists, but process consistency or evidence is incomplete.
- **Weak** means the control exists informally or inconsistently.
- **Missing** means the control is expected but no reliable implementation or evidence is assumed in the synthetic assessment.
- **Planned** means an enhancement control is proposed to strengthen governance, monitoring, or audit-readiness.

---

## Control Type Summary

| Control Type | Count |
| --- | ---: |
| Corrective | 2 |
| Detective | 2 |
| Detective / Preventive | 1 |
| Governance / Detective | 2 |
| Preventive | 4 |
| Preventive / Corrective | 1 |
| Preventive / Detective | 3 |

---

## Control Overview

| Control ID | Control Area | Mapped Risk | Type | Frequency | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C-001 | Access Management | R-001 | Preventive / Detective | Quarterly | IT Manager / System Owner | Partial |
| C-002 | Access Management / User Lifecycle | R-002; R-010 | Preventive | Per access request; Monthly reconciliation | IT Admin / HR Coordinator / Data Owner | Partial |
| C-003 | Logging & Monitoring | R-006 | Detective | Monthly | IT Security / System Administrator | Weak |
| C-004 | Backup & Recovery | R-003 | Corrective | Quarterly; before high-risk academic periods | IT Operations Lead | Missing |
| C-005 | Change Management | R-004 | Preventive | Per change | System Owner / Change Manager | Partial |
| C-006 | Incident Handling | R-005 | Corrective | Per incident; Quarterly process review | Helpdesk Lead / IT Support | Partial |
| C-007 | Vendor / Third-Party Management | R-007 | Detective / Preventive | Semiannual; after major vendor incidents | Vendor Manager / IT Manager | Partial |
| C-008 | Data Retention / Privacy | R-013 | Preventive | Annual; after policy change | Data Owner / Compliance Coordinator | Missing |
| C-009 | Security Awareness | R-014 | Preventive | Annual; onboarding; after major policy update | IT Security / HR Training Coordinator | Weak |
| C-010 | Data Quality / Data Integrity | R-008; R-011 | Detective | Monthly; per reporting cycle | BI / Reporting Owner / Finance Data Owner | Partial |
| C-011 | Business Continuity | R-009 | Preventive / Corrective | Before peak registration period; Annual review | Academic Operations / IT Operations | Partial |
| C-012 | Workflow Evidence / Service Processing | R-012 | Preventive / Detective | Per request; Monthly sample review | Academic Services Lead | Partial |
| C-013 | Vulnerability Management | R-015 | Preventive / Detective | Monthly; after security advisory or vendor notification | IT Security / Vendor Manager | Missing |
| C-014 | Personal Data Export Review | R-002; R-013 | Governance / Detective | Per export; Monthly review | Data Owner / Compliance Coordinator | Planned |
| C-015 | Centralized Control Evidence Repository | R-001; R-004; R-012; R-015 | Governance / Detective | Monthly evidence status update; Quarterly management review | IT GRC Analyst / Control Owners | Planned |

---

## How Controls Were Designed

Each control was designed using the following logic:

1. Start from the risk statement in `risk_register.csv`.
2. Identify the expected control objective that would reduce the risk.
3. Define a practical control activity that could be performed by a business or IT owner.
4. Assign a control type: preventive, detective, corrective, or governance-oriented.
5. Define control frequency and owner.
6. Define evidence required for audit-readiness.
7. Map the control to public industry reference themes.
8. Assign an initial simulated implementation status based on the current-state assumptions.

---

## Source Alignment

| Source | Usage |
| --- | --- |
| NIST CSF 2.0 | High-level Govern, Identify, Protect, Detect, Respond, and Recover mapping |
| NIST SP 800-53 Rev. 5 | Security and privacy control families such as AC, AU, CP, CM, IR, RA, SI, SR, and PT |
| NIST SP 800-53A Rev. 5 | Control assessment and evidence logic that will be used in Step 5 |
| ISO/IEC 27001 concepts | Confidentiality, integrity, availability, ISMS-style risk and control themes |
| CIS Controls v8.1 | Practical cyber hygiene safeguards such as account management, log management, recovery, awareness, and vulnerability management |
| COBIT governance concepts | Governance, accountability, control ownership, service/change/vendor management framing |
| Indonesia PDP Law | Personal data protection context for access, privacy, retention, and data exposure risks |

---

## Evidence Logic

Every control includes evidence requirements because IT GRC work must be supported by proof, not only by policy statements.

Examples of evidence used in the matrix include:

- user access review worksheet,
- role approval record,
- admin activity log review,
- backup restore test log,
- change request ticket,
- UAT sign-off,
- incident escalation log,
- vendor SLA review sheet,
- data retention review log,
- vulnerability backlog,
- remediation ticket,
- and management sign-off.

These evidence requirements will feed into the later **Control Assessment Results** and **Evidence Tracker** deliverables.

---

## Control-to-Risk Coverage

The control matrix covers all 15 risks in `risk_register.csv`.

Some controls map to more than one risk because one control can reduce several related risks:

| Control ID | Mapped Risks | Reason |
|---|---|---|
| C-002 | R-002; R-010 | Role-based access and user lifecycle management support both data privacy and account lifecycle risk. |
| C-010 | R-008; R-011 | Data quality validation supports both reporting reliability and data integrity. |
| C-014 | R-002; R-013 | Personal data export review supports privacy exposure and data retention risk. |
| C-015 | R-001; R-004; R-012; R-015 | Centralized evidence monitoring improves audit-readiness across access, change, workflow, and vulnerability controls. |

---

## Relationship to Previous Deliverables

| Previous Deliverable | How It Connects to Control Matrix |
|---|---|
| `asset_inventory.csv` | Defines the assets that controls protect, monitor, or govern. |
| `risk_register.csv` | Provides the risks that controls are mapped to. |
| `control_matrix.csv` | Converts risks into control objectives, activities, evidence, owners, and source mapping. |

---

## Relationship to Next Deliverable

The next step is `control_assessment_results.csv` and `docs/06_control_assessment_results.md`.

That step will assess each control using a more audit-style structure:

- design effectiveness,
- implementation status,
- operating effectiveness,
- evidence status,
- finding,
- severity,
- recommendation.

---

## Limitations

- The controls are not official NIST, ISO, CIS, COBIT, or PDP compliance statements.
- Framework references are used as alignment themes, not as a formal certification mapping.
- Control status is simulated and should not be interpreted as a real organization's maturity or audit result.
- Step 5 is required before drawing conclusions about control design, implementation, and evidence readiness.
