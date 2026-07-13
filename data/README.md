# Data Source and Methodology

## Overview

All datasets in this folder are synthetic and were created for portfolio demonstration. They model an internal academic services system and do not contain real student, employee, vendor, incident, access, payment, or audit data.

## Dataset Files

| File | Rows | Purpose |
|---|---:|---|
| `asset_inventory.csv` | 12 | Defines in-scope assets, sensitivity, criticality, owners, dependencies, and key exposures. |
| `risk_register.csv` | 15 | Defines risk statements, threats, vulnerabilities, impacts, scores, owners, responses, and priorities. |
| `control_matrix.csv` | 15 | Defines control objectives, activities, owners, frequency, required evidence, and public framework themes. |
| `control_assessment_results.csv` | 15 | Defines simulated test procedures, implementation, operating effectiveness, evidence status, findings, and severity. |
| `remediation_plan_poam.csv` | 15 | Defines remediation actions, owners, target dates, dependencies, evidence requirements, and closure criteria. |
| `evidence_tracker.csv` | 15 | Connects controls, assessments, and POA&M actions to required evidence without claiming evidence was collected. |
| **Total** | **87** | Versioned CSV rows validated by `scripts/validate_project.py`. |

## Data Lineage

```text
asset_inventory.csv
        |
        v
risk_register.csv
        |
        v
control_matrix.csv
        |
        v
control_assessment_results.csv
        |
        v
remediation_plan_poam.csv
        |
        v
evidence_tracker.csv
```

Each stage uses explicit identifiers. The validator confirms that asset, risk, control, assessment, POA&M, and evidence references resolve correctly.

## Scoring Rules

- Likelihood uses a 1-to-5 scale.
- Impact uses a 1-to-5 scale.
- Inherent risk equals likelihood multiplied by impact.
- Residual risk must not exceed inherent risk.
- Priority is a simplified portfolio classification documented in the methodology.

These scores demonstrate a risk-assessment workflow and are not calibrated to a real organization's risk appetite or loss model.

## Evidence Rule

No real evidence is stored in the repository. Every evidence-tracker row uses:

```text
Not collected - synthetic case study
```

The tracker records required evidence, evidence status, owner, frequency, finding, action, and target date. It does not invent logs, screenshots, approvals, tickets, or review dates.

## Data Quality Rules

The automated validator checks:

- exact expected row counts,
- unique primary identifiers,
- non-orphan asset, risk, control, assessment, POA&M, and evidence links,
- valid score ranges and inherent-risk calculations,
- residual risk not exceeding inherent risk,
- valid target dates,
- allowed status values through SQLite constraints,
- management KPI results,
- and common secret patterns.

## Regeneration

`evidence_tracker.csv` is generated deterministically from the control, assessment, and POA&M datasets:

```bash
python scripts/generate_artifacts.py
```

The five upstream CSV datasets remain the authored source records.

## Disclaimer

The datasets do not demonstrate real audit work, real compliance, control effectiveness, or ISO/IEC 27001 conformity. They demonstrate structured IT GRC data design and analysis using a transparent synthetic scenario.
