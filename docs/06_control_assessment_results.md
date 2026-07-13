# Control Assessment Results

## Purpose

This document records the simulated control assessment results for the IT GRC Risk & Control Assessment Case Study.

The purpose is to move beyond a control list and show how each control can be assessed using an audit-style structure:

```text
Control -> Test Procedure -> Design Effectiveness -> Implementation Status -> Operating Effectiveness -> Evidence Status -> Finding -> Recommendation
```

This document is based on the control matrix created in Step 4 and prepares the project for the next steps:

- gap analysis,
- remediation plan / POA&M,
- evidence tracker,
- and management summary.

---

## Assessment Scope

The assessment covers all 15 controls defined in `data/control_matrix.csv`.

The controls are mapped to the simulated Internal Academic Services System and cover:

- access management,
- user lifecycle,
- logging and monitoring,
- backup and recovery,
- change management,
- incident handling,
- vendor management,
- data retention and privacy,
- security awareness,
- data quality,
- business continuity,
- workflow evidence,
- vulnerability management,
- personal data export review,
- and centralized evidence management.

---

## Methodology

The assessment approach is inspired by NIST SP 800-53A control assessment concepts.

For this portfolio project, each control is assessed using the following simplified dimensions:

| Dimension | Meaning |
|---|---|
| Design Effectiveness | Whether the control design is suitable to address the related risk |
| Implementation Status | Whether the control is implemented, partially implemented, weak, missing, or planned |
| Operating Effectiveness | Whether the control appears to operate effectively based on simulated evidence status |
| Evidence Status | Whether required evidence is available, partial, or unavailable |
| Finding | The control weakness or observation identified |
| Severity | High or Medium priority based on potential risk exposure and evidence weakness |
| Recommendation | Practical improvement action for remediation planning |

This is not a formal audit or certification assessment. It is a simulated portfolio artifact intended to demonstrate IT GRC control assessment thinking.

---

## Assessment Result Summary

### Design Effectiveness

| Design Effectiveness   |   Count |
|:-----------------------|--------:|
| Adequate               |       9 |
| Needs Improvement      |       4 |
| Planned                |       2 |

### Implementation Status

| Implementation Status   |   Count |
|:------------------------|--------:|
| Partial                 |       8 |
| Missing                 |       3 |
| Weak                    |       2 |
| Planned                 |       2 |

### Operating Effectiveness

| Operating Effectiveness   |   Count |
|:--------------------------|--------:|
| Partially Effective       |       8 |
| Not Tested                |       5 |
| Not Effective             |       2 |

### Evidence Status

| Evidence Status   |   Count |
|:------------------|--------:|
| Partial           |       9 |
| Not Available     |       6 |

### Finding Severity

| Severity   |   Count |
|:-----------|--------:|
| Medium     |       8 |
| High       |       7 |

### Assessment Result Type

| Assessment Result       |   Count |
|:------------------------|--------:|
| Finding Raised          |       7 |
| Observation Raised      |       6 |
| Enhancement Recommended |       2 |

---

## Key Assessment Findings

The assessment identified 7 high-severity findings and 8 medium-severity observations or enhancement items.

High-severity findings are concentrated in these areas:

1. **Access governance**

   Quarterly privileged access review and lifecycle reconciliation are not consistently evidenced.

2. **Logging and monitoring**

   Admin activity logs are assumed to exist, but there is no documented periodic review.

3. **Backup and recovery**

   Backup activity is assumed, but restore testing evidence is not available.

4. **Change management**

   Change approval exists partially, but UAT and rollback documentation are inconsistent.

5. **Data retention and privacy**

   No formal retention schedule or deletion review evidence is available for personal data.

6. **Vulnerability management**

   No formal vulnerability backlog or patch tracking evidence is available.

---

## High-Severity Findings

| assessment_id   | control_id   | finding                                                                                                                          | recommendation                                                                                                                                |
|:----------------|:-------------|:---------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------|
| A-001           | C-001        | User access review is defined conceptually, but there is no consistent quarterly sign-off record for privileged access review.   | Formalize quarterly user access review with reviewer sign-off, exception tracking, removal evidence, and management approval.                 |
| A-002           | C-002        | Access approval evidence exists for some requests, but lifecycle reconciliation and removal evidence are incomplete.             | Implement a monthly joiner-mover-leaver reconciliation and require access removal evidence for role changes and terminations.                 |
| A-003           | C-003        | System logs are assumed to exist, but there is no documented monthly admin activity log review or exception escalation evidence. | Define a monthly admin log review procedure, exception criteria, reviewer responsibility, and escalation workflow.                            |
| A-004           | C-004        | Backup activity is assumed, but there is no documented restoration test evidence to confirm recovery readiness.                  | Perform quarterly backup restoration testing and document test scope, result, issues, remediation, and sign-off.                              |
| A-005           | C-005        | Change approval exists for some changes, but UAT evidence and rollback documentation are inconsistent.                           | Standardize change request documentation, UAT sign-off, rollback plan, and post-implementation review before production release.              |
| A-008           | C-008        | No formal retention schedule or deletion review evidence is available for student-related personal data.                         | Define data retention rules, deletion review process, data owner approval, and evidence documentation for personal data lifecycle governance. |
| A-013           | C-013        | No formal vulnerability backlog or patch tracking evidence is available for in-scope assets.                                     | Create a vulnerability backlog linked to asset inventory, severity, owner, due date, remediation status, and closure evidence.                |

