/**
 * Content model for the NIST CSF 2.0 informational page.
 *
 * Terminology follows the official CSF 2.0 structure: the six Functions,
 * the CSF Core (Functions > Categories > Subcategories), Organizational
 * Profiles and Implementation Tiers. Function/category codes below are the
 * official NIST identifiers; prose is editorial summarisation, not quoted
 * normative text.
 */

export const NIST_FUNCTIONS = [
  {
    id: 'govern',
    code: 'GV',
    name: 'Govern',
    color: '#34d399',
    summary:
      'Establish and monitor cybersecurity risk management strategy, expectations and policies.',
    purpose:
      'Govern addresses how an organisation leads and governs cybersecurity risk management. It establishes the strategy, policies, roles, accountability and organisational context that every other Function depends on.',
    activities: [
      'Understand the organisation’s mission, scope and cybersecurity risk context',
      'Establish and maintain a cybersecurity risk management strategy',
      'Define and enforce cybersecurity policies and roles',
      'Assess cybersecurity risk on a recurring, defined cadence',
      'Manage cybersecurity risk introduced through suppliers and partners',
    ],
    outcome:
      'Cybersecurity decisions are traceable to business objectives, with named owners and documented risk appetite.',
    governX:
      'Govern-X records governance responses as auditable evidence and scores the Govern Function continuously, so policy maturity is measured rather than asserted.',
  },
  {
    id: 'identify',
    code: 'ID',
    name: 'Identify',
    color: '#38bdf8',
    summary: 'Understand the organization’s assets, risks, dependencies and cybersecurity context.',
    purpose:
      'Identify builds the understanding required to manage cybersecurity risk. It covers assets, software, data, business environments, supply chains and the threats and vulnerabilities that apply.',
    activities: [
      'Maintain inventories of hardware, software, data and services',
      'Catalogue business environment and critical service dependencies',
      'Identify and assess threats, vulnerabilities and likelihoods of occurrence',
      'Monitor the supply chain for assets and services the organisation relies on',
    ],
    outcome:
      'The organisation knows what it owns, what depends on what, and where its exposure actually sits.',
    governX:
      'The Identify collector enumerates AWS assets and maps findings to Identify outcomes so the asset inventory is evidence-backed.',
  },
  {
    id: 'protect',
    code: 'PR',
    name: 'Protect',
    color: '#10b981',
    summary: 'Implement safeguards to manage cybersecurity risks.',
    purpose:
      'Protect covers the safeguards an organisation puts in place to manage cybersecurity risk, including identity, access, encryption, secure development, configuration and protective technology.',
    activities: [
      'Manage identities, credentials and access controls',
      'Raise workforce cybersecurity awareness and capability',
      'Protect data at rest, in transit and in use',
      'Apply secure baselines and vulnerability management to platforms',
      'Operate logging, backups and protective network technology',
    ],
    outcome:
      'Controls that reduce the likelihood and impact of attack are applied consistently and verifiably.',
    governX:
      'Encryption, access-block and configuration checks run continuously and report PASS/FAIL per resource against Protect outcomes.',
  },
  {
    id: 'detect',
    code: 'DE',
    name: 'Detect',
    color: '#a78bfa',
    summary: 'Find and analyze possible cybersecurity attacks and compromises.',
    purpose:
      'Detect identifies potential cybersecurity attacks and compromises. It covers analytics and monitoring, adverse event analysis, and validating the effectiveness of detection processes.',
    activities: [
      'Monitor networks, endpoints and workloads continuously',
      'Analyse telemetry for indicators of malicious activity',
      'Correlate events and validate detection coverage',
      'Test and refine detection rules and thresholds',
    ],
    outcome:
      'Compromise is detected quickly and with enough fidelity to respond proportionately.',
    governX:
      'Govern-X exposes detected control gaps as findings with severity, so detection output becomes a prioritised work queue.',
  },
  {
    id: 'respond',
    code: 'RS',
    name: 'Respond',
    color: '#f87171',
    summary: 'Take action regarding detected cybersecurity incidents.',
    purpose:
      'Respond covers the means to respond to a confirmed or suspected cybersecurity incident, including analysis, containment, eradication, communication and incident response planning.',
    activities: [
      'Execute and refine the incident response plan',
      'Contain the incident to prevent further spread',
      'Eradicate the adversary and restore a clean state',
      'Coordinate legal, regulatory and customer communications',
      'Document and review lessons after every incident',
    ],
    outcome:
      'Incidents are contained and resolved through a rehearsed process with clear decision authority.',
    governX:
      'Respond-scoped findings carry severity and resource detail, giving responders the evidence needed to triage quickly.',
  },
  {
    id: 'recover',
    code: 'RC',
    name: 'Recover',
    color: '#fbbf24',
    summary: 'Restore affected assets, operations and capabilities after cybersecurity incidents.',
    purpose:
      'Recover covers restoring assets and operations after an incident, including recovery planning, verification that service is restored, and updates to recovery capabilities.',
    activities: [
      'Maintain and test a recovery plan for critical services',
      'Verify restored assets are operating correctly and securely',
      'Update recovery plans and capabilities after real incidents',
      'Track lessons learned to prevent recurrence',
    ],
    outcome:
      'Critical services return to a known-good state within tested recovery objectives.',
    governX:
      'Recover outcomes stay continuously scored so resilience is demonstrated before an incident, not during one.',
  },
];

