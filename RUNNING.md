# Run and Validate

## Requirements

- Python 3.11 or later
- `reportlab` and `pypdf`
- Poppler only for optional PDF rendering
- Node.js and `@oai/artifact-tool` only when rebuilding the Excel workpaper

## Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

## Generate the audit memorandum

```powershell
python scripts\generate_audit_memo.py
```

Expected file:

```text
output/pdf/BSI_Public_Evidence_GRC_Assessment_Memo.pdf
```

## Rebuild the Excel workpaper

```powershell
node scripts\build_grc_workpaper.mjs
```

Expected file:

```text
output/workbook/BSI_Public_Evidence_GRC_Workpaper.xlsx
```

The workbook builder also renders all six worksheets to `tmp/workbook-renders/` for visual inspection. Temporary previews are ignored by Git.

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
workbook_integrity=passed
pdf_integrity=passed
no_infographics=passed
markdown_links=passed
secret_scan=passed
```

## Optional PDF visual check

```powershell
pdftoppm -png output\pdf\BSI_Public_Evidence_GRC_Assessment_Memo.pdf tmp\pdfs\bsi-grc-memo
```

Inspect all six pages for clipped text, overlapping rows, unreadable tables, or missing headers and footers.
