# Data Layer

All records in this folder are built from public sources or explicitly labelled analyst output.

## Source-derived tables

- `source_catalog.csv`: authoritative source inventory.
- `incident_timeline.csv`: dated public events with classification, confidence, and source IDs.
- `evidence_claims.csv`: claim register that distinguishes confirmed facts, attributed statements, third-party claims, and unknowns.

## Analytical tables

- `control_observability.csv`: public-evidence mapping against regulatory or technical expectations. It does not test BSI's internal controls.
- `recommendation_register.csv`: portfolio analyst recommendations. Every row is labelled `Analyst proposal - not a BSI commitment`.

## Integrity rules

1. Every non-source table row must cite at least one valid `source_id`.
2. Third-party breach claims must never be counted as confirmed facts.
3. `Not publicly observable` must not be converted into `Failed` or `Missing control`.
4. No row may assert an attack vector, forensic root cause, affected-record count, or internal test result unless a reviewed primary source supports it.
5. Analyst recommendations must remain clearly separated from actions publicly attributed to BSI or OJK.

See [`data_dictionary.md`](data_dictionary.md) for field definitions.
