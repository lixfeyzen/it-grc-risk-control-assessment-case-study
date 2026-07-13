# Methodology and Source Mapping

## Purpose

This document explains the methodology and industry references used to design the IT GRC Risk & Control Assessment Case Study.

The goal is to make the project source-based, transparent, and aligned with common IT GRC practices rather than presenting it as a generic risk register template.

---

## Methodology Overview

The project follows a simplified IT GRC assessment workflow:

```text
Define Scope
    ↓
Identify Assets
    ↓
Identify Risks
    ↓
Score Inherent Risk
    ↓
Map Existing Controls
    ↓
Assess Control Design, Implementation, Operation, and Evidence
    ↓
Determine Residual Risk and Gaps
    ↓
Create Remediation Plan / POA&M
    ↓
Track Evidence
    ↓
Prepare Management Summary
```

---

## Frameworks and References

The project uses public industry references as guidance for structure, terminology, and mapping.

| Reference | Official Source | How It Is Used in This Project |
|---|---|---|
| NIST Cybersecurity Framework 2.0 | https://www.nist.gov/cyberframework | Used as the high-level structure for Govern, Identify, Protect, Detect, Respond, and Recover concepts |
| NIST SP 800-30 Rev. 1 | https://csrc.nist.gov/pubs/sp/800/30/r1/final | Used for risk assessment logic, including likelihood, impact, inherent risk, residual risk, and response |
| NIST SP 800-53 Rev. 5 | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | Used for security and privacy control family mapping |
| NIST SP 800-53A Rev. 5 | https://csrc.nist.gov/pubs/sp/800/53/a/r5/final | Used for control assessment concepts such as test procedure, evidence, implementation, and effectiveness |
| ISO/IEC 27001:2022 | https://www.iso.org/standard/27001 | Used for information security management concepts, including confidentiality, integrity, availability, and risk treatment thinking |
| CIS Controls v8.1 | https://www.cisecurity.org/controls | Used for practical cybersecurity safeguards and cyber hygiene control themes |
| COBIT / ISACA | https://www.isaca.org/resources/cobit | Used for governance and management of enterprise IT concepts, control ownership, and accountability framing |
| Indonesia Law No. 27 of 2022 on Personal Data Protection | https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 | Used for Indonesian personal data protection context and data privacy risk framing |

---

## How Each Reference Is Applied

### 1. NIST Cybersecurity Framework 2.0

NIST CSF 2.0 is used as a high-level organizing structure.

| NIST CSF Function | Project Application |
|---|---|
| Govern | Defines governance context, roles, owners, accountability, and management reporting |
| Identify | Supports asset inventory and risk identification |
| Protect | Supports access control, data protection, awareness, and backup controls |
| Detect | Supports logging, monitoring, and evidence review controls |
| Respond | Supports incident handling, escalation, and response documentation |
| Recover | Supports backup restoration, recovery readiness, and continuity planning |

---

### 2. NIST SP 800-30 Rev. 1

NIST SP 800-30 is used as inspiration for the risk assessment approach.

The project applies a simplified scoring model:

```text
Likelihood Score × Impact Score = Inherent Risk Score
```

Residual risk is assessed after considering existing control effectiveness.

Risk response options used in the project:

- Mitigate
- Accept
- Transfer
- Avoid

Risk register fields inspired by NIST SP 800-30 include:

- threat event,
- vulnerability,
- business impact,
- likelihood score,
- impact score,
- inherent risk score,
- residual risk score,
- risk response.

---

### 3. NIST SP 800-53 Rev. 5

NIST SP 800-53 is used to map risks to relevant security and privacy control families.

Example mapping:

| Risk Area | NIST SP 800-53 Control Family |
|---|---|
| Access Management | Access Control, Identification and Authentication |
| Logging & Monitoring | Audit and Accountability |
| Backup & Recovery | Contingency Planning |
| Change Management | Configuration Management |
| Incident Handling | Incident Response |
| Vendor Dependency | Supply Chain Risk Management |
| Data Privacy | Privacy and Access Control concepts |
| Risk Management | Risk Assessment |

The project does not implement the full NIST SP 800-53 catalog. It uses selected control families as source-based references for portfolio-level control mapping.

---

### 4. NIST SP 800-53A Rev. 5

NIST SP 800-53A is used to structure the control assessment result.

The project assesses controls using simplified fields:

