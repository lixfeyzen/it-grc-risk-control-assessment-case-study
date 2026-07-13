# BSI May 2023 Cyber Incident - Public-Evidence IT GRC Workpaper

An independent portfolio case study that reconstructs the May 2023 Bank Syariah Indonesia (BSI) service disruption from public evidence and evaluates the limits of what can be concluded about cyber resilience, incident response, recovery, and data protection.

> This is not an audit of BSI, is not affiliated with BSI or OJK, and uses no internal or confidential data. A control marked `Not publicly observable` is not classified as failed.

## Case position

| Question | Evidence-based answer |
|---|---|
| Was there a real service disruption? | Yes. BSI and its audited 2023 filing identify an operational impact on 8 May 2023. |
| Was a cyber incident publicly acknowledged? | Yes. BSI disclosed indications of a cyberattack and the need for audit and digital forensics. |
| Was recovery reported? | Yes. BSI and OJK published staged recovery statements between 9 and 13 May. These are not independent uptime measurements. |
| Was regulator coordination visible? | Yes. OJK disclosed supervisory coordination and requested acceleration of the forensic audit. |
| Is the final root cause public in the reviewed sources? | No. The final forensic root cause and initial-access vector remain not publicly observable. |
| Is a verified affected-record inventory public? | No. A Reuters report documents an external LockBit claim, but the reviewed primary sources do not publish a verified affected-record inventory. |
| Can internal control effectiveness be concluded? | No. Public disclosures are not control test workpapers. |

## Primary deliverables

| Deliverable | Reviewer use |
|---|---|
| [`output/workbook/BSI_Public_Evidence_GRC_Workpaper.xlsx`](output/workbook/BSI_Public_Evidence_GRC_Workpaper.xlsx) | Six-sheet Excel workpaper containing source, timeline, claim, control-observability, and recommendation registers. |
| [`output/pdf/BSI_Public_Evidence_GRC_Assessment_Memo.pdf`](output/pdf/BSI_Public_Evidence_GRC_Assessment_Memo.pdf) | Six-page black-and-white assessment memorandum for recruiter review or interview discussion. |
| [`data/source_catalog.csv`](data/source_catalog.csv) | Nine public sources with publisher, date, locator, URL, authority level, and intended use. |
| [`sql/01_create_tables.sql`](sql/01_create_tables.sql) and [`sql/02_analysis_queries.sql`](sql/02_analysis_queries.sql) | SQLite schema, integrity rules, and evidence-monitoring queries. |

The project intentionally contains no dashboard or infographic. With only 7 timeline events, 12 evidence claims, and 10 control domains, large charts add presentation weight without adding analytical evidence. The recruiter-facing format is therefore an audit workpaper and memorandum.

## Evidence set

| Register | Rows | Control rule |
|---|---:|---|
| Public sources | 9 | Eight primary sources and one secondary report used only for an attributed external claim. |
| Incident timeline | 7 | Events remain attributed to issuer, regulator, filing, or Reuters evidence. |
| Evidence claims | 12 | Eight supported or attributed claims, one reported claim, and three non-observable facts. |
| Control domains | 10 | Two observed actions, three areas with partial public evidence, and five not publicly observable. |
| Recommendations | 8 | All are labelled analyst proposals and are not presented as BSI commitments. |

## Repository map

| Path | Purpose |
|---|---|
| [`data/`](data/) | Source catalog and all analysis registers in CSV format. |
| [`docs/`](docs/) | Scope, chronology, evidence interpretation, control assessment, recommendations, interview notes, and ethics. |
| [`sql/`](sql/) | Relational schema and reusable analysis views. |
| [`scripts/build_grc_workpaper.mjs`](scripts/build_grc_workpaper.mjs) | Builds the Excel workpaper from repository CSV files. |
| [`scripts/generate_audit_memo.py`](scripts/generate_audit_memo.py) | Builds the plain PDF memorandum from the same CSV files. |
| [`scripts/validate_project.py`](scripts/validate_project.py) | Checks row counts, source traceability, claim guardrails, SQL results, files, links, and repository safety. |

## Method

1. Register each source and define its permitted analytical use.
2. Extract dated events while preserving attribution.
3. Separate supported facts, attributed statements, reported claims, and unknowns.
4. Map public evidence to Indonesian banking rules and incident-response guidance.
5. Assess public observability, not internal control effectiveness.
6. Define follow-up evidence, accountable ownership, and closure criteria.
7. Validate data integrity, source references, wording guardrails, SQL outputs, workbook structure, and PDF text.

## Core sources

- [BSI service recovery and cyber-incident indication](https://ir.bankbsi.co.id/newsroom/1a92cc8ca2_4364ce956d.pdf)
- [OJK supervisory update, 13 May 2023](https://www.ojk.go.id/id/berita-dan-kegiatan/siaran-pers/Documents/Pages/Operasional-Bank-Syariah-Indonesia-Kembali-Normal-Masyarakat-Diminta-Tenang/SP%20-%20OPERASIONAL%20BANK%20SYARIAH%20INDONESIA%20KEMBALI%20NORMAL%20MASYARAKAT%20DIMINTA%20TENANG.pdf)
- [BSI audited financial statements 2023, Note 47(f)](https://ir.bankbsi.co.id/misc/Laporan-Keuangan/Tahun-Laporan-2023/FY-2023.pdf)
- [POJK No. 11/POJK.03/2022](https://ojk.go.id/id/regulasi/Documents/Pages/Penyelenggaraan-Teknologi-Informasi-Oleh-Bank-Umum/POJK%2011%20-%2003%20-%202022.pdf)
- [SEOJK No. 29/SEOJK.03/2022](https://www.ojk.go.id/id/regulasi/Documents/Pages/Ketahanan-dan-Keamanan-Siber-Bagi-Bank-Umum/SEOJK%2029%20SEOJK.03%202022.pdf)
- [Indonesia Personal Data Protection Law](https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022)
- [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST SP 800-184](https://csrc.nist.gov/pubs/sp/800/184/final)

The complete source register, including the secondary Reuters locator and allowed use, is in [`data/source_catalog.csv`](data/source_catalog.csv).

## Reproduce and validate

```powershell
python -m pip install -r requirements.txt
python scripts/generate_audit_memo.py
python scripts/validate_project.py
```

Workbook regeneration requires Node.js and `@oai/artifact-tool`:

```powershell
node scripts/build_grc_workpaper.mjs
```

See [`RUNNING.md`](RUNNING.md) for expected outputs and validation results.

## Skills demonstrated

- Public-source evaluation and traceability
- Incident chronology reconstruction
- Evidence classification and uncertainty management
- Indonesian banking IT GRC control mapping
- SQL data modeling and quality checks
- Remediation design and closure evidence
- Audit-style reporting

## Honest boundary

This project demonstrates how an analyst can turn a real public incident into a traceable and decision-useful GRC assessment. It does not prove that BSI passed or failed any specific internal control.
