# Gap Analysis

## Purpose

This document translates the Step 5 control assessment results into clear current-vs-target gaps for the simulated IT GRC Risk & Control Assessment Case Study.

The goal of this step is to convert assessment findings into actionable remediation input:

```text
Assessment Finding -> Current Condition -> Target Condition -> Gap -> Business Risk -> Remediation Direction
```

This document prepares the project for Step 7: `remediation_plan_poam.csv` and `docs/08_remediation_plan_poam.md`.

---

## Input Artifacts

This gap analysis is based on the following project artifacts:

| Artifact | How It Is Used |
|---|---|
| `data/asset_inventory.csv` | Defines the in-scope systems, owners, sensitivity, and criticality |
| `data/risk_register.csv` | Provides risk statements, likelihood, impact, residual risk, owner, and source reference |
| `data/control_matrix.csv` | Defines expected controls, evidence, frequency, owners, and framework mapping |
| `data/control_assessment_results.csv` | Provides findings, severity, evidence status, and recommendations |

---

## Gap Analysis Method

For this portfolio case study, each control assessment result is translated into a gap using the following structure:

| Field | Meaning |
|---|---|
| Gap ID | Unique identifier for the gap |
| Gap Area | Business/control area affected by the gap |
| Current Condition | Current simulated condition based on the assessment result |
| Target Condition | Expected control condition based on industry-aligned control practices |
| Gap | Difference between current and target condition |
| Business Risk | Potential business, operational, privacy, or compliance impact |
| Priority | High or Medium management priority |
| Remediation Direction | Practical action direction for POA&M planning |

The priority is based on assessment severity, related risk exposure, evidence weakness, and whether the affected area involves sensitive data, privileged access, recovery, change management, or monitoring.

---

## Gap Summary

### Priority Summary

| Priority   |   Count |
|:-----------|--------:|
| High       |       7 |
| Medium     |       8 |

### Theme Summary

| Theme                         | Related Gaps                      | Why It Matters                                                                     |
|:------------------------------|:----------------------------------|:-----------------------------------------------------------------------------------|
| Access and privacy governance | G-001, G-002, G-008, G-014        | Protects sensitive student/personal data and supports privacy accountability.      |
| Detection and monitoring      | G-003, G-013                      | Improves visibility over admin activity and vulnerability exposure.                |
| Resilience and recovery       | G-004, G-011                      | Supports service continuity during outages, data issues, or peak academic periods. |
| Change and workflow control   | G-005, G-012                      | Strengthens audit trail for system changes and service request closure.            |
| Operational governance        | G-006, G-007, G-009, G-010, G-015 | Improves SLA, vendor, awareness, data quality, and evidence readiness practices.   |

---

## High-Priority Gaps

The following gaps should be prioritized first in the Step 7 remediation plan / POA&M.

