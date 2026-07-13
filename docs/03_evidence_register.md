# 03 - Evidence and Claim Register

## Purpose

The evidence register prevents a common OSINT error: combining an official incident statement, a management statement, and an attacker claim into one apparently certain narrative.

## Classification summary

| Classification group | Meaning | Safe use |
|---|---|---|
| Confirmed or authoritative public statement | BSI, OJK, or the audited filing establishes the stated public fact or action. | May appear in the incident baseline with attribution where needed. |
| Issuer or management statement | BSI reported an outcome or management view. | Must remain attributed; does not prove independent effectiveness. |
| Reported third-party claim | Reuters documented what LockBit claimed. | May describe the allegation but cannot enter confirmed breach metrics. |
| Not publicly observable | Reviewed sources do not provide enough evidence. | Must remain unresolved; no invented answer. |

## High-value evidence

- S-001 provides BSI's event sequence, cyberattack indication, channel switch-off, recovery statements, and explicit forensic caveat.
- S-002 provides OJK's supervisory status, forensic-audit request, coordination, and customer-complaint context.
- S-003 records the incident in the year-end filing and states that corrective action and cybersecurity enhancement occurred.
- S-004 records an externally reported LockBit claim and BSI's non-confirmation in the report.

## Material unknowns

The reviewed source set does not establish:

- final forensic root cause;
- initial access vector;
- verified affected-record count;
- complete data categories affected;
- control design or operating-effectiveness results;
- actual channel-level RTO, RPO, or service availability;
- whether every remediation item passed independent closure testing.

## Confidence is not probability

`High` means the claim is accurately attributed and directly supported by an authoritative source. It does not mean undisclosed technical details are probably true. `Not assessable` means the evidence is insufficient and no probability estimate is offered.

The complete register is in [`../data/evidence_claims.csv`](../data/evidence_claims.csv).
