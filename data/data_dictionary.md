# Data Dictionary

## `source_catalog.csv`

| Field | Definition |
|---|---|
| `source_id` | Stable source key used across every analytical table. |
| `publisher` | Organization responsible for the source. |
| `title` | Document or article title. |
| `publication_date` | Original publication date in ISO format. |
| `source_type` | Issuer disclosure, regulator release, audited filing, reporting, law, regulation, or standard. |
| `authority_level` | `Primary` or `Secondary`. |
| `source_locator` | Page, note, article, section, or other location used. |
| `url` | Direct public URL. |
| `accessed_date` | Research access date. |
| `primary_use` | Allowed analytical purpose. |

## `incident_timeline.csv`

| Field | Definition |
|---|---|
| `event_id` | Stable event key. |
| `event_date` | Publicly supported event date. |
| `event_order` | Display order when events share a date. |
| `event_title` | Short event label. |
| `publicly_supported_fact` | Neutral factual or attributed event description. |
| `evidence_classification` | Public fact, issuer statement, caveated statement, regulator statement, or third-party claim. |
| `confidence` | Analyst confidence in the attribution and wording, not in undisclosed technical details. |
| `source_ids` | Semicolon-separated references to `source_catalog.csv`. |

## `evidence_claims.csv`

| Field | Definition |
|---|---|
| `claim_id` | Stable claim key. |
| `claim_category` | Availability, recovery, investigation, impact, data, or control topic. |
| `claim_text` | Claim being evaluated. |
| `classification` | Confirmed fact, attributed statement, reported claim, or not publicly observable. |
| `confidence` | `High`, `Medium`, or `Not assessable`. |
| `source_ids` | Supporting source keys. |
| `analyst_treatment` | Rule for using the claim without overstating evidence. |

## `control_observability.csv`

| Field | Definition |
|---|---|
| `control_id` | Stable assessment key. |
| `control_domain` | IT GRC topic. |
| `reference_expectation` | Regulatory or technical expectation. |
| `reference_ids` | Sources defining the expectation. |
| `public_evidence` | What the reviewed incident sources make visible. |
| `source_ids` | Incident evidence references. |
| `observability_status` | `Observed public action`, `Partial public evidence`, or `Not publicly observable`. |
| `assessment_conclusion` | Safe conclusion boundary. |

## `recommendation_register.csv`

| Field | Definition |
|---|---|
| `recommendation_id` | Stable recommendation key. |
| `priority` | Analyst-assigned `P1` or `P2`. |
| `time_horizon` | Proposed completion window. |
| `control_domain` | Target improvement domain. |
| `recommendation` | Proposed action. |
| `public_evidence_basis` | Why the proposal is relevant to the public record. |
| `reference_ids` | Regulatory, legal, or technical references. |
| `deliverable` | Evidence expected if the proposal were implemented. |
| `ownership_model` | Suggested accountable functions, not actual BSI assignments. |
| `status` | Fixed disclaimer that the row is an analyst proposal. |
