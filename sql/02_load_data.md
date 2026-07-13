# Loading the CSV data into SQLite

The repository validator loads all six CSV datasets into an in-memory SQLite database, enforces the schema constraints, and executes the monitoring queries.

Run from the repository root:

```bash
python scripts/generate_artifacts.py
python scripts/validate_project.py
```

This approach is cross-platform and avoids relying on SQLite CLI dot-commands. The generated database is intentionally not committed because all tables can be recreated from the versioned CSV files and `sql/01_create_tables.sql`.
