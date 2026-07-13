# Evidence Repository Boundary

This directory documents the evidence-handling boundary for the synthetic case study.

No real audit or control evidence is stored here. Required evidence, owner, frequency, status, finding, remediation action, and target date are maintained in:

```text
data/evidence_tracker.csv
```

The tracker intentionally uses:

```text
evidence_repository_path = Not collected - synthetic case study
```

This prevents placeholder screenshots, invented approval records, fake logs, or fabricated review dates from being mistaken for real evidence.

In a real engagement, evidence storage would require access restrictions, retention rules, naming conventions, chain-of-custody considerations, reviewer access, and privacy controls.
