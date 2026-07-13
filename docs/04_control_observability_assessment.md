# 04 - Control Observability Assessment

## Important distinction

This project does not test BSI controls. It asks whether public sources expose evidence of an action or outcome relevant to a control expectation.

| Status | Meaning |
|---|---|
| `Observed public action` | A public source shows that an action occurred. This does not prove effectiveness. |
| `Partial public evidence` | Some relevant action or result is visible, but design, scope, timing, or validation evidence is missing. |
| `Not publicly observable` | Reviewed sources do not provide the evidence needed for a conclusion. This is not a failure rating. |

## Assessment summary

| Domain | Status | Safe conclusion |
|---|---|---|
| Disaster recovery | Not publicly observable | Restoration was reported, but DR plans, tests, RTO, and RPO are not public. |
| Cyber risk identification | Not publicly observable | No public asset, threat, vulnerability, or dependency assessment. |
| Cyber maturity assessment | Not publicly observable | No public maturity result. |
| Security testing | Not publicly observable | No public vulnerability or scenario-test evidence. |
| Detection and containment | Partial public evidence | Channel switch-off is visible; telemetry and criteria are not. |
| Forensic investigation and coordination | Observed public action | Investigation and regulator coordination are visible; outcome is not. |
| Service recovery | Partial public evidence | Recovery statements exist; independently measured service levels do not. |
| Personal-data protection | Not publicly observable | Conflicting statements exist; no public verified data-impact assessment. |
| Stakeholder communication | Observed public action | BSI and OJK communicated publicly; completeness is not scored. |
| Post-incident improvement | Partial public evidence | Enhancement is stated; implementation and closure testing are not public. |

## Regulatory basis

- POJK No. 11/POJK.03/2022 Article 18: disaster recovery planning, execution, testing, and review.
- Articles 21-26: cyber resilience, maturity assessment, testing, and independent cyber function.
- Articles 43-45: data management and personal-data protection.
- SEOJK No. 29/SEOJK.03/2022: cyber-risk assessment, maturity, testing, reporting, and evidence formats.
- NIST SP 800-61 Rev. 3 and SP 800-184: incident response and event recovery guidance.

Detailed records are in [`../data/control_observability.csv`](../data/control_observability.csv).
