# SQL Layer

`01_create_tables.sql` creates the normalized SQLite schema, integrity constraints, indexes, and reporting views.

`02_analysis_queries.sql` contains nine review queries for:

- public chronology;
- claim classification;
- material unknowns;
- control observability;
- evidence gaps;
- proposed action priority;
- source usage;
- recovery-statement reconciliation; and
- traceability exceptions.

The validation script loads every CSV into an in-memory SQLite database and verifies the expected results.