export const FUNCTION_IDS = NIST_FUNCTIONS.map((fn) => fn.id);

export const WHY_NIST = [
  {
    id: 'risk',
    title: 'Risk Management',
    body: 'Understand and prioritize cybersecurity risks in the language the business already uses for risk.',
  },
  {
    id: 'improvement',
    title: 'Security Improvement',
    body: 'Identify the gap between the current and the desired security posture, and work that gap deliberately.',
  },
  {
    id: 'language',
    title: 'Common Language',
    body: 'Give technical teams, management and leadership one shared vocabulary for discussing cyber posture.',
  },
  {
    id: 'governance',
    title: 'Governance',
    body: 'Connect cybersecurity decisions directly to organisational objectives, accountability and risk tolerance.',
  },
  {
    id: 'continuity',
    title: 'Continuous Improvement',
    body: 'Evaluate capability on a recurring cycle so posture compounds instead of decaying.',
  },
];

export const CSF_2_CHANGES = [
  {
    id: 'govern-function',
    index: '01',
    title: 'Govern Function',
    body:
      'The most significant structural addition. Govern makes explicit that leadership and accountability for cybersecurity risk are part of the framework itself, not a separate concern. Cybersecurity risk management strategy, policy, roles, risk assessment and supply chain risk all sit inside the Core.',
    emphasis: 'Structural addition',
  },
  {
    id: 'applicability',
    index: '02',
    title: 'Broader Applicability',
    body:
      'CSF 2.0 is written for organisations of different sizes, sectors and maturity levels, and for organisations of varying risk exposure and resource constraints.',
    emphasis: 'Sector and size agnostic',
  },
  {
    id: 'governance-risk',
    index: '03',
    title: 'Stronger Governance & Risk Management',
    body:
      'The Framework places greater emphasis on organisational context, supply chain considerations and explicit cybersecurity risk management, treating these as first-class concerns rather than peripheral ones.',
    emphasis: 'Governance emphasis',
  },
  {
    id: 'profiles',
    index: '04',
    title: 'Improved Profiles & Implementation Guidance',
    body:
      'Organizational Profiles are expressed as Current and Target profiles, which make gap analysis between actual and desired posture an explicit, structured step rather than an informal judgement.',
    emphasis: 'Profiles & Tiers',
  },
];

export const CSF_EVOLUTION = {
  from: 'CSF 1.1',
  to: 'CSF 2.0',
  rows: [
    {
      aspect: 'Structure',
      v1: 'Five Functions: Identify, Protect, Detect, Respond, Recover',
      v2: 'Six Functions: Govern, Identify, Protect, Detect, Respond, Recover',
    },
    {
      aspect: 'Governance',
      v1: 'Not a Function; governance treated largely as external context',
      v2: 'Govern is a Function in its own right, within the CSF Core',
    },
    {
      aspect: 'Application',
      v1: 'Strongly oriented to critical infrastructure and operations',
      v2: 'Applies to any organisation regardless of sector, size or maturity',
    },
    {
      aspect: 'Risk framing',
      v1: 'Focused on security outcomes alongside business outcomes',
      v2: 'Framed explicitly around managing cybersecurity risk',
    },
    {
      aspect: 'Profiles',
      v1: 'Informal and lightly defined',
      v2: 'Formalised as Current Profile, Target Profile and gap analysis',
    },
    {
      aspect: 'Tiers',
      v1: 'Tiered characteristics of risk management practice',
      v2: 'Implementation Tiers describing the rigor of those practices',
    },
  ],
  note:
    'CSF 2.0 evolves the Framework rather than discarding it. The five original Functions, the Core structure and the tiered characteristics of risk management all carry forward; Govern is added and the framing is explicitly rebuilt around cybersecurity risk management for a broader audience.',
};

