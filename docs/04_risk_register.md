# Risk Register

## Purpose

This document explains the simulated IT risk register for the **Internal Academic Services System**.

The risk register connects in-scope assets to risk statements, threat events, vulnerabilities, business impact, likelihood-impact scoring, existing control references, residual risk, ownership, risk response, priority, and source references.

The detailed dataset is available in:

```text
data/risk_register.csv
```

---

## Methodology

This risk register uses a simplified portfolio-friendly risk assessment method inspired by **NIST SP 800-30 Rev. 1** and aligned with the broader governance and control references listed in the project methodology.

The assessment logic is:

```text
Likelihood Score x Impact Score = Inherent Risk Score
Residual Risk Score = Risk remaining after considering existing control effectiveness
```

This is a simulated assessment and does not represent a real audit, certification, or production risk assessment.

---

## Scoring Scale

### Likelihood

| Score | Meaning |
|---:|---|
| 1 | Rare |
| 2 | Unlikely |
| 3 | Possible |
| 4 | Likely |
| 5 | Almost certain |

### Impact

| Score | Meaning |
|---:|---|
| 1 | Very low business impact |
| 2 | Low business impact |
| 3 | Moderate business impact |
| 4 | High business impact |
| 5 | Severe business, privacy, compliance, or continuity impact |

### Priority Rule

| Priority | Typical Interpretation |
|---|---|
| High | Requires management attention and remediation planning |
| Medium | Requires monitoring, ownership, and planned improvement |
| Low | Acceptable for monitoring if controls are adequate |

---

## Risk Register Summary

### Priority Distribution

| Priority | Count |
| --- | --- |
| High | 8 |
| Medium | 7 |

### Control Effectiveness Distribution

| Control Effectiveness | Count |
| --- | --- |
| Missing | 2 |
| Partial | 8 |
| Weak | 5 |

### Risk Area Distribution

| Risk Area | Count |
| --- | --- |
| Access Management | 1 |
| Backup & Recovery | 1 |
| Business Continuity | 1 |
| Change Management | 1 |
| Data Integrity | 1 |
| Data Privacy | 1 |
| Data Quality | 1 |
| Data Retention | 1 |
| Incident Handling | 1 |
| Logging & Monitoring | 1 |
| Security Awareness | 1 |
| User Lifecycle Management | 1 |
| Vendor Dependency | 1 |
| Vulnerability Management | 1 |
| Workflow Evidence | 1 |

---

## Top Risks for Management Attention

The following risks have the highest management relevance due to high residual exposure, privacy impact, service continuity impact, or weak/missing controls.

| Risk ID | Risk Statement | Residual Risk | Priority | Owner |
| --- | --- | --- | --- | --- |
| R-001 | Unauthorized staff may access sensitive academic records due to lack of periodic user access review and role recertification. | 15 | High | IT Manager / System Owner |
| R-004 | System changes may disrupt academic services if approval, testing, and UAT evidence are not consistently documented before release. | 12 | High | System Owner / Academic Operations |
| R-010 | Inactive, transferred, or resigned user accounts may remain active due to incomplete offboarding and access revocation tracking. | 12 | High | IT Admin / HR Coordinator |
| R-002 | Student personal data may be exposed due to excessive admin access and insufficient restriction over sensitive data visibility. | 12 | High | Data Owner / Academic Services |
| R-003 | Critical academic services may not recover within expected time if backup restoration is not tested and documented. | 12 | High | IT Operations Lead |
| R-009 | Course registration may become unavailable during peak periods if continuity planning and capacity readiness are not tested. | 12 | High | Academic Operations / IT Operations |
| R-013 | Personal data may be retained longer than necessary if retention and deletion review procedures are not defined. | 12 | High | Data Owner / Compliance Coordinator |
| R-015 | Known vulnerabilities in supporting systems or third-party components may remain unresolved if vulnerability tracking is not maintained. | 12 | High | IT Security / Vendor Manager |

---

## Full Risk Register Overview

