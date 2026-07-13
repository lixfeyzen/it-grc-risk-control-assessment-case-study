# Evidence Tracker

## Purpose

The evidence tracker connects every assessed control to its required evidence, assessment result, remediation action, owner, and target date.

This artifact is an **evidence index**, not a collection of real audit evidence. The scenario is synthetic, so the repository deliberately does not fabricate screenshots, approval records, tickets, logs, or review dates.

## Input Artifacts

- `data/control_matrix.csv`
- `data/control_assessment_results.csv`
- `data/remediation_plan_poam.csv`
- `data/evidence_tracker.csv`

## Evidence Tracking Method

Each evidence row is generated from three linked records:

1. The control matrix defines the control owner, frequency, and required evidence.
2. The assessment result defines whether evidence is partial or unavailable and records the finding.
3. The POA&M defines the corrective action, target date, and accountable remediation owner.

The resulting traceability is:

```text
Control -> Assessment finding -> POA&M action -> Evidence requirement
```

## Evidence Readiness Summary

| Evidence status | Count | Interpretation |
|---|---:|---|
| Partial | 9 | Some evidence is assumed or described, but the evidence set is incomplete and cannot support full review. |
| Not Available | 6 | Evidence is not available in the simulated baseline, so operating effectiveness cannot be verified. |
| Available | 0 | No control is represented as fully evidenced in this baseline. |
| **Total** | **15** | One tracker row for each assessed control. |

## Required Evidence Themes

| Theme | Example required evidence | Why it matters |
|---|---|---|
| Access governance | User-role export, approval record, exception list, access removal confirmation | Demonstrates that sensitive access is authorized and reviewed. |
| Monitoring | Admin log extract, review checklist, exception register, follow-up ticket | Demonstrates that unusual privileged activity is reviewed and escalated. |
| Recovery | Backup schedule, restore-test result, issue log, management sign-off | Demonstrates that backups can actually be restored. |
| Change management | Change request, approval, UAT result, rollback plan, post-change review | Demonstrates traceability from request to production release. |
| Privacy | Retention schedule, deletion approval, export review, exception record | Demonstrates accountable handling of personal data. |
| Vulnerability management | Vulnerability backlog, severity, owner, remediation ticket, closure evidence | Demonstrates that known weaknesses are prioritized and resolved. |

## Tracker Fields

| Field | Purpose |
|---|---|
| `evidence_id` | Unique evidence-tracker identifier. |
| `control_id` | Links to `control_matrix.csv`. |
| `assessment_id` | Links to `control_assessment_results.csv`. |
| `poam_id` | Links to `remediation_plan_poam.csv`. |
| `evidence_required` | Evidence expected to support control review. |
| `evidence_owner` | Role accountable for producing or maintaining evidence. |
| `collection_frequency` | Expected evidence collection or review cycle. |
| `evidence_status` | Current simulated readiness: Partial or Not Available. |
| `review_outcome` | Explains why the evidence is not fully reviewable. |
| `evidence_repository_path` | Explicitly states that no evidence file was collected in this synthetic case. |
| `gap_or_issue` | Finding that prevents full evidence readiness. |
| `action_required` | Corrective action needed to improve evidence readiness. |
| `evidence_due_date` | Target date inherited from the related POA&M action. |

## Evidence Integrity Rule

The project uses the following rule:

> If a real evidence file does not exist, the tracker must say that it was not collected. It must not use a placeholder screenshot, invented approval, fabricated log, or fake review date.

This rule keeps the project useful for demonstrating GRC reasoning without misrepresenting simulated work as a real audit engagement.

## Source Alignment

- NIST SP 800-53A Rev. 5 supports an evidence-based control assessment approach.
- NIST CSF 2.0 supports governance and oversight outcomes.
- COBIT concepts support ownership, monitoring, and management reporting.
- ISO/IEC 27001 public concepts support risk-aware information security management and continual improvement.

## Status

The evidence tracker is complete for the synthetic baseline. All 15 controls have a linked evidence requirement, assessment finding, remediation action, owner, and due date.
