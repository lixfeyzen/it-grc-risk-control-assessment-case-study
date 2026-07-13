# Data Dictionary

This file explains the datasets used in the IT GRC Risk & Control Assessment Case Study.

The datasets are synthetic and created for portfolio demonstration purposes.

---
## `asset_inventory.csv`

| Column | Description |
|---|---|
| `asset_id` | Unique asset identifier, e.g., A-001. |
| `asset_name` | Name of the in-scope asset. |
| `asset_type` | Type of asset such as application module, database, repository, infrastructure, or third-party portal. |
| `business_function` | Business process or operational function supported by the asset. |
| `primary_data_processed` | Main data type processed by the asset. |
| `data_sensitivity` | Sensitivity rating: High, Medium, or Low. |
| `business_criticality` | Operational criticality rating: High, Medium, or Low. |
| `asset_owner` | Simulated business or IT owner responsible for the asset. |
| `system_dependency` | Main system or process dependencies. |
| `availability_requirement` | Availability expectation based on operational importance. |
| `key_risk_exposure` | Key GRC or IT risk exposure associated with the asset. |
| `related_grc_area` | Related governance, risk, or compliance topic. |
| `source_reference` | Source/framework references used to justify the GRC relevance. |
| `scope_status` | In Scope or Out of Scope. |
| `notes` | Additional project notes. |

---

## `risk_register.csv`

| Column | Description |
|---|---|
| `risk_id` | Unique identifier for each risk, e.g., R-001. |
| `asset_id` | Related asset ID from asset_inventory.csv; multiple IDs can be separated by semicolon. |
| `risk_area` | Risk category such as Access Management, Data Privacy, or Change Management. |
| `risk_statement` | Clear statement of what could go wrong and why it matters. |
| `threat_event` | Possible event that could trigger the risk. |
| `vulnerability` | Weakness or condition that allows the risk to occur. |
| `business_impact` | Potential operational, privacy, compliance, financial, or service impact. |
| `likelihood_score` | Score from 1 to 5 representing probability/possibility of occurrence. |
| `impact_score` | Score from 1 to 5 representing business severity. |
| `inherent_risk_score` | Likelihood multiplied by impact before considering existing controls. |
| `existing_control_id` | Preliminary control ID mapped to the risk. |
| `control_effectiveness` | High-level control effectiveness rating: Effective, Partial, Weak, or Missing. |
| `residual_risk_score` | Estimated remaining risk after considering current control effectiveness. |
| `risk_owner` | Role responsible for managing the risk. |
| `risk_response` | Planned response such as Mitigate, Accept, Transfer, or Avoid. |
| `priority` | Management priority: High, Medium, or Low. |
| `source_reference` | Framework, standard, or regulation reference used to support the risk/control mapping. |

---

## `control_matrix.csv`

| Column | Description |
|---|---|
| `control_id` | Unique identifier for each control, e.g., C-001. |
| `control_area` | Control category or domain. |
| `control_objective` | Objective the control is expected to achieve. |
| `control_activity` | Specific activity or procedure used to operate the control. |
| `control_type` | Preventive, Detective, Corrective, or combination. |
| `frequency` | Expected control operation frequency. |
| `control_owner` | Role responsible for operating or overseeing the control. |
| `evidence_required` | Evidence expected to demonstrate the control is designed and/or operating. |
| `mapped_risk_id` | Risk ID(s) addressed by the control. |
| `mapped_asset_id` | Asset ID(s) covered by the control. |
| `nist_csf_mapping` | High-level NIST CSF mapping used for source alignment. |
| `nist_80053_family` | NIST SP 800-53 control family mapping. |
| `iso27001_theme` | ISO/IEC 27001 concept or information security theme. |
| `cis_control_theme` | CIS Controls theme or safeguard area. |
| `cobit_theme` | COBIT governance or management concept used as reference. |
| `implementation_status` | Simulated current implementation status: Implemented, Partial, Weak, Missing, or Planned. |
| `control_maturity` | Short note on current simulated maturity level. |
| `source_reference` | Textual reference to standards/frameworks used. |
| `source_url` | Public URL(s) for framework/regulation references. |
| `notes` | Additional control notes. |

---

## `control_assessment_results.csv`

