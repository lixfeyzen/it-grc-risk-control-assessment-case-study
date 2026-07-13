-- Query 1: Risk exposure by priority.
SELECT
    priority,
    COUNT(*) AS risk_count,
    ROUND(AVG(inherent_risk_score), 2) AS avg_inherent_score,
    ROUND(AVG(residual_risk_score), 2) AS avg_residual_score,
    MAX(residual_risk_score) AS max_residual_score
FROM risks
GROUP BY priority
ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END;

-- Query 2: Highest residual risks requiring management attention.
SELECT
    risk_id,
    risk_area,
    risk_owner,
    inherent_risk_score,
    residual_risk_score,
    control_effectiveness
FROM risks
WHERE residual_risk_score >= 12
ORDER BY residual_risk_score DESC, inherent_risk_score DESC, risk_id;

-- Query 3: Controls that cannot be fully evidenced.
SELECT
    control_id,
    control_area,
    severity,
    assessment_result,
    assessment_evidence_status,
    poam_id,
    poam_status,
    target_date
FROM v_assessment_poam_evidence
WHERE assessment_evidence_status <> 'Available'
ORDER BY CASE severity WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END, target_date;

-- Query 4: POA&M status and target-date monitoring as of the assessment cut-off.
SELECT
    poam_id,
    control_area,
    owner,
    priority,
    target_date,
    status,
    CAST(julianday(target_date) - julianday('2026-07-13') AS INTEGER) AS days_to_target
FROM poam
WHERE status <> 'Closed'
ORDER BY target_date, CASE priority WHEN 'High' THEN 1 ELSE 2 END;

-- Query 5: Remediation workload by owner and status.
SELECT
    owner,
    COUNT(*) AS action_count,
    SUM(CASE WHEN priority = 'High' THEN 1 ELSE 0 END) AS high_priority_actions,
    SUM(CASE WHEN status = 'Open' THEN 1 ELSE 0 END) AS open_actions,
    SUM(CASE WHEN status = 'In Progress' THEN 1 ELSE 0 END) AS in_progress_actions
FROM poam
GROUP BY owner
ORDER BY high_priority_actions DESC, action_count DESC, owner;

-- Query 6: Actions due within 60 days of the assessment cut-off.
SELECT
    poam_id,
    related_control_id,
    control_area,
    priority,
    target_date,
    status,
    evidence_required
FROM poam
WHERE date(target_date) BETWEEN date('2026-07-13') AND date('2026-07-13', '+60 days')
  AND status <> 'Closed'
ORDER BY target_date, poam_id;

-- Query 7: Full traceability from risk to control, finding, remediation, and evidence.
SELECT
    r.risk_id,
    r.risk_area,
    r.residual_risk_score,
    c.control_id,
    c.implementation_status,
    a.assessment_id,
    a.severity,
    p.poam_id,
    p.status AS poam_status,
    e.evidence_id,
    e.evidence_status
FROM risks AS r
JOIN controls AS c ON c.control_id = r.existing_control_id
JOIN assessments AS a ON a.control_id = c.control_id
JOIN poam AS p ON p.related_control_id = c.control_id
JOIN evidence_tracker AS e ON e.control_id = c.control_id
ORDER BY r.residual_risk_score DESC, r.risk_id;

-- Query 8: Compact management KPI output.
SELECT metric, value
FROM v_management_summary
ORDER BY metric;
