PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS v_management_summary;
DROP VIEW IF EXISTS v_assessment_poam_evidence;
DROP VIEW IF EXISTS v_risk_control_overview;
DROP TABLE IF EXISTS evidence_tracker;
DROP TABLE IF EXISTS poam;
DROP TABLE IF EXISTS assessments;
DROP TABLE IF EXISTS risks;
DROP TABLE IF EXISTS controls;
DROP TABLE IF EXISTS assets;

CREATE TABLE assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    business_function TEXT NOT NULL,
    primary_data_processed TEXT NOT NULL,
    data_sensitivity TEXT NOT NULL CHECK (data_sensitivity IN ('High', 'Medium', 'Low')),
    business_criticality TEXT NOT NULL CHECK (business_criticality IN ('High', 'Medium', 'Low')),
    asset_owner TEXT NOT NULL,
    system_dependency TEXT NOT NULL,
    availability_requirement TEXT NOT NULL,
    key_risk_exposure TEXT NOT NULL,
    related_grc_area TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    scope_status TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE controls (
    control_id TEXT PRIMARY KEY,
    control_area TEXT NOT NULL,
    control_objective TEXT NOT NULL,
    control_activity TEXT NOT NULL,
    control_type TEXT NOT NULL,
    frequency TEXT NOT NULL,
    control_owner TEXT NOT NULL,
    evidence_required TEXT NOT NULL,
    mapped_risk_id TEXT NOT NULL,
    mapped_asset_id TEXT NOT NULL,
    nist_csf_mapping TEXT NOT NULL,
    nist_80053_family TEXT NOT NULL,
    iso27001_theme TEXT NOT NULL,
    cis_control_theme TEXT NOT NULL,
    cobit_theme TEXT NOT NULL,
    implementation_status TEXT NOT NULL CHECK (implementation_status IN ('Partial', 'Weak', 'Missing', 'Planned')),
    control_maturity TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    source_url TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE risks (
    risk_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    risk_area TEXT NOT NULL,
    risk_statement TEXT NOT NULL,
    threat_event TEXT NOT NULL,
    vulnerability TEXT NOT NULL,
    business_impact TEXT NOT NULL,
    likelihood_score INTEGER NOT NULL CHECK (likelihood_score BETWEEN 1 AND 5),
    impact_score INTEGER NOT NULL CHECK (impact_score BETWEEN 1 AND 5),
    inherent_risk_score INTEGER NOT NULL CHECK (inherent_risk_score BETWEEN 1 AND 25),
    existing_control_id TEXT NOT NULL REFERENCES controls(control_id),
    control_effectiveness TEXT NOT NULL CHECK (control_effectiveness IN ('Partial', 'Weak', 'Missing')),
    residual_risk_score INTEGER NOT NULL CHECK (residual_risk_score BETWEEN 1 AND 25),
    risk_owner TEXT NOT NULL,
    risk_response TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
    source_reference TEXT NOT NULL,
    CHECK (inherent_risk_score = likelihood_score * impact_score),
    CHECK (residual_risk_score <= inherent_risk_score)
);

CREATE TABLE assessments (
    assessment_id TEXT PRIMARY KEY,
    control_id TEXT NOT NULL REFERENCES controls(control_id),
    test_procedure TEXT NOT NULL,
    design_effectiveness TEXT NOT NULL,
    implementation_status TEXT NOT NULL,
    operating_effectiveness TEXT NOT NULL,
    evidence_status TEXT NOT NULL CHECK (evidence_status IN ('Available', 'Partial', 'Not Available')),
    finding TEXT NOT NULL,
    severity TEXT NOT NULL CHECK (severity IN ('High', 'Medium', 'Low')),
    recommendation TEXT NOT NULL,
    assessment_result TEXT NOT NULL,
    poam_required TEXT NOT NULL CHECK (poam_required IN ('Yes', 'No')),
    source_reference TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE poam (
    poam_id TEXT PRIMARY KEY,
    related_gap_id TEXT NOT NULL,
    related_risk_id TEXT NOT NULL,
    related_control_id TEXT NOT NULL REFERENCES controls(control_id),
    control_area TEXT NOT NULL,
    finding TEXT NOT NULL,
    remediation_action TEXT NOT NULL,
    owner TEXT NOT NULL,
    priority TEXT NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
    target_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Open', 'In Progress', 'Planned', 'Closed', 'Overdue')),
    evidence_required TEXT NOT NULL,
    closure_criteria TEXT NOT NULL,
    dependency TEXT NOT NULL,
    expected_management_outcome TEXT NOT NULL,
    source_reference TEXT NOT NULL,
    source_url TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE evidence_tracker (
    evidence_id TEXT PRIMARY KEY,
    control_id TEXT NOT NULL REFERENCES controls(control_id),
    assessment_id TEXT NOT NULL REFERENCES assessments(assessment_id),
    poam_id TEXT NOT NULL REFERENCES poam(poam_id),
    control_area TEXT NOT NULL,
    evidence_required TEXT NOT NULL,
    evidence_owner TEXT NOT NULL,
    collection_frequency TEXT NOT NULL,
    evidence_status TEXT NOT NULL CHECK (evidence_status IN ('Available', 'Partial', 'Not Available')),
    review_outcome TEXT NOT NULL,
    evidence_repository_path TEXT NOT NULL,
    reviewer_role TEXT NOT NULL,
    gap_or_issue TEXT NOT NULL,
    action_required TEXT NOT NULL,
    evidence_due_date TEXT NOT NULL,
    confidentiality_classification TEXT NOT NULL,
    retention_guidance TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE INDEX idx_risks_priority ON risks(priority, residual_risk_score DESC);
CREATE INDEX idx_controls_status ON controls(implementation_status);
CREATE INDEX idx_assessments_evidence ON assessments(evidence_status, severity);
CREATE INDEX idx_poam_status_date ON poam(status, target_date);
CREATE INDEX idx_evidence_status ON evidence_tracker(evidence_status);

CREATE VIEW v_risk_control_overview AS
SELECT
    r.risk_id,
    r.risk_area,
    r.inherent_risk_score,
    r.residual_risk_score,
    r.priority,
    r.risk_owner,
    c.control_id,
    c.control_area,
    c.implementation_status,
    c.control_owner
FROM risks AS r
JOIN controls AS c ON c.control_id = r.existing_control_id;

CREATE VIEW v_assessment_poam_evidence AS
SELECT
    a.assessment_id,
    a.control_id,
    c.control_area,
    a.severity,
    a.assessment_result,
    a.evidence_status AS assessment_evidence_status,
    p.poam_id,
    p.priority AS poam_priority,
    p.status AS poam_status,
    p.target_date,
    p.owner AS remediation_owner,
    e.evidence_id,
    e.evidence_status AS tracker_evidence_status,
    e.review_outcome
FROM assessments AS a
JOIN controls AS c ON c.control_id = a.control_id
JOIN poam AS p ON p.related_control_id = a.control_id
JOIN evidence_tracker AS e ON e.control_id = a.control_id;

CREATE VIEW v_management_summary AS
SELECT 'assets_in_scope' AS metric, COUNT(*) AS value FROM assets
UNION ALL SELECT 'risks_assessed', COUNT(*) FROM risks
UNION ALL SELECT 'high_priority_risks', COUNT(*) FROM risks WHERE priority = 'High'
UNION ALL SELECT 'controls_assessed', COUNT(*) FROM controls
UNION ALL SELECT 'high_severity_findings', COUNT(*) FROM assessments WHERE severity = 'High'
UNION ALL SELECT 'evidence_unavailable', COUNT(*) FROM evidence_tracker WHERE evidence_status = 'Not Available'
UNION ALL SELECT 'poam_open', COUNT(*) FROM poam WHERE status = 'Open'
UNION ALL SELECT 'poam_in_progress', COUNT(*) FROM poam WHERE status = 'In Progress';
