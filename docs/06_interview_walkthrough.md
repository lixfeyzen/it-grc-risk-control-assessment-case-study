# 06 - Interview Walkthrough

## 60-second explanation

> I built an independent IT GRC assessment using the real May 2023 BSI cyber incident. I collected official BSI and OJK disclosures, the audited year-end filing, Indonesian banking IT regulations, the PDP law, and NIST guidance. I separated confirmed facts, management statements, external claims, and unknowns. Then I mapped ten control domains and assessed only what was publicly observable. The main lesson was that lack of public evidence is not the same as a failed control. I proposed eight evidence-based remediation actions and produced an Excel audit workpaper, SQL checks, automated validation, and a six-page assessment memorandum.

## What to show first

1. `data/source_catalog.csv` - proof that the project starts with real sources.
2. `data/evidence_claims.csv` - proof that uncertainty is handled explicitly.
3. `data/control_observability.csv` - proof of cautious GRC judgment.
4. `sql/02_analysis_queries.sql` - proof of practical data handling.
5. The PDF - proof of management communication.

## Likely interview questions

### Why did you not call the control failed?

Because I had no internal test evidence. Public disclosure can show that an action occurred but cannot prove design and operating effectiveness.

### Did LockBit definitely steal the reported data?

The project does not make that claim. Reuters reported LockBit's allegation and BSI's response. I classified it as a reported third-party claim and excluded it from confirmed metrics.

### What would you request as an internal assessor?

Forensic scope and chain of custody, incident ticket timeline, SIEM/EDR evidence, channel availability telemetry, DR execution evidence, RTO/RPO results, affected-data assessment, regulator notifications, customer communications, remediation tickets, validation tests, and formal closure approval.

### What is the strongest recommendation?

Complete a forensic closure pack that links root cause, affected systems and data, corrective actions, validation evidence, accountable owners, and remaining risk acceptance.

### What technical work did you do?

I built normalized CSV datasets, a relational SQLite schema, monitoring queries, automated source-traceability and claim-guardrail checks, an Excel audit workpaper, and a generated PDF memorandum.

## Honest positioning

Describe this as an **open-source public-evidence assessment**, not a BSI audit, penetration test, or professional forensic engagement.