| gap_id   | gap_area                                    | control_id   | related_risk_id   | current_condition                                                                                                     | target_condition                                                                                                                    | gap                                                                                                      | business_risk                                                                                                              | remediation_direction                                                                                                           |
|:---------|:--------------------------------------------|:-------------|:------------------|:----------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|
| G-001    | Privileged Access Review                    | C-001        | R-001             | Privileged access review is conceptually defined, but quarterly review evidence and formal sign-off are inconsistent. | Quarterly privileged access review is performed, signed off, exceptions are tracked, and removal evidence is retained.              | No consistent formal review evidence, exception log, and management approval trail for privileged users. | Unauthorized or outdated access may remain active and expose sensitive academic records.                                   | Formalize quarterly access review template, reviewer ownership, exception handling, removal evidence, and management approval.  |
| G-002    | Joiner-Mover-Leaver Access Control          | C-002        | R-002; R-010      | Access approval exists for some requests, but role-change and offboarding reconciliation evidence is incomplete.      | All access provisioning, role changes, and terminations are reconciled monthly with documented approval and removal evidence.       | User lifecycle access review is not consistently evidenced across joiner, mover, and leaver events.      | Former users or users with changed roles may retain unnecessary access to personal or sensitive data.                      | Implement monthly joiner-mover-leaver reconciliation with access removal proof and owner sign-off.                              |
| G-003    | Admin Activity Log Review                   | C-003        | R-006             | System logs are assumed to exist, but there is no documented monthly admin activity review or escalation record.      | Admin activity logs are reviewed monthly, exceptions are documented, and unusual activities are escalated to responsible owners.    | Log review procedure, exception criteria, and escalation evidence are missing.                           | Suspicious privileged activity may not be detected or investigated in a timely manner.                                     | Define monthly admin log review procedure, exception criteria, reviewer responsibility, and escalation workflow.                |
| G-004    | Backup Restoration Testing                  | C-004        | R-003             | Backup activity is assumed, but restoration test evidence is not available.                                           | Backup restoration tests are performed quarterly and before peak academic periods with documented result and sign-off.              | No restore test log, result validation, recovery time evidence, issue log, or management sign-off.       | Critical academic services may not recover within expected time during outage, data corruption, or operational disruption. | Perform documented quarterly restore tests covering scope, result, recovery time, issues, remediation, and approval.            |
| G-005    | Change Approval and UAT Evidence            | C-005        | R-004             | Change approval exists for some changes, but UAT evidence, rollback plan, and post-change review are inconsistent.    | Every production change has documented approval, UAT result, rollback plan, release note, and post-implementation review.           | Change documentation is incomplete and not consistently traceable from request to release.               | Unvalidated changes may disrupt registration, admin, or reporting workflows and weaken audit trail.                        | Standardize change request form, approval workflow, UAT sign-off, rollback documentation, and post-change review.               |
| G-008    | Personal Data Retention and Deletion Review | C-008        | R-013             | No formal retention schedule or deletion review evidence is available for student-related personal data.              | Personal data retention rules, deletion review process, owner approval, and evidence records are documented and reviewed.           | No documented personal data lifecycle governance evidence for retention and deletion.                    | Personal data may be retained longer than necessary, increasing privacy and compliance exposure.                           | Define retention schedule, deletion review process, data owner approval, and evidence documentation.                            |
| G-013    | Vulnerability Backlog and Patch Tracking    | C-013        | R-015             | No formal vulnerability backlog or patch tracking evidence is available for in-scope assets.                          | Vulnerabilities are recorded in a backlog with affected asset, severity, owner, due date, remediation status, and closure evidence. | No structured vulnerability backlog, patch tracking, or closure evidence is available.                   | Known vulnerabilities may remain unresolved and expose critical academic systems to avoidable risk.                        | Create vulnerability backlog linked to asset inventory, severity, owner, target date, remediation status, and closure evidence. |

---

## Full Gap Matrix

