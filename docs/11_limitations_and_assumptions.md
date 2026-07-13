# Limitations and Assumptions

## Purpose

This document defines what the project demonstrates and what it does not claim.

## Scenario Assumptions

- The internal academic services system, organization, roles, assets, risks, findings, and remediation dates are simulated.
- The system is assumed to process student identity, enrollment, academic, payment-status, and service-request information.
- System logs, access requests, backup processes, and change records may exist in the scenario, but their operating effectiveness is not assumed without evidence.
- Scores use a simplified 1-to-5 likelihood and impact scale for portfolio demonstration.
- The assessment cut-off date is 13 July 2026.

## Evidence Limitation

No real evidence files were collected. The repository does not contain:

- real user-access exports,
- real approval records,
- production logs,
- incident tickets,
- backup screenshots,
- vulnerability reports,
- personal data,
- or real management sign-offs.

`data/evidence_tracker.csv` records what evidence would be required and explicitly marks the repository path as `Not collected - synthetic case study`.

## Framework Limitation

The project uses public framework pages and high-level concepts for learning and traceability.

- NIST publications support risk, control-family, and assessment methodology.
- CIS Controls support practical safeguard themes.
- COBIT supports governance, ownership, monitoring, and management concepts.
- ISO/IEC 27001 references are limited to publicly described ISMS, risk-management, confidentiality, integrity, availability, and continual-improvement concepts.
- Indonesia Law No. 27 of 2022 supports the privacy context.

The project does not reproduce copyrighted framework content, claim an authoritative crosswalk, or substitute for licensed standards and professional judgment.

## Claims Explicitly Not Made

This project is not:

- a real company engagement,
- a formal internal or external audit,
- an ISO/IEC 27001 certification assessment,
- a COBIT capability or maturity assessment,
- a legal compliance opinion,
- a penetration test,
- a production security review,
- or evidence of professional audit work experience.

## Data and Scoring Limitations

- Synthetic findings may not represent the frequency or severity of issues in a real organization.
- Risk scoring is ordinal and simplified; it does not model financial loss, threat intelligence, control reliability statistics, or enterprise risk appetite.
- Residual risk values demonstrate prioritization logic and are not independently calibrated.
- Multi-value asset and risk relationships are stored as semicolon-separated identifiers for readability. A production implementation should use bridge tables.
- POA&M target dates and owners are simulated planning fields, not commitments made by a real organization.

## Technical Limitations

- The SQLite schema is designed for portfolio validation and management queries, not a multi-user production GRC platform.
- The repository does not implement authentication, workflow approvals, immutable evidence storage, or role-based access control.
- Visuals are generated from the current CSV baseline and must be regenerated if source data changes.

## Safe Interpretation

The project demonstrates that the author can:

- structure an IT GRC assessment,
- define and validate data relationships,
- identify control and evidence gaps,
- build a remediation tracker,
- create management queries,
- and communicate results with clear limitations.

It should be discussed in interviews as a **self-directed synthetic case study**, not as production or client experience.
