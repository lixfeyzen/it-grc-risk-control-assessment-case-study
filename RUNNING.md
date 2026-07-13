# Run and Validate

## Requirements

- Python 3.11 or later
- `Pillow`, `reportlab`, and `pypdf`
- Poppler only when re-rendering the PDF for visual inspection

## Install

```powershell
python -m pip install -r requirements.txt
```

## Generate charts and PDF

```powershell
python scripts\generate_artifacts.py
```

Expected files:

```text
assets/incident_timeline.png
assets/evidence_classification.png
assets/control_observability.png
assets/recommendation_priority.png
output/pdf/Public_Evidence_Banking_Cyber_Incident_GRC_Assessment.pdf
```

## Validate

```powershell
python scripts\validate_project.py
```

Expected result:

```text
validation=passed
sources=9
timeline_events=7
evidence_claims=12
control_domains=10
recommendations=8
source_traceability=passed
claim_guardrails=passed
sql_queries=passed
artifact_integrity=passed
markdown_links=passed
secret_scan=passed
```

## Optional PDF visual check

```powershell
pdftoppm -png output\pdf\Public_Evidence_Banking_Cyber_Incident_GRC_Assessment.pdf tmp\pdfs\public-evidence-grc
```

Inspect every rendered page for clipped text, overlap, unreadable tables, or inconsistent spacing.