| Assessment Field | Meaning |
|---|---|
| Test Procedure | How the control would be reviewed |
| Design Effectiveness | Whether the control design is appropriate |
| Implementation Status | Whether the control is implemented, partial, or missing |
| Operating Effectiveness | Whether the control appears to work consistently |
| Evidence Status | Whether evidence is available, partial, or unavailable |
| Finding | Issue identified from assessment |
| Severity | High, Medium, or Low |
| Recommendation | Suggested improvement |

This is not an official NIST control assessment. It is a simplified portfolio demonstration inspired by control assessment concepts.

---

### 5. ISO/IEC 27001:2022 Concepts

ISO/IEC 27001 concepts are used for information security management framing.

The project applies the following themes:

- confidentiality,
- integrity,
- availability,
- risk treatment,
- control ownership,
- continual improvement,
- management awareness.

The project does not claim ISO 27001 certification readiness or official ISO audit work.

---

### 6. CIS Controls v8.1

CIS Controls are used for practical cyber hygiene safeguards.

Example project themes inspired by CIS Controls:

- asset inventory,
- account management,
- access control management,
- vulnerability management,
- audit log management,
- data protection,
- incident response,
- security awareness.

CIS Controls help make the project practical and measurable rather than purely theoretical.

---

### 7. COBIT Governance Concepts

COBIT is used for governance framing, especially:

- IT governance and management accountability,
- risk ownership,
- control ownership,
- management reporting,
- process improvement,
- governance over enterprise IT.

The project does not claim an official COBIT assessment. It uses COBIT concepts to support governance-oriented documentation.

---

### 8. Indonesia Personal Data Protection Law

Indonesia Law No. 27 of 2022 on Personal Data Protection is used as the Indonesian privacy compliance context.

The project uses this reference for risks related to:

- excessive access to personal data,
- weak access review,
- unclear data handling responsibility,
- insufficient evidence over personal data protection controls,
- and privacy-related risk treatment.

This project does not provide a legal opinion.

---

## Source-to-Artifact Mapping

| Project Artifact | Primary Source Influence |
|---|---|
| Asset Inventory | NIST CSF Identify, CIS asset inventory concept |
| Risk Register | NIST SP 800-30, NIST CSF Govern/Identify, ISO 27001 risk concepts |
| Control Matrix | NIST SP 800-53, CIS Controls, COBIT governance concepts |
| Control Assessment Results | NIST SP 800-53A concepts |
| Gap Analysis | NIST RMF-style improvement thinking, ISO 27001 continual improvement concepts |
| Remediation Plan / POA&M | NIST risk management and remediation tracking concepts |
| Evidence Tracker | NIST SP 800-53A evidence/testing concepts, audit-readiness practice |
| Management Summary | COBIT governance reporting concepts, NIST CSF communication concepts |
| Data Privacy Risks | Indonesia PDP Law, NIST privacy/security control concepts |

---

## Scoring Method

The project uses a simplified 1–5 scoring model.

### Likelihood Score

| Score | Meaning |
|---:|---|
| 1 | Rare |
| 2 | Unlikely |
| 3 | Possible |
| 4 | Likely |
| 5 | Almost Certain |

### Impact Score

| Score | Meaning |
|---:|---|
| 1 | Minimal impact |
| 2 | Minor operational impact |
| 3 | Moderate business impact |
| 4 | Major operational or compliance impact |
| 5 | Critical business, compliance, or data impact |

### Inherent Risk Score

```text
Inherent Risk Score = Likelihood Score × Impact Score
```

### Priority Classification

| Score Range | Priority |
|---:|---|
| 1–5 | Low |
| 6–11 | Medium |
| 12–25 | High |

Residual risk will be estimated after considering control effectiveness.

---

## Data Methodology

This project uses synthetic data.

The dataset is created manually to represent realistic IT GRC artifacts for an internal academic services system. It does not include real company data, real student data, real employee records, real incident records, or real audit evidence.

Synthetic data is used because real risk registers, access reviews, control assessment results, remediation plans, and audit evidence are normally confidential.

---

## Important Limitations

This project is a portfolio demonstration.

It does not represent:

- a production audit,
- a certification assessment,
- legal compliance advice,
- penetration testing,
- vulnerability scanning,
- or real evidence testing.

The project focuses on showing structured IT GRC thinking and artifact preparation for entry-level or junior IT GRC roles.