export const CORE_HIERARCHY = [
  {
    level: 'Core',
    title: 'CSF Core',
    body:
      'The set of cybersecurity outcomes that the Framework is built around, organised under the six Functions. The Core is what an organisation assesses itself against.',
  },
  {
    level: 'Functions',
    title: 'Functions',
    body:
      'The six groupings of cybersecurity outcomes — Govern, Identify, Protect, Detect, Respond, Recover — that organise the Core.',
  },
  {
    level: 'Categories',
    title: 'Categories',
    body:
      'Groupings of related outcomes within a Function. Each Category belongs to exactly one Function and carries a code such as GV.OC or PR.AA.',
  },
  {
    level: 'Subcategories',
    title: 'Subcategories',
    body:
      'The specific, detailed cybersecurity outcomes an organisation evaluates to assess and improve its practices. These are the measurable unit of implementation.',
  },
];

export const GOVERN_EXAMPLE_HIERARCHY = [
  {
    code: 'GV',
    level: 'Function',
    title: 'Govern',
  },
  {
    code: 'GV.OC',
    level: 'Category',
    title: 'Organizational Context',
  },
  {
    code: 'GV.OC-01',
    level: 'Category Example',
    title:
      'Understanding of the organisation’s mission, scope, and cybersecurity risk context is documented and reviewed',
  },
  {
    code: 'GV.OC-02',
    level: 'Category Example',
    title:
      'Legal, regulatory and contractual requirements relevant to the organisation are understood and applied',
  },
  {
    code: 'GV.OC-03',
    level: 'Category Example',
    title:
      'Business environment, relationships and dependencies are documented and used to inform risk assessment',
  },
];

export const PROFILES_STAGES = [
  {
    id: 'current',
    label: 'Current Profile',
    question: 'What is our cybersecurity posture today?',
    body:
      'The outcomes the organisation has achieved right now, evidenced by the controls and telemetry actually in place. This is the baseline every gap analysis starts from.',
  },
  {
    id: 'gap',
    label: 'Gap Analysis',
    question: 'Where are we short of the target?',
    body:
      'A structured comparison of the Current Profile against the Target Profile, showing which outcomes are absent, partial or unevidenced — and why that matters.',
  },
  {
    id: 'target',
    label: 'Target Profile',
    question: 'What outcomes do we want to achieve?',
    body:
      'The outcomes the organisation has committed to. A good Target Profile is selected deliberately against risk tolerance, business needs and the resources available.',
  },
  {
    id: 'improve',
    label: 'Improvement',
    question: 'What do we do about the gap first?',
    body:
      'Gaps are prioritised by business need and risk rather than implementation convenience, so effort lands where it changes the risk position most.',
  },
];

export const IMPLEMENTATION_TIERS = [
  {
    tier: 1,
    name: 'Partial',
    color: '#f87171',
    body:
      'Risk management practices are limited and may be reactive. Cybersecurity risk is addressed inconsistently and often only after an incident.',
  },
  {
    tier: 2,
    name: 'Risk Informed',
    color: '#fbbf24',
    body:
      'Risk awareness exists, but practices may not be organisation-wide or consistently implemented. Some processes are documented without being followed uniformly.',
  },
  {
    tier: 3,
    name: 'Repeatable',
    color: '#38bdf8',
    body:
      'Risk management practices are formally established and consistently implemented. Cybersecurity is treated as an ongoing organisational process with defined ownership.',
  },
  {
    tier: 4,
    name: 'Adaptive',
    color: '#34d399',
    body:
      'The organisation continuously adapts cybersecurity practices based on lessons learned and changing threats, using maturity data to drive decision-making.',
  },
];

export const TIER_CAVEAT =
  'Tiers describe the rigor, formality and consistency of cybersecurity risk governance and management practices. A Tier placement is not a security score, and reaching a higher Tier is not a guarantee of security — it reflects the maturity of the management system, not the absence of vulnerabilities.';