| Column | Description |
|---|---|
| `assessment_id` | Unique assessment identifier, e.g., A-001. |
| `control_id` | Control ID being assessed. |
| `test_procedure` | Simulated test procedure used to assess the control. |
| `design_effectiveness` | Whether the control design is adequate or needs improvement. |
| `implementation_status` | Simulated implementation status at assessment time. |
| `operating_effectiveness` | Whether the control appears to operate effectively based on available evidence. |
| `evidence_status` | Evidence availability: Available, Partial, or Not Available. |
| `finding` | Assessment finding or observation. |
| `severity` | Severity level: High or Medium. |
| `recommendation` | Recommended improvement or remediation direction. |
| `assessment_result` | Result classification such as Finding Raised, Observation Raised, or Enhancement Recommended. |
| `poam_required` | Indicates whether the item should flow into the remediation plan / POA&M. |
| `source_reference` | Framework/standard references supporting the assessment. |
| `notes` | Additional assessment notes. |

---

## Scoring Notes

Risk scoring uses a simplified likelihood-impact model for portfolio demonstration:

```text
Inherent Risk Score = Likelihood Score x Impact Score
```

Residual risk is estimated after considering existing control effectiveness. This is not a formal audit result and should not be interpreted as real organizational risk posture.

---

## Assessment Notes

Control assessment results are simulated to demonstrate an IT GRC testing and documentation workflow. The assessment fields are inspired by control assessment concepts such as test procedure, evidence review, design effectiveness, implementation status, operating effectiveness, finding, severity, and recommendation.

---

## `remediation_plan_poam.csv`

This dataset tracks remediation actions using a POA&M-style structure. Each row links a gap, risk, and control to a corrective action, owner, target date, required evidence, and closure criteria.

| Column | Description |
|---|---|
| `poam_id` | Unique remediation action identifier |
| `related_gap_id` | Related gap from `docs/07_gap_analysis.md` |
| `related_risk_id` | Related risk ID or multiple risk IDs from `risk_register.csv` |
| `related_control_id` | Related control ID from `control_matrix.csv` |
| `finding` | Assessment finding or observation that triggered the action |
| `remediation_action` | Corrective action required to close or reduce the gap |
| `owner` | Responsible control owner or action owner |
| `priority` | Remediation priority based on assessment severity: High or Medium |
| `target_date` | Target completion date for the remediation action |
| `status` | Current remediation status: Open, In Progress, Planned, Closed, or Overdue |
| `evidence_required` | Evidence required to validate completion of the remediation action |
| `closure_criteria` | Conditions that must be met before the action can be closed |
| `source_reference` | Framework or methodology references supporting the action |
| `notes` | Additional context about linkage to project artifacts |

Expected use:

- track remediation actions from assessment findings,
- support management follow-up,
- prepare evidence for audit-readiness,
- and feed Step 8 evidence tracking.

---

## `evidence_tracker.csv`

This dataset is generated from the control matrix, control assessment results, and POA&M. It records required evidence and evidence readiness without claiming that real evidence files were collected.

| Column | Description |
|---|---|
| `evidence_id` | Unique evidence-tracker identifier |
| `control_id` | Related control in `control_matrix.csv` |
| `assessment_id` | Related assessment in `control_assessment_results.csv` |
| `poam_id` | Related action in `remediation_plan_poam.csv` |
| `control_area` | Control theme or operational area |
| `evidence_required` | Evidence expected to support control review |
| `evidence_owner` | Role accountable for producing or maintaining evidence |
| `collection_frequency` | Expected collection or review cycle |
| `evidence_status` | Simulated readiness: Partial or Not Available |
| `review_outcome` | Explains why the evidence set is not fully reviewable |
| `evidence_repository_path` | States that evidence was not collected in the synthetic scenario |
| `reviewer_role` | Simulated reviewer role, not a real reviewer identity |
| `gap_or_issue` | Finding that prevents full evidence readiness |
| `action_required` | Corrective action inherited from the linked POA&M |
| `evidence_due_date` | Target date inherited from the linked POA&M |
| `confidentiality_classification` | Synthetic classification for portfolio handling |
| `retention_guidance` | States that real retention is organization-specific and out of scope |
| `notes` | Explicit synthetic-data and no-real-evidence disclaimer |

Expected use:

- monitor evidence readiness by control,
- connect assessment findings to remediation,
- identify missing or partial evidence,
- and support management reporting without fabricating audit artifacts.