| Risk ID | Asset ID | Risk Area | Likelihood | Impact | Inherent | Residual | Priority | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-001 | A-005; A-009 | Access Management | 4 | 5 | 20 | 15 | High | IT Manager / System Owner |
| R-002 | A-001; A-006 | Data Privacy | 3 | 5 | 15 | 12 | High | Data Owner / Academic Services |
| R-003 | A-008; A-006 | Backup & Recovery | 3 | 5 | 15 | 12 | High | IT Operations Lead |
| R-004 | A-010; A-002; A-005 | Change Management | 4 | 4 | 16 | 12 | High | System Owner / Academic Operations |
| R-005 | A-011 | Incident Handling | 3 | 4 | 12 | 9 | Medium | Helpdesk Lead / IT Support |
| R-006 | A-005; A-006 | Logging & Monitoring | 3 | 4 | 12 | 10 | Medium | IT Security / System Administrator |
| R-007 | A-012 | Vendor Dependency | 3 | 4 | 12 | 9 | Medium | Vendor Manager / IT Manager |
| R-008 | A-007; A-006 | Data Quality | 4 | 3 | 12 | 8 | Medium | BI / Reporting Owner |
| R-009 | A-002; A-006 | Business Continuity | 3 | 5 | 15 | 12 | High | Academic Operations / IT Operations |
| R-010 | A-009; A-005 | User Lifecycle Management | 4 | 4 | 16 | 12 | High | IT Admin / HR Coordinator |
| R-011 | A-003; A-006 | Data Integrity | 3 | 4 | 12 | 9 | Medium | Finance Data Owner / Academic Services |
| R-012 | A-004 | Workflow Evidence | 3 | 3 | 9 | 6 | Medium | Academic Services Lead |
| R-013 | A-001; A-006 | Data Retention | 3 | 4 | 12 | 12 | High | Data Owner / Compliance Coordinator |
| R-014 | A-005; A-009 | Security Awareness | 3 | 4 | 12 | 10 | Medium | IT Security / HR Training Coordinator |
| R-015 | A-006; A-007; A-012 | Vulnerability Management | 3 | 4 | 12 | 12 | High | IT Security / Vendor Manager |

---

## Risk Response Approach

The project uses four common risk response categories:

| Response | Meaning |
|---|---|
| Mitigate | Implement or strengthen controls to reduce likelihood or impact |
| Accept | Management accepts risk within tolerance |
| Transfer | Shift part of risk through vendor, insurance, or contractual mechanism |
| Avoid | Stop or redesign the activity causing the risk |

For this simulated assessment, all identified risks are currently assigned **Mitigate** because the objective is to demonstrate control improvement, remediation planning, and audit-readiness tracking.

---

## Source Alignment

The risk register is mapped to source references such as:

- **NIST CSF 2.0** for governance, identify, protect, detect, respond, and recover concepts.
- **NIST SP 800-30 Rev. 1** for risk assessment structure.
- **NIST SP 800-53 Rev. 5** for security and privacy control family references.
- **NIST SP 800-53A Rev. 5** for later control assessment and evidence logic.
- **ISO/IEC 27001 concepts** for confidentiality, integrity, availability, and ISMS-oriented risk thinking.
- **CIS Controls v8.1** for practical safeguard themes.
- **COBIT governance concepts** for IT governance, risk, accountability, and management reporting.
- **Indonesia PDP Law** for personal data protection context.

Each row in `risk_register.csv` includes a `source_reference` field to explain the basis for the risk/control mapping.

---

## Key Observations

1. **Access management and user lifecycle risks are high priority** because the simulated system processes sensitive academic and personal data.
2. **Backup and business continuity risks are high priority** because academic services can become time-sensitive during registration and operational peak periods.
3. **Change management is a major governance concern** because informal approvals and weak UAT evidence can create operational disruption and weak audit trail.
4. **Data privacy and retention risks require strong evidence** because personal data handling must be defensible and traceable.
5. **Control effectiveness is mostly Partial, Weak, or Missing**, which creates clear input for the next project phase: control matrix and control assessment.

---

## Limitations

- The risk register uses synthetic data and does not represent a real organization.
- The scoring model is simplified for portfolio demonstration.
- Control IDs are preliminary references that will be expanded in the next step: `control_matrix.csv`.
- No real personal data, employee data, student data, system logs, or audit evidence is included.

---

## Next Step

The next project artifact is the **Control Matrix**, which will define control objectives, control activities, owners, frequencies, evidence requirements, framework mapping, and implementation status for the risks listed here.