export const PROCESS_STEPS = [
  {
    id: 1,
    title: 'Understand Organization',
    body: 'Establish mission, scope, context and the risk appetite that frame every later decision.',
  },
  {
    id: 2,
    title: 'Identify Cybersecurity Risks',
    body: 'Surface assets, dependencies, threats and vulnerabilities that the organisation actually faces.',
  },
  {
    id: 3,
    title: 'Assess Current Posture',
    body: 'Gather evidence and build the Current Profile across the six Functions.',
  },
  {
    id: 4,
    title: 'Define Target Outcomes',
    body: 'Select the outcomes the organisation commits to, forming the Target Profile.',
  },
  {
    id: 5,
    title: 'Identify Gaps',
    body: 'Compare Current against Target to expose absent, partial and unevidenced outcomes.',
  },
  {
    id: 6,
    title: 'Prioritize Improvements',
    body: 'Sequence remediation by business need and risk, not by ease of implementation.',
  },
  {
    id: 7,
    title: 'Continuously Monitor & Improve',
    body: 'Re-assess as conditions change, and close the loop by updating Profiles and Tiers.',
  },
];

export const GOVERN_X_FLOW = [
  { id: 'cloud', label: 'AWS / Cloud', kind: 'input' },
  { id: 'identity', label: 'Identity & Access', kind: 'input' },
  { id: 'endpoints', label: 'Endpoints', kind: 'input' },
  { id: 'telemetry', label: 'Security Telemetry', kind: 'input' },
  { id: 'governx', label: 'GOVERN-X', kind: 'core' },
  { id: 'mapping', label: 'NIST CSF 2.0 Mapping', kind: 'stage' },
  { id: 'maturity', label: 'Maturity Assessment', kind: 'stage' },
  { id: 'gap', label: 'Gap Analysis', kind: 'stage' },
  { id: 'risk', label: 'Cyber Risk Quantification', kind: 'stage' },
  { id: 'exec', label: 'Executive Decision Support', kind: 'outcome' },
];

export const GOVERN_X_CAPABILITIES = [
  {
    id: 'assessment',
    title: 'Automated Assessment',
    body: 'Collects and evaluates security information from connected infrastructure or mock/live integrations, removing the manual evidence-gathering step.',
  },
  {
    id: 'mapping',
    title: 'NIST Mapping',
    body: 'Maps security findings and organisational information to relevant NIST CSF 2.0 Functions, Categories and outcomes.',
  },
  {
    id: 'maturity',
    title: 'Maturity Assessment',
    body: 'Evaluates cybersecurity posture and places each Function against the Implementation Tiers.',
  },
  {
    id: 'gaps',
    title: 'Gap Identification',
    body: 'Identifies where the current state does not meet the desired security posture, and quantifies the distance.',
  },
  {
    id: 'financial',
    title: 'Financial Risk',
    body: 'Translates cybersecurity exposure into understandable financial risk indicators such as potential Value at Risk.',
  },
  {
    id: 'governance',
    title: 'Governance',
    body: 'Connects security decisions with policies, organisational context, risk tolerance and business objectives.',
  },
  {
    id: 'visibility',
    title: 'Executive Visibility',
    body: 'Presents technical findings in a format suitable for security teams, managers and CISO or board-level discussion.',
  },
];

export const WORKFLOW_LAYERS = [
  { id: 'org', label: 'ORGANIZATION', kind: 'source' },
  { id: 'telemetry', label: 'SECURITY TELEMETRY', kind: 'source' },
  { id: 'governx', label: 'GOVERN-X', kind: 'core' },
  { id: 'mapping', label: 'NIST MAPPING', kind: 'engine' },
  { id: 'risk', label: 'RISK ENGINE', kind: 'engine' },
  { id: 'maturity', label: 'MATURITY', kind: 'engine' },
  { id: 'gap', label: 'GAP ANALYSIS', kind: 'engine' },
  { id: 'recommendations', label: 'RECOMMENDATIONS', kind: 'outcome' },
  { id: 'decisions', label: 'EXECUTIVE DECISIONS', kind: 'outcome' },
];

