# 01 - Scope and Method

## Objective

Turn a real banking cyber incident into a defensible public-evidence IT GRC assessment that a recruiter or interviewer can inspect end to end.

## Assessment question

What do public BSI, OJK, audited-filing, legal, regulatory, technical, and reputable media sources establish about the May 2023 disruption, and what control areas should an IT GRC analyst prioritize without pretending to have internal audit access?

## In scope

- Public events from 7-16 May 2023.
- BSI's year-end disclosure of the 8 May cyber incident.
- Service availability, recovery, investigation, regulatory coordination, communication, data-protection uncertainty, and post-incident improvement.
- Mapping to POJK No. 11/POJK.03/2022, SEOJK No. 29/SEOJK.03/2022, Law No. 27 of 2022, NIST SP 800-61 Rev. 3, and NIST SP 800-184.
- Analyst recommendations and expected evidence artifacts.

## Out of scope

- Penetration testing, vulnerability scanning, or contact with BSI systems.
- Access to leaked or allegedly stolen data.
- Claims about malware entry path, staff action, affected records, or final forensic root cause.
- Certification, legal opinion, regulatory finding, or internal control effectiveness conclusion.
- Any claim that recommendations in this repository were adopted by BSI.

## Evidence hierarchy

| Rank | Evidence type | Use |
|---:|---|---|
| 1 | BSI and OJK official disclosure | Incident dates, public action, and attributed statements. |
| 2 | Audited BSI filing | Year-end management disclosure. |
| 3 | Regulation, law, and official standard | Control expectation and recommendation design. |
| 4 | Reuters reporting | Third-party claim context only. |

## Classification rules

- `Confirmed public fact`: supported by at least one authoritative primary source, preferably corroborated.
- `Issuer statement`: fact about what the issuer said or reported; not independent assurance.
- `Confirmed regulator statement`: fact about what OJK observed, requested, or communicated.
- `Management statement in audited filing`: management representation appearing in audited financial statements; not a forensic audit conclusion.
- `Reported third-party claim`: attributed external allegation; excluded from confirmed-fact counts.
- `Not publicly observable`: the source set is insufficient; no positive or negative control conclusion is allowed.

## Workflow

1. Register sources and define allowed use.
2. Extract dated events and preserve attribution.
3. Build a claim register, including unknowns.
4. Map regulatory and technical expectations.
5. Assess public observability rather than control effectiveness.
6. Propose evidence-based actions with deliverables and suggested owners.
7. Validate citation coverage, wording guardrails, SQL outputs, workbook structure, and PDF rendering.

## Success criteria

- Every analytical row cites valid sources.
- No confirmed-fact metric includes LockBit's unverified claim.
- No missing public disclosure is called a failed control.
- Recommendations are labelled as analyst proposals.
- The Excel workpaper is generated from repository data and contains no decorative chart.
- The PDF uses a plain audit-memorandum layout and contains no unsupported claim.

Source details are in [`../data/source_catalog.csv`](../data/source_catalog.csv).
