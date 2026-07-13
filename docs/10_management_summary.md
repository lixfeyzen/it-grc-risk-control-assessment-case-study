# Management Summary

## Executive Conclusion

The simulated internal academic services system has a documented control environment, but the baseline is not audit-ready. The largest issues are privileged-access governance, monitoring, recovery testing, change traceability, personal-data lifecycle governance, and vulnerability tracking.

No control is represented as fully implemented and fully evidenced. The correct management response is therefore not to claim compliance, but to prioritize remediation, collect evidence, and re-test controls after corrective actions are completed.

Assessment cut-off: **13 July 2026**.

## Management KPI Snapshot

| Metric | Result |
|---|---:|
| Assets in scope | 12 |
| High-sensitivity assets | 6 |
| High-criticality assets | 7 |
| Risks assessed | 15 |
| High-priority risks | 8 |
| Risks with residual score >= 12 | 8 |
| Average inherent risk score | 13.47 |
| Average residual risk score | 10.67 |
| Controls assessed | 15 |
| Missing or weak controls | 5 |
| Partial controls | 8 |
| Planned controls | 2 |
| High-severity findings | 7 |
| Medium-severity findings | 8 |
| Partial evidence sets | 9 |
| Evidence sets unavailable | 6 |
| POA&M actions | 15 |
| Open actions | 5 |
| Actions in progress | 4 |
| Planned actions | 6 |

## Priority Findings

### 1. Privileged access governance

`R-001` has the highest residual risk score at 15. Quarterly privileged access review is conceptually defined, but reviewer sign-off, exception tracking, removal evidence, and management approval are inconsistent.

Management action: complete `P-001` by formalizing quarterly access recertification and retaining evidence of review and removal decisions.

### 2. Detection and monitoring

Admin logs are assumed to exist, but there is no documented monthly review or exception-escalation evidence. A vulnerability backlog is also unavailable.

Management action: prioritize `P-003` and `P-013` to establish repeatable log review and vulnerability remediation tracking.

### 3. Recovery readiness

Backup activity alone does not demonstrate recoverability. No restoration-test evidence is available in the simulated baseline.

Management action: complete `P-004` with a documented restore test, measured result, issue log, remediation record, and sign-off.

### 4. Change traceability

Some change approvals exist, but UAT evidence, rollback plans, release notes, and post-implementation reviews are inconsistent.

Management action: complete `P-005` and require traceability from change request through production review.

### 5. Personal-data governance

Retention, deletion, and bulk-export review are not fully governed or evidenced. This creates privacy and accountability risk for data handled by the simulated system.

Management action: complete `P-008` and `P-014`, with data-owner approval and reviewable evidence.

## Remediation Portfolio

| Priority | Count | Management treatment |
|---|---:|---|
| High | 7 | Assign active ownership, monitor target dates, and require closure evidence before status can become Closed. |
| Medium | 8 | Schedule after immediate high-priority actions while retaining owner and target-date visibility. |

| Status | Count | Interpretation |
|---|---:|---|
| Open | 5 | Action is approved but work has not started. |
| In Progress | 4 | Remediation is underway but closure criteria are not yet met. |
| Planned | 6 | Action is scheduled but not started. |
| Closed | 0 | No action is represented as complete in the baseline. |

## Recommended Management Sequence

1. Confirm accountable owners for all seven high-priority POA&M actions.
2. Complete privileged access, log monitoring, recovery, change, retention, and vulnerability evidence first.
3. Review target dates monthly using `sql/03_grc_monitoring_queries.sql`.
4. Do not close an action until its closure criteria and evidence requirements are both satisfied.
5. Re-test the related control after remediation and update the assessment result.
6. Present the updated risk, evidence, and remediation position to management.

## Decision Statement

The synthetic organization should treat the current baseline as **remediation required**, not compliant or audit-ready. Management visibility is now possible because every risk, control finding, POA&M action, and evidence requirement has an explicit identifier and owner.
