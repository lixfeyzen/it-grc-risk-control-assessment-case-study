# 02 - Public Incident Timeline

## Timeline

| Date | Event | Evidence interpretation | Sources |
|---|---|---|---|
| 7 May 2023 | BSI later stated that IT maintenance was conducted as a risk-mitigation step. | Attributed issuer statement; it does not establish root cause. | S-001 |
| 8 May 2023 | Customers experienced access difficulty; BSI's year-end filing records that operations were affected by a cyber incident. | Confirmed disruption and cyber-incident date. | S-001, S-003 |
| 9 May 2023 | BSI reported branch and ATM transactions available and basic mobile functions returning gradually. | Attributed recovery statement. | S-001 |
| 11 May 2023 | BSI reported branch, ATM, and mobile banking as normal and described capacity increases for core and critical channels. | Attributed issuer recovery statement. | S-001 |
| 11 May 2023 | BSI disclosed indications of a cyberattack, temporary channel switch-off, and need for audit and digital forensics. | High-confidence fact about the disclosure; no final root cause. | S-001 |
| 13 May 2023 | OJK described progressive normalization, continued supervisory coordination, and requested faster forensic audit completion. | Confirmed regulator statement. | S-002 |
| 16 May 2023 | Reuters reported LockBit's data claim and reported that BSI did not confirm leakage. | Third-party claim, not a verified breach fact. | S-004 |

## Why the recovery dates are not treated as a contradiction

BSI used normal-service wording on 11 May. OJK used progressive-normalization wording on 13 May. These statements can refer to different reporting cut-offs, delivery channels, functionality levels, or supervisory perspectives. Without service telemetry, it would be unsafe to select one as an independently verified restoration timestamp.

The project therefore preserves both statements and recommends channel-level recovery metrics rather than forcing a single unsupported number.

## Derived, limited metric

The interval from the first documented access disruption on 8 May to BSI's normal-service statement on 11 May is three calendar days. This is a timeline interval, not measured downtime and not proof that every channel was unavailable throughout the period.

Machine-readable events are in [`../data/incident_timeline.csv`](../data/incident_timeline.csv).
