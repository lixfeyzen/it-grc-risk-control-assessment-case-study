-- 1. Evidence-based public chronology
SELECT
    event_date,
    event_order,
    event_title,
    evidence_classification,
    confidence,
    source_ids
FROM incident_timeline
ORDER BY event_date, event_order;

-- 2. Claim classification summary
SELECT claim_group, claim_count
FROM v_claim_classification_summary
ORDER BY claim_count DESC, claim_group;

-- 3. Material facts that remain unknown
SELECT claim_id, claim_category, claim_text, analyst_treatment
FROM v_claim_register
WHERE claim_group = 'Not publicly observable'
ORDER BY claim_id;

-- 4. Public control-observability summary
SELECT observability_status, control_count
FROM v_control_observability_summary
ORDER BY CASE observability_status
    WHEN 'Observed public action' THEN 1
    WHEN 'Partial public evidence' THEN 2
    ELSE 3
END;

-- 5. Controls requiring internal evidence before a conclusion
SELECT control_id, control_domain, public_evidence, assessment_conclusion
FROM control_observability
WHERE observability_status <> 'Observed public action'
ORDER BY CASE observability_status
    WHEN 'Partial public evidence' THEN 1
    ELSE 2
END, control_id;

-- 6. Prioritized proposed actions
SELECT
    recommendation_id,
    priority,
    time_horizon,
    control_domain,
    recommendation,
    deliverable,
    ownership_model
FROM recommendation_register
ORDER BY priority, CASE time_horizon WHEN '0-30 days' THEN 1 ELSE 2 END, recommendation_id;

-- 7. Source usage and traceability
SELECT
    source_id,
    publisher,
    authority_level,
    timeline_rows,
    claim_rows,
    control_rows,
    recommendation_rows
FROM v_source_usage
ORDER BY source_id;

-- 8. Recovery statements that need channel-level telemetry for reconciliation
SELECT event_date, event_title, publicly_supported_fact, source_ids
FROM incident_timeline
WHERE event_title IN (
    'Issuer reports channel recovery',
    'Regulator confirms progressive normalization'
)
ORDER BY event_date;

-- 9. Traceability exceptions; expected result is zero rows
WITH all_references AS (
    SELECT event_id AS record_id, source_ids AS ids FROM incident_timeline
    UNION ALL
    SELECT claim_id, source_ids FROM evidence_claims
    UNION ALL
    SELECT control_id, source_ids || ';' || reference_ids FROM control_observability
    UNION ALL
    SELECT recommendation_id, reference_ids FROM recommendation_register
)
SELECT record_id, ids
FROM all_references
WHERE ids IS NULL OR trim(ids) = '';