| gap_id   | gap_area                                    | control_id   | related_risk_id            | priority   | current_condition                                                                                                           | target_condition                                                                                                                          | gap                                                                                                         | business_risk                                                                                                              | remediation_direction                                                                                                                |
|:---------|:--------------------------------------------|:-------------|:---------------------------|:-----------|:----------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
| G-001    | Privileged Access Review                    | C-001        | R-001                      | High       | Privileged access review is conceptually defined, but quarterly review evidence and formal sign-off are inconsistent.       | Quarterly privileged access review is performed, signed off, exceptions are tracked, and removal evidence is retained.                    | No consistent formal review evidence, exception log, and management approval trail for privileged users.    | Unauthorized or outdated access may remain active and expose sensitive academic records.                                   | Formalize quarterly access review template, reviewer ownership, exception handling, removal evidence, and management approval.       |
| G-002    | Joiner-Mover-Leaver Access Control          | C-002        | R-002; R-010               | High       | Access approval exists for some requests, but role-change and offboarding reconciliation evidence is incomplete.            | All access provisioning, role changes, and terminations are reconciled monthly with documented approval and removal evidence.             | User lifecycle access review is not consistently evidenced across joiner, mover, and leaver events.         | Former users or users with changed roles may retain unnecessary access to personal or sensitive data.                      | Implement monthly joiner-mover-leaver reconciliation with access removal proof and owner sign-off.                                   |
| G-003    | Admin Activity Log Review                   | C-003        | R-006                      | High       | System logs are assumed to exist, but there is no documented monthly admin activity review or escalation record.            | Admin activity logs are reviewed monthly, exceptions are documented, and unusual activities are escalated to responsible owners.          | Log review procedure, exception criteria, and escalation evidence are missing.                              | Suspicious privileged activity may not be detected or investigated in a timely manner.                                     | Define monthly admin log review procedure, exception criteria, reviewer responsibility, and escalation workflow.                     |
| G-004    | Backup Restoration Testing                  | C-004        | R-003                      | High       | Backup activity is assumed, but restoration test evidence is not available.                                                 | Backup restoration tests are performed quarterly and before peak academic periods with documented result and sign-off.                    | No restore test log, result validation, recovery time evidence, issue log, or management sign-off.          | Critical academic services may not recover within expected time during outage, data corruption, or operational disruption. | Perform documented quarterly restore tests covering scope, result, recovery time, issues, remediation, and approval.                 |
| G-005    | Change Approval and UAT Evidence            | C-005        | R-004                      | High       | Change approval exists for some changes, but UAT evidence, rollback plan, and post-change review are inconsistent.          | Every production change has documented approval, UAT result, rollback plan, release note, and post-implementation review.                 | Change documentation is incomplete and not consistently traceable from request to release.                  | Unvalidated changes may disrupt registration, admin, or reporting workflows and weaken audit trail.                        | Standardize change request form, approval workflow, UAT sign-off, rollback documentation, and post-change review.                    |
| G-006    | Incident Severity and Escalation            | C-006        | R-005                      | Medium     | Incident tickets are available, but severity classification and escalation evidence are not consistently documented.        | Incidents are classified by severity, assigned SLA targets, escalated when required, and closed with documented review.                   | Severity matrix, escalation SLA, required ticket fields, and post-incident review checklist are incomplete. | Security or service incidents may be handled inconsistently, causing delayed response and unclear accountability.          | Define incident severity matrix, escalation SLA, ticket field requirements, and post-incident review checklist.                      |
| G-007    | Vendor SLA and Escalation Governance        | C-007        | R-007                      | Medium     | Vendor dependency is recognized, but SLA review and escalation testing are not consistently documented.                     | Vendor SLA, support scope, escalation contacts, dependency review notes, and escalation test evidence are maintained.                     | Vendor management evidence is incomplete for service dependency and support escalation monitoring.          | Vendor delays or unclear support responsibilities may extend incident resolution or recovery time.                         | Maintain vendor SLA review records, escalation contacts, support scope, and periodic dependency review notes.                        |
| G-008    | Personal Data Retention and Deletion Review | C-008        | R-013                      | High       | No formal retention schedule or deletion review evidence is available for student-related personal data.                    | Personal data retention rules, deletion review process, owner approval, and evidence records are documented and reviewed.                 | No documented personal data lifecycle governance evidence for retention and deletion.                       | Personal data may be retained longer than necessary, increasing privacy and compliance exposure.                           | Define retention schedule, deletion review process, data owner approval, and evidence documentation.                                 |
| G-009    | Role-Based Security and Privacy Awareness   | C-009        | R-014                      | Medium     | Training may exist informally, but completion records and role-specific privacy/security awareness evidence are incomplete. | Annual awareness training and admin onboarding checklist are completed, tracked, and reviewed for relevant users.                         | No consistent completion tracking or role-specific awareness evidence for users handling sensitive data.    | Users may mishandle personal data or fail to follow security expectations due to weak awareness controls.                  | Create annual training tracker and onboarding checklist for admin users handling sensitive academic data.                            |
| G-010    | Reporting Data Quality Validation           | C-010        | R-008; R-011               | Medium     | Data validation is performed in some cases, but reconciliation evidence and exception tracking are not standardized.        | Reporting data is validated monthly using a documented checklist, reconciliation steps, exception owner, and reviewer sign-off.           | Data quality validation evidence is inconsistent across reporting outputs.                                  | Management decisions may rely on inaccurate or unreconciled academic reporting data.                                       | Standardize reporting validation checklist, reconciliation steps, exception owner, and reviewer sign-off.                            |
| G-011    | Business Continuity Readiness               | C-011        | R-009                      | Medium     | Continuity need is recognized, but walkthrough/testing evidence and fallback ownership are not fully documented.            | Continuity procedures, fallback owners, readiness walkthroughs, and test evidence are documented before peak academic periods.            | Business continuity procedure evidence and fallback ownership are incomplete.                               | Academic services may be disrupted during peak periods if continuity responsibilities are unclear.                         | Document continuity procedures, assign fallback owners, and perform pre-peak readiness walkthroughs.                                 |
| G-012    | Workflow Closure Evidence                   | C-012        | R-012                      | Medium     | Workflow records exist, but closure evidence and sample review results are not consistently linked to each request.         | Each completed request has closure evidence, approval note, reviewer field, and sample review record.                                     | Request closure evidence is not consistently linked to workflow records.                                    | Document request processing may lack audit trail, making service completion difficult to verify.                           | Require closure evidence, approval note, reviewer field, and monthly sample review for fulfillment workflows.                        |
| G-013    | Vulnerability Backlog and Patch Tracking    | C-013        | R-015                      | High       | No formal vulnerability backlog or patch tracking evidence is available for in-scope assets.                                | Vulnerabilities are recorded in a backlog with affected asset, severity, owner, due date, remediation status, and closure evidence.       | No structured vulnerability backlog, patch tracking, or closure evidence is available.                      | Known vulnerabilities may remain unresolved and expose critical academic systems to avoidable risk.                        | Create vulnerability backlog linked to asset inventory, severity, owner, target date, remediation status, and closure evidence.      |
| G-014    | Personal Data Export Review                 | C-014        | R-002; R-013               | Medium     | Personal data export review control is planned but not yet implemented.                                                     | Bulk personal data exports require documented purpose, scope, requester, approver, log review, and retention note.                        | No implemented control for reviewing or approving bulk personal data exports.                               | Sensitive personal data may be exported without sufficient purpose limitation, approval, or review evidence.               | Implement approval and log review for bulk personal data exports, including purpose, scope, requester, approver, and retention note. |
| G-015    | Centralized Control Evidence Repository     | C-015        | R-001; R-004; R-012; R-015 | Medium     | Centralized control evidence repository is planned but not yet implemented.                                                 | Control evidence is stored in a centralized tracker/repository with owner, frequency, review status, and management reporting visibility. | Control evidence is fragmented and not centrally tracked for audit-readiness monitoring.                    | Management and auditors may not be able to verify control performance efficiently during review cycles.                    | Build evidence tracker and repository index to centralize evidence ownership, review status, and management reporting.               |

