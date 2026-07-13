# Run and Verify the Project

## Requirements

- Python 3.10+
- Packages in `requirements.txt`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Generate the Evidence Tracker, Visuals, and PDF

```bash
python scripts/generate_artifacts.py
```

Generated files:

```text
data/evidence_tracker.csv
assets/grc_workflow.png
assets/risk_heatmap.png
assets/control_gap_summary.png
assets/remediation_status_summary.png
output/pdf/IT_GRC_Project_Summary.pdf
```

## Validate the Project

```bash
python scripts/validate_project.py
```

The validator checks:

- required dataset row counts,
- duplicate identifiers,
- asset-risk-control-assessment-POA&M-evidence relationships,
- likelihood, impact, inherent-risk, and residual-risk logic,
- ISO-formatted target dates,
- SQLite table constraints and monitoring-query syntax,
- expected management KPI results,
- and common secret or private-key patterns.

Expected final result:

```text
validation=passed
csv_rows=87
relationship_checks=passed
risk_score_checks=passed
sql_schema_and_queries=passed
secret_scan=passed
```

## Important Boundary

The project uses synthetic data. Running the generator or validator does not create real evidence, perform an audit, certify compliance, or test a production system.
