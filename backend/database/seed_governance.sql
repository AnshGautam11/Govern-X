-- GovernX Week 3 Day 1
-- Initial governance questionnaire questions

INSERT OR IGNORE INTO governance_questions
    (question_key, question_text, csf_category)
VALUES
    (
        'risk_owner_assigned',
        'Is a cybersecurity risk owner assigned at the leadership level?',
        'GV.RR'
    ),
    (
        'security_policy_reviewed',
        'Has the organizational security policy been established and reviewed periodically?',
        'GV.PO'
    ),
    (
        'incident_response_plan_exists',
        'Does the organization have an incident response plan?',
        'GV.OV'
    ),
    (
        'third_party_risk_reviewed',
        'Is third-party and supply-chain cybersecurity risk reviewed?',
        'GV.SC'
    );