---

## Key Observations

### 1. Access governance is the highest-risk theme

The strongest gap area is access governance. Privileged access review, joiner-mover-leaver reconciliation, and personal data visibility are only partially evidenced. This creates risk around excessive access, outdated privileges, and unauthorized viewing of sensitive academic records.

### 2. Recovery readiness is not sufficiently evidenced

Backup activity is assumed, but restore test evidence is missing. From a GRC perspective, backup existence alone is not enough. The organization must be able to demonstrate that restoration has been tested and documented.

### 3. Change management requires stronger traceability

Change approvals exist only partially, while UAT evidence, rollback plans, and post-change reviews are inconsistent. This weakens traceability from change request to production release.

### 4. Monitoring controls are underdeveloped

Admin logs are assumed to exist, but monthly log review and exception escalation evidence are unavailable. Vulnerability tracking is also missing. These gaps reduce the organization's ability to detect issues early.

### 5. Evidence readiness is a cross-cutting issue

Many controls are not only weak because the activity is missing, but because evidence is not retained or centrally tracked. This supports the need for Step 8: evidence tracker and centralized evidence repository.

---

## Remediation Planning Input

The following table will be used as the input for Step 7 POA&M creation.

| gap_id   | control_id   | related_risk_id            | priority   | remediation_direction                                                                                                                | evidence_required                                                                                                     |
|:---------|:-------------|:---------------------------|:-----------|:-------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| G-001    | C-001        | R-001                      | High       | Formalize quarterly access review template, reviewer ownership, exception handling, removal evidence, and management approval.       | User-role export, access review worksheet, exception list, removal confirmation, reviewer sign-off                    |
| G-002    | C-002        | R-002; R-010               | High       | Implement monthly joiner-mover-leaver reconciliation with access removal proof and owner sign-off.                                   | Access request form, approval record, active user list, HR role-change list, deactivation evidence                    |
| G-003    | C-003        | R-006                      | High       | Define monthly admin log review procedure, exception criteria, reviewer responsibility, and escalation workflow.                     | Admin activity log extract, log review checklist, exception register, reviewer sign-off, follow-up ticket             |
| G-004    | C-004        | R-003                      | High       | Perform documented quarterly restore tests covering scope, result, recovery time, issues, remediation, and approval.                 | Backup schedule, restore test log, restoration screenshot, recovery result, issue log, management sign-off            |
| G-005    | C-005        | R-004                      | High       | Standardize change request form, approval workflow, UAT sign-off, rollback documentation, and post-change review.                    | Change request form, approval record, UAT result, rollback plan, release note, post-change review                     |
| G-006    | C-006        | R-005                      | Medium     | Define incident severity matrix, escalation SLA, ticket field requirements, and post-incident review checklist.                      | Incident ticket, severity classification, escalation log, communication note, resolution record, post-incident review |
| G-007    | C-007        | R-007                      | Medium     | Maintain vendor SLA review records, escalation contacts, support scope, and periodic dependency review notes.                        | Vendor SLA document, support contact list, escalation matrix, review meeting note, issue resolution record            |
| G-008    | C-008        | R-013                      | High       | Define retention schedule, deletion review process, data owner approval, and evidence documentation.                                 | Data retention schedule, retention review worksheet, deletion approval, exception register, policy review note        |
| G-009    | C-009        | R-014                      | Medium     | Create annual training tracker and onboarding checklist for admin users handling sensitive academic data.                            | Training material, attendance/completion report, quiz result, reminder notice, exception follow-up                    |
| G-010    | C-010        | R-008; R-011               | Medium     | Standardize reporting validation checklist, reconciliation steps, exception owner, and reviewer sign-off.                            | Validation checklist, reconciliation report, exception log, correction record, dashboard refresh note                 |
| G-011    | C-011        | R-009                      | Medium     | Document continuity procedures, assign fallback owners, and perform pre-peak readiness walkthroughs.                                 | Continuity checklist, peak readiness review, support roster, communication plan, test result, issue follow-up         |
| G-012    | C-012        | R-012                      | Medium     | Require closure evidence, approval note, reviewer field, and monthly sample review for fulfillment workflows.                        | Request record, approval note, fulfillment evidence, closure timestamp, sample review sheet                           |
| G-013    | C-013        | R-015                      | High       | Create vulnerability backlog linked to asset inventory, severity, owner, target date, remediation status, and closure evidence.      | Vulnerability backlog, severity rating, owner assignment, remediation ticket, vendor advisory, closure evidence       |
| G-014    | C-014        | R-002; R-013               | Medium     | Implement approval and log review for bulk personal data exports, including purpose, scope, requester, approver, and retention note. | Export request log, approval record, data scope note, monthly export review, exception register                       |
| G-015    | C-015        | R-001; R-004; R-012; R-015 | Medium     | Build evidence tracker and repository index to centralize evidence ownership, review status, and management reporting.               | Evidence tracker, repository index, reviewer notes, missing evidence list, management review summary                  |