---

## Medium-Severity Observations and Enhancements

| assessment_id   | control_id   | finding                                                                                                                         | recommendation                                                                                                                       |
|:----------------|:-------------|:--------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------|
| A-006           | C-006        | Incident tickets are available, but severity classification and escalation evidence are not consistently documented.            | Define an incident severity matrix, escalation SLA, required ticket fields, and post-incident review checklist.                      |
| A-007           | C-007        | Vendor dependency is recognized, but SLA review and escalation testing are not consistently documented.                         | Maintain vendor SLA review records, escalation contacts, support scope, and periodic dependency review notes.                        |
| A-009           | C-009        | Training may exist informally, but completion records and role-specific privacy/security awareness evidence are incomplete.     | Create annual awareness training completion tracking and onboarding awareness checklist for admin users handling sensitive data.     |
| A-010           | C-010        | Data validation is performed in some cases, but reconciliation evidence and exception resolution tracking are not standardized. | Standardize monthly reporting validation checklist, reconciliation steps, exception owner, and reviewer sign-off.                    |
| A-011           | C-011        | Continuity need is recognized, but walkthrough/testing evidence and fallback ownership are not fully documented.                | Document continuity procedures, perform pre-peak readiness walkthrough, and assign fallback owners for critical academic services.   |
| A-012           | C-012        | Workflow records exist, but closure evidence and sample review results are not consistently linked to each request.             | Require closure evidence, approval note, reviewer field, and monthly sample review for document request fulfillment.                 |
| A-014           | C-014        | Personal data export review control is planned but not yet implemented in the simulated control environment.                    | Implement approval and log review for bulk personal data exports, including purpose, scope, requester, approver, and retention note. |
| A-015           | C-015        | Centralized control evidence repository is planned but not yet implemented.                                                     | Build an evidence tracker and repository index to centralize evidence ownership, review status, and management reporting.            |

---

## Assessment Rating Logic

The assessment rating uses the following simplified logic:

| Condition | Result |
|---|---|
| Control is designed and implemented with clear evidence | No finding or low concern |
| Control exists but evidence is partial or inconsistent | Observation or finding |
| Control is weak, missing, or not evidenced | Finding raised |
| Control is planned but not implemented | Enhancement recommended |
| Control affects sensitive data, privileged access, recovery, or change management | Higher severity consideration |

For this case study, severity is not a legal or regulatory conclusion. It is a management prioritization indicator.

---

## Relationship to Control Matrix

The control assessment results are directly linked to the Step 4 control matrix:

| Artifact | Relationship |
|---|---|
| `control_matrix.csv` | Defines the expected controls, owners, evidence, and source mapping |
| `control_assessment_results.csv` | Evaluates whether each control is designed, implemented, operating, and evidenced |
| `07_gap_analysis.md` | Will translate assessment weaknesses into current-vs-target gaps |
| `remediation_plan_poam.csv` | Will convert findings into owner-based remediation actions |
| `evidence_tracker.csv` | Will track whether required evidence exists and has been reviewed |

---

## Source Alignment

The assessment structure is aligned with public IT GRC and control assessment references:

| Source | How It Supports This Step |
|---|---|
| NIST SP 800-53A | Provides control assessment mindset, assessment procedures, and evidence-based evaluation concepts |
| NIST SP 800-53 | Provides security and privacy control families used in the control matrix |
| NIST CSF 2.0 | Provides governance, identify, protect, detect, respond, and recover alignment |
| ISO/IEC 27001 concepts | Supports information security risk and evidence-based control thinking |
| CIS Controls | Supports practical safeguard and control implementation thinking |
| COBIT governance concepts | Supports governance, accountability, control monitoring, and management reporting |
| Indonesia PDP Law | Supports privacy-focused risks and evidence requirements for personal data governance |

---

## Limitations

This assessment uses synthetic data and simulated evidence assumptions.

It does not represent:

- a real company assessment,
- a real audit engagement,
- an ISO certification audit,
- a COBIT assessment,
- a legal compliance opinion,
- or production evidence review.

The purpose is to demonstrate structured junior IT GRC work artifacts that can be reviewed in a portfolio context.

---

## Next Step

The next project artifact is:

```text
docs/07_gap_analysis.md
```

The gap analysis will convert control assessment findings into clear current condition, target condition, gap, business risk, priority, and remediation direction.
