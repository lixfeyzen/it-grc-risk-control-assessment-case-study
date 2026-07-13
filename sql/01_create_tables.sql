PRAGMA foreign_keys = ON;

CREATE TABLE source_catalog (
    source_id TEXT PRIMARY KEY CHECK (source_id GLOB 'S-[0-9][0-9][0-9]'),
    publisher TEXT NOT NULL,
    title TEXT NOT NULL,
    publication_date TEXT NOT NULL CHECK (publication_date GLOB '????-??-??'),
    source_type TEXT NOT NULL,
    authority_level TEXT NOT NULL CHECK (authority_level IN ('Primary', 'Secondary')),
    source_locator TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE CHECK (url LIKE 'https://%'),
    accessed_date TEXT NOT NULL CHECK (accessed_date GLOB '????-??-??'),
    primary_use TEXT NOT NULL
);

CREATE TABLE incident_timeline (
    event_id TEXT PRIMARY KEY CHECK (event_id GLOB 'E-[0-9][0-9][0-9]'),
    event_date TEXT NOT NULL CHECK (event_date GLOB '????-??-??'),
    event_order INTEGER NOT NULL CHECK (event_order > 0),
    event_title TEXT NOT NULL,
    publicly_supported_fact TEXT NOT NULL,
    evidence_classification TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK (confidence IN ('High', 'Medium', 'Not assessable')),
    source_ids TEXT NOT NULL,
    UNIQUE (event_date, event_order)
);

CREATE TABLE evidence_claims (
    claim_id TEXT PRIMARY KEY CHECK (claim_id GLOB 'C-[0-9][0-9][0-9]'),
    claim_category TEXT NOT NULL,
    claim_text TEXT NOT NULL,
    classification TEXT NOT NULL,
    confidence TEXT NOT NULL CHECK (confidence IN ('High', 'Medium', 'Not assessable')),
    source_ids TEXT NOT NULL,
    analyst_treatment TEXT NOT NULL
);

CREATE TABLE control_observability (
    control_id TEXT PRIMARY KEY CHECK (control_id GLOB 'O-[0-9][0-9][0-9]'),
    control_domain TEXT NOT NULL UNIQUE,
    reference_expectation TEXT NOT NULL,
    reference_ids TEXT NOT NULL,
    public_evidence TEXT NOT NULL,
    source_ids TEXT NOT NULL,
    observability_status TEXT NOT NULL CHECK (
        observability_status IN (
            'Observed public action',
            'Partial public evidence',
            'Not publicly observable'
        )
    ),
    assessment_conclusion TEXT NOT NULL
);

CREATE TABLE recommendation_register (
    recommendation_id TEXT PRIMARY KEY CHECK (recommendation_id GLOB 'R-[0-9][0-9][0-9]'),
    priority TEXT NOT NULL CHECK (priority IN ('P1', 'P2')),
    time_horizon TEXT NOT NULL CHECK (time_horizon IN ('0-30 days', '31-90 days')),
    control_domain TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    public_evidence_basis TEXT NOT NULL,
    reference_ids TEXT NOT NULL,
    deliverable TEXT NOT NULL,
    ownership_model TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status = 'Analyst proposal - not a BSI commitment')
);

CREATE VIEW v_claim_register AS
SELECT
    claim_id,
    claim_category,
    claim_text,
    classification,
    confidence,
    source_ids,
    analyst_treatment,
    CASE
        WHEN classification = 'Reported third-party claim' THEN 'Reported claim'
        WHEN classification = 'Not publicly observable' THEN 'Not publicly observable'
        ELSE 'Confirmed or attributed public evidence'
    END AS claim_group
FROM evidence_claims;

CREATE VIEW v_claim_classification_summary AS
SELECT claim_group, COUNT(*) AS claim_count
FROM v_claim_register
GROUP BY claim_group;

CREATE VIEW v_control_observability_summary AS
SELECT observability_status, COUNT(*) AS control_count
FROM control_observability
GROUP BY observability_status;

CREATE VIEW v_recommendation_priority_summary AS
SELECT priority, time_horizon, COUNT(*) AS recommendation_count
FROM recommendation_register
GROUP BY priority, time_horizon;

CREATE VIEW v_source_usage AS
SELECT
    s.source_id,
    s.publisher,
    s.authority_level,
    (
        SELECT COUNT(*) FROM incident_timeline t
        WHERE instr(';' || t.source_ids || ';', ';' || s.source_id || ';') > 0
    ) AS timeline_rows,
    (
        SELECT COUNT(*) FROM evidence_claims c
        WHERE instr(';' || c.source_ids || ';', ';' || s.source_id || ';') > 0
    ) AS claim_rows,
    (
        SELECT COUNT(*) FROM control_observability o
        WHERE instr(';' || o.source_ids || ';', ';' || s.source_id || ';') > 0
           OR instr(';' || o.reference_ids || ';', ';' || s.source_id || ';') > 0
    ) AS control_rows,
    (
        SELECT COUNT(*) FROM recommendation_register r
        WHERE instr(';' || r.reference_ids || ';', ';' || s.source_id || ';') > 0
    ) AS recommendation_rows
FROM source_catalog s;

CREATE INDEX idx_timeline_date ON incident_timeline (event_date, event_order);
CREATE INDEX idx_claim_classification ON evidence_claims (classification);
CREATE INDEX idx_control_status ON control_observability (observability_status);
CREATE INDEX idx_recommendation_priority ON recommendation_register (priority, time_horizon);