export const RISK_STORY = {
  finding: 'Multi-factor authentication is missing for a critical financial database.',
  stages: [
    {
      id: 'technical',
      label: 'Technical Finding',
      body: 'Identity control check returns FAIL on a production financial database resource.',
    },
    {
      id: 'mapping',
      label: 'NIST CSF 2.0 Mapping',
      body: 'Mapped to Protect — access control outcomes, with the gap recorded against the Identify asset context.',
    },
    {
      id: 'risk',
      label: 'Risk Assessment',
      body: 'Rated by severity and asset criticality, elevating it into the prioritised remediation queue.',
    },
    {
      id: 'maturity',
      label: 'Maturity Impact',
      body: 'Lowers the Protect Function score and pulls the organisation’s overall Tier assessment down.',
    },
    {
      id: 'financial',
      label: 'Financial Exposure',
      body: 'Translated into a potential Value at Risk figure for executive review.',
    },
    {
      id: 'action',
      label: 'Recommended Action',
      body: 'Enforce MFA on the affected resource and re-run the scan to verify the outcome closes.',
    },
  ],
  valueAtRisk: '$1.2M',
  disclaimer:
    'Illustrative example data only. This figure is produced for demonstration and is not an actual financial prediction, valuation or guarantee of loss.',
};

export const COMPARISON = {
  traditional: {
    title: 'Traditional Approach',
    items: [
      'Spreadsheet-based assessment',
      'Manual evidence collection',
      'Static compliance reports',
      'Separate technical and business risk views',
      'Difficult continuous monitoring',
    ],
  },
  governX: {
    title: 'Govern-X',
    items: [
      'Automated evidence collection',
      'Continuous assessment capability',
      'NIST CSF 2.0 mapping',
      'Maturity analysis',
      'Gap identification',
      'Financial risk quantification',
      'Executive dashboard',
    ],
  },
};

export const FAQ_ITEMS = [
  {
    q: 'What is NIST CSF 2.0?',
    a: 'NIST CSF 2.0 is a cybersecurity risk management framework published by the National Institute of Standards and Technology. It gives organisations a common structure for understanding, assessing and improving their cybersecurity posture across six Functions: Govern, Identify, Protect, Detect, Respond and Recover.',
  },
  {
    q: 'Is NIST CSF 2.0 a cybersecurity certification?',
    a: 'No. NIST CSF is a voluntary framework for managing cybersecurity risk, not a certification and not a regulatory mandate. It is not mandatory for any organisation, though some sectors, customers or regulators may reference it in their own requirements.',
  },
  {
    q: 'What are the six NIST CSF 2.0 Functions?',
    a: 'The six Functions are Govern, Identify, Protect, Detect, Respond and Recover. They are not a strict linear process — an organisation may apply them in an order that fits its context, and they are intended to interact rather than proceed sequentially.',
  },
  {
    q: 'What is the Govern Function?',
    a: 'Govern is the Function added in CSF 2.0. It covers establishing and monitoring cybersecurity risk management strategy, policies, roles and accountability, organisational context, risk assessment and supply chain risk. It was introduced so that leadership and governance sit inside the framework rather than around it.',
  },
  {
    q: 'What are CSF Profiles?',
    a: 'An Organizational Profile captures the cybersecurity outcomes an organisation has achieved. A Current Profile reflects posture today, a Target Profile reflects desired outcomes, and comparing them produces a gap analysis that drives prioritised improvement.',
  },
  {
    q: 'What are CSF Tiers?',
    a: 'The four Implementation Tiers — Partial, Risk Informed, Repeatable and Adaptive — describe the rigor and consistency of an organisation’s cybersecurity risk governance and management practices. They are not security scores and do not guarantee a level of security.',
  },
  {
    q: 'How does NIST CSF 2.0 help organisations?',
    a: 'It gives a structured way to assess current posture, define desired outcomes, identify the gap between them, and prioritise improvements based on business need and risk. That gives cybersecurity investment a defensible rationale and a measurable trajectory.',
  },
  {
    q: 'How does Govern-X use NIST CSF 2.0?',
    a: 'Govern-X operationalises the Framework. It collects security findings, maps them to the six Functions, scores maturity by Function and Tier, identifies gaps, and translates the resulting exposure into financial risk indicators for executive decision-making.',
  },
  {
    q: 'Does Govern-X replace cybersecurity teams?',
    a: 'No. Govern-X reduces the manual evidence-collection and reporting burden so security teams can focus on judgement and remediation. It does not replace qualified cybersecurity professionals or the governance decisions they make.',
  },
  {
    q: 'Can NIST CSF 2.0 be used by small organisations?',
    a: 'Yes. CSF 2.0 is explicitly applicable to organisations of different sizes, sectors and maturity levels, and to organisations with varying risk exposure and resource constraints. A small organisation can implement the Functions proportionally without attempting Tier 4 outright.',
  },
];