---

## Source Alignment

This gap analysis remains aligned with the source-based methodology defined earlier in the project:

| Source / Concept | How It Supports the Gap Analysis |
|---|---|
| NIST CSF 2.0 | Supports governance, identify, protect, detect, respond, and recover themes |
| NIST SP 800-30 | Supports risk-based prioritization using likelihood, impact, and residual risk thinking |
| NIST SP 800-53 | Supports control family mapping such as Access Control, Audit and Accountability, Configuration Management, Contingency Planning, and Incident Response |
| NIST SP 800-53A | Supports evidence-based control assessment and finding translation |
| ISO/IEC 27001 concepts | Supports confidentiality, integrity, availability, and risk-aware information security management |
| CIS Controls | Supports practical safeguard and cyber hygiene remediation direction |
| COBIT governance concepts | Supports accountability, ownership, control monitoring, and management reporting |
| Indonesia PDP Law | Supports privacy-focused gaps related to personal data access, export, retention, and evidence |

---

## Limitations

This gap analysis is based on synthetic data and simulated assessment results.

It does not represent:

- a real company gap assessment,
- a legal compliance conclusion,
- an ISO certification audit,
- a formal COBIT capability assessment,
- or a production evidence review.

The purpose is to demonstrate how a junior IT GRC analyst can translate control assessment results into a structured current-vs-target gap analysis for remediation planning.

---

## Next Step

The next project artifact is:

```text
data/remediation_plan_poam.csv
docs/08_remediation_plan_poam.md
```

The remediation plan / POA&M will convert each important gap into an action with owner, target date, priority, status, evidence requirement, and closure criteria.
