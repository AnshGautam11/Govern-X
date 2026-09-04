# 🛡️ GovernX

## Automated NIST CSF 2.0 Compliance & Cyber Risk Quantification Engine

**Company:** AXLERO Innovating Solutions

**Team**

* Harshal Ghatbandhe
* Ansh Gautam
* Mounika Dunna
* Sujal Waghmode
* Amrita
* Yannam Chittikumari

> **GovernX transforms cloud security telemetry into continuous NIST CSF 2.0 compliance insights, cybersecurity maturity scores, and measurable financial risk.**

---

# 🚀 Overview

GovernX is an automated **Governance, Risk, and Compliance (GRC)** platform designed around the **NIST Cybersecurity Framework (CSF) 2.0**.

Traditional compliance programs often depend on spreadsheets, manually collected evidence, periodic audits, and disconnected security tools.

GovernX follows a continuous approach:

```text
Cloud / Security Telemetry
          ↓
Automated Security Checks
          ↓
Security Findings
          ↓
NIST CSF 2.0 Mapping
          ↓
Compliance Assessment
          ↓
Maturity Analysis
          ↓
Cyber Risk Quantification
          ↓
Financial Risk Estimation
          ↓
Executive Dashboard
          ↓
Remediation & Continuous Reassessment
```

The core objective is to create a bridge between:

**Technical Security Data → Compliance → Risk → Business Decisions**

---

# 🎯 Core Vision

GovernX answers three fundamental questions:

### 1. Where are we vulnerable?

Automated security configuration and control assessment.

### 2. How does the weakness affect our cybersecurity posture?

NIST CSF 2.0 control mapping and maturity analysis.

### 3. Why should the business care?

Financial risk estimation and executive-level business impact.

---

# 💡 Why GovernX?

A traditional security tool may report:

```text
Finding:
MFA Disabled

Severity:
Critical
```

GovernX expands the finding into a business-oriented risk story:

```text
MFA Disabled
      ↓
Identity & Access Control Gap
      ↓
NIST CSF 2.0 Mapping
      ↓
Compliance Impact
      ↓
Maturity Impact
      ↓
Asset Exposure
      ↓
Financial Risk Estimation
      ↓
Recommended Remediation
```

This enables security teams to communicate technical issues using a language that executives and risk owners can understand.

---

# 🏛️ NIST CSF 2.0 Coverage

GovernX is structured around the six functions of NIST CSF 2.0.

| Function     | GovernX Focus                                                        |
| ------------ | -------------------------------------------------------------------- |
| **GOVERN**   | Policies, roles, strategy, risk ownership and organizational context |
| **IDENTIFY** | Assets, dependencies, risks and business context                     |
| **PROTECT**  | Access control, encryption, identity and security safeguards         |
| **DETECT**   | Security events, configuration anomalies and monitoring              |
| **RESPOND**  | Incident response and security remediation                           |
| **RECOVER**  | Backup, recovery planning and restoration capabilities               |

The platform converts technical evidence into an organized representation of the organization's cybersecurity posture.

---

# 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │   AWS / Cloud Data   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Cloud Integration    │
                         │ & Polling Engine     │
                         │       Python         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Security Check       │
                         │ Registry             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Security Findings    │
                         │ PASS / FAIL / WARN   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ NIST CSF 2.0 Mapping Engine  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Compliance & Maturity Engine  │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Cyber Risk Quantification     │
                    │ SLE / ARO / ALE / VaR         │
                    │ Monte Carlo Simulation        │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ Backend REST API              │
                    │ Flask / FastAPI               │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │ React Executive Dashboard     │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                 ┌─────────────────────────────────────┐
                 │ CISO / Security Team / Risk / Board │
                 └─────────────────────────────────────┘
```

---

# 🔄 End-to-End Data Flow

GovernX follows a complete backend-to-frontend workflow.

```text
AWS Resource
     ↓
boto3 Collector
     ↓
Compliance Check
     ↓
Finding Generated
     ↓
NIST Mapping
     ↓
Compliance Score
     ↓
Risk Calculation
     ↓
Database Persistence
     ↓
REST API
     ↓
React Frontend
     ↓
Dashboard Visualization
```

The frontend is designed to consume **real backend API responses rather than static mock values**.

This allows changes in the monitored environment to propagate through the complete system.

---

# ☁️ Cloud Integration Engine

The cloud integration engine provides automated security configuration assessment.

## Current AWS capabilities

GovernX includes checks for:

* S3 encryption at rest
* EBS encryption
* IAM configuration
* Public resource exposure
* Security groups
* Open ports
* Identity configuration
* Additional AWS security controls

The architecture uses:

```text
Python
 ├── boto3
 ├── REST APIs
 ├── JSON
 ├── Scheduled Polling
 └── Modular Check Registry
```

The modular design allows additional cloud and security integrations to be added without redesigning the entire system.

---

# 🔐 AWS Security Check Framework

GovernX uses a shared AWS compliance-check registry.

Conceptually:

```text
AWS Resource
      ↓
Registered Check
      ↓
Security Evaluation
      ↓
Finding
      ↓
NIST Mapping
      ↓
Risk
```

Each check should provide:

```text
Check ID
Resource Type
Security Control
Status
Severity
Evidence
Description
Remediation
NIST Mapping
```

Example:

```json
{
  "check": "ebs_encryption",
  "resource": "vol-123456",
  "status": "FAIL",
  "severity": "HIGH",
  "control": "Encryption at Rest",
  "nist_function": "PROTECT",
  "nist_category": "PR.DS-01"
}
```

---

# 🔒 Encryption Checks

## S3 Encryption at Rest

The `s3_encryption_at_rest` check verifies whether S3 buckets have server-side encryption configured.

The check:

* Identifies S3 buckets
* Inspects encryption configuration
* Produces resource-level findings
* Handles AWS API errors
* Produces PASS/FAIL results
* Maps findings to NIST CSF 2.0

### NIST Mapping

```text
S3 Encryption
      ↓
Data Security
      ↓
PR.DS-01
```

---

# 💾 EBS Encryption

The `ebs_encryption` check evaluates EBS volumes to determine whether encryption at rest is enabled.

Capabilities include:

* `describe_volumes` based assessment
* Pagination support
* Per-volume findings
* Encrypted/un-encrypted detection
* AWS error handling
* PASS/FAIL reporting
* NIST CSF 2.0 mapping

### NIST Mapping

```text
EBS Encryption
      ↓
Data Security
      ↓
PR.DS-01
```

---

# 🧪 Mock AWS Verification

GovernX supports local testing through a **Moto-backed mock AWS environment**.

This is important because security checks can be validated without:

* Real AWS credentials
* Production resources
* Real cloud infrastructure
* Unnecessary AWS costs

The verification environment creates compliant and non-compliant resources and confirms that GovernX correctly identifies their security posture.

Example:

```text
Mock AWS
   │
   ├── Encrypted S3 Bucket
   │       ↓
   │      PASS
   │
   ├── Unencrypted S3 Bucket
   │       ↓
   │      FAIL
   │
   ├── Encrypted EBS Volume
   │       ↓
   │      PASS
   │
   └── Unencrypted EBS Volume
           ↓
          FAIL
```

Run:

```bash
cd backend
python verify_day4.py
```

---

# 🗺️ NIST CSF 2.0 Mapping Engine

The mapping engine establishes the relationship between technical findings and cybersecurity framework outcomes.

```text
Technical Finding
       ↓
Security Control
       ↓
NIST CSF Function
       ↓
NIST Category / Subcategory
       ↓
Compliance Status
       ↓
Risk Impact
```

Example:

| Technical Finding       | Control               | NIST Mapping | Result |
| ----------------------- | --------------------- | ------------ | ------ |
| S3 Public Access        | Public Access Block   | Protect      | FAIL   |
| MFA Disabled            | Strong Authentication | Protect      | FAIL   |
| S3 Encryption Disabled  | Data Encryption       | PR.DS-01     | FAIL   |
| EBS Encryption Disabled | Data Encryption       | PR.DS-01     | FAIL   |
| Backup Missing          | Recovery Control      | Recover      | FAIL   |

---

# 📊 Compliance Engine

GovernX calculates compliance posture from individual control results.

```text
Individual Checks
       ↓
Control Results
       ↓
NIST Categories
       ↓
NIST Functions
       ↓
Overall Compliance Score
```

Possible statuses:

```text
PASS
FAIL
WARNING
NOT_ASSESSED
```

This allows the dashboard to distinguish between:

* Fully compliant controls
* Failed controls
* Partially implemented controls
* Controls that have not yet been assessed

---

# 📈 Cybersecurity Maturity

GovernX evaluates organizational maturity using the NIST CSF Tier model.

### Tier 1 — Partial

Cybersecurity practices are limited or inconsistent.

### Tier 2 — Risk Informed

Security decisions consider organizational risk but may not be consistently applied.

### Tier 3 — Repeatable

Formal and repeatable cybersecurity processes are established.

### Tier 4 — Adaptive

The organization continuously improves its cybersecurity capabilities using lessons learned and changing threat intelligence.

GovernX derives maturity insights from:

```text
Control Performance
       ↓
Function Scores
       ↓
Category Scores
       ↓
Current Profile
       ↓
Target Profile
       ↓
Maturity Gap
```

---

# 💰 Cyber Risk Quantification

One of GovernX's major differentiators is its ability to translate security weaknesses into estimated financial exposure.

Instead of:

```text
CRITICAL
```

GovernX attempts to communicate:

```text
Potential Financial Impact
```

---

# 📐 Risk Model

GovernX can incorporate:

* Asset value
* Exposure factor
* Threat probability
* Control effectiveness
* Incident frequency
* Potential loss
* Recovery cost
* Business impact

A simplified model:

```text
SLE = Asset Value × Exposure Factor

ALE = SLE × ARO
```

Where:

```text
SLE = Single Loss Expectancy
ARO = Annual Rate of Occurrence
ALE = Annualized Loss Expectancy
```

---

# 🎲 Monte Carlo Risk Simulation

Cybersecurity risk contains uncertainty.

GovernX can model this uncertainty using Monte Carlo simulation.

```text
Input Variables
      ↓
Probability Distributions
      ↓
Thousands of Simulations
      ↓
Loss Distribution
      ↓
Percentiles
      ↓
Risk Estimate
```

Example:

```text
Potential Annual Loss

$420K ───────── $1.2M ───────── $3.4M
 Low             Expected         High
```

This provides a more useful risk representation than a single deterministic number.

---

# 📉 Risk Reduction Analysis

GovernX can compare the organization's risk posture before and after remediation.

```text
Current Risk
     ↓
Apply Remediation
     ↓
Recalculate Controls
     ↓
Recalculate Risk
     ↓
Risk Reduction
```

Example:

```text
Before Remediation:
$1.2M Estimated Exposure

After MFA Enforcement:
$430K Estimated Exposure

Potential Risk Reduction:
$770K
```

This can help organizations evaluate the business value of security investments.

---

# 🏛️ Governance Layer

GovernX extends beyond technical cloud security.

The governance layer can represent:

* Cybersecurity strategy
* Policies
* Risk ownership
* Roles and responsibilities
* Risk appetite
* Organizational context
* Supply-chain cybersecurity
* Governance oversight

The intended relationship is:

```text
Business Strategy
       ↓
Cybersecurity Governance
       ↓
Policies
       ↓
Security Controls
       ↓
Technical Evidence
       ↓
Measured Risk
```

---

# 📊 Executive Dashboard

The React dashboard provides an executive-level representation of security posture.

### Key dashboard metrics

```text
┌───────────────────────────────────────────────┐
│                  GOVERNX                      │
├───────────────────────────────────────────────┤
│                                               │
│ Security Score        Maturity Tier           │
│      78%                  Tier 3               │
│                                               │
├───────────────────────────────────────────────┤
│                                               │
│ GOVERN       ████████████████░░  82%          │
│ IDENTIFY     ███████████████░░░  76%          │
│ PROTECT      █████████████░░░░░  68%          │
│ DETECT       ████████████████░░  81%          │
│ RESPOND      ███████████████░░░  74%          │
│ RECOVER      ██████████████░░░░  71%          │
│                                               │
├───────────────────────────────────────────────┤
│                                               │
│ Critical Risk Exposure       $1.2M             │
│ Open Critical Findings      07                │
│ Compliance Score             76%              │
│                                               │
└───────────────────────────────────────────────┘
```

The dashboard should obtain these values from backend APIs so that the UI reflects actual assessment results.

---

# 🔌 Frontend–Backend Integration

GovernX follows an API-driven architecture.

```text
React Frontend
      │
      │ HTTP / REST
      ▼
Flask / FastAPI Backend
      │
      ▼
Compliance Services
      │
      ├── AWS Collector
      ├── Security Checks
      ├── NIST Mapping
      ├── Maturity Engine
      └── Risk Engine
      │
      ▼
Database
```

The frontend should not independently calculate or hard-code core compliance results.

Instead:

```text
Backend = Source of Truth
Frontend = Visualization Layer
```

This ensures that dashboard values represent actual backend assessment results.

---

# 🔄 Dynamic Assessment Example

Suppose a mock AWS environment initially contains:

```text
EBS Encryption = ENABLED
```

GovernX returns:

```text
PASS
```

Now change the resource:

```text
EBS Encryption = DISABLED
```

The expected flow is:

```text
Configuration Change
        ↓
AWS Collector
        ↓
EBS Encryption Check
        ↓
FAIL
        ↓
Finding Updated
        ↓
NIST Mapping Updated
        ↓
Compliance Score Recalculated
        ↓
Risk Recalculated
        ↓
API Response Updated
        ↓
React Dashboard Updated
```

This demonstrates that GovernX is a **working compliance engine rather than a static dashboard or UI mockup**.

---

# 🧪 Testing Strategy

GovernX uses automated testing to validate backend behavior.

Testing should cover:

### Unit Tests

```text
Individual security checks
Risk calculations
Mapping logic
Scoring logic
```

### Integration Tests

```text
AWS Collector
      ↓
Security Checks
      ↓
NIST Mapping
      ↓
API
```

### Mock Cloud Tests

```text
Moto AWS Environment
      ↓
Create Test Resources
      ↓
Run Security Checks
      ↓
Verify PASS / FAIL
```

### API Tests

Validate:

* HTTP status codes
* Response schemas
* Invalid input handling
* Error responses
* Database interactions
* Assessment endpoints

Run backend tests using:

```bash
pytest -v
```

A successful test run provides confidence that the backend implementation remains functional as new modules are added.

---

# 🛡️ Security Architecture

GovernX follows security-by-design principles.

### Least Privilege

AWS integrations should use only the permissions required for security assessment.

### Secret Management

Credentials should never be hard-coded.

Use:

```text
Environment Variables
Secret Managers
Secure Configuration
```

### API Security

Recommended controls include:

* Authentication
* Authorization
* Input validation
* Request validation
* Rate limiting
* Secure error handling

### Audit Logging

Important events should be logged:

```text
User
Action
Timestamp
Resource
Result
```

---

# 🗄️ Data Persistence

GovernX should maintain persistent records for:

```text
Organizations
Assets
Security Findings
Controls
NIST Mappings
Assessment Results
Risk Calculations
Remediation Status
Audit Events
```

Example relationship:

```text
Organization
     │
     ├── Assets
     │
     ├── Findings
     │      ↓
     │   Controls
     │      ↓
     │   NIST Mapping
     │
     ├── Risk Assessments
     │
     └── Remediation Records
```

This makes the platform suitable for historical trend analysis rather than only showing the current state.

---

# 📋 Reporting Engine

GovernX can generate automated reports containing:

### Executive Summary

High-level cybersecurity posture.

### NIST CSF 2.0 Assessment

Function and category-level results.

### Maturity Assessment

Current and target maturity.

### Critical Findings

High-priority security gaps.

### Financial Risk

ALE, estimated loss distribution and Value-at-Risk.

### Remediation Priorities

Actions ranked according to business impact.

### Risk Reduction

Estimated improvement after remediation.

---

# 📅 Development Roadmap

## Week 1 — Cloud Integration & Dashboard Foundation

### Backend

* AWS integration
* boto3 collectors
* S3 security checks
* EBS security checks
* Encryption validation
* IAM analysis
* Public exposure detection
* Security group analysis
* Finding persistence

### Frontend

* React dashboard
* NIST function cards
* Security score
* Finding overview
* API service layer

---

# Week 2 — NIST Mapping & Maturity

### Backend

* NIST CSF 2.0 mapping database
* Technical-control relationships
* Control scoring
* Function-level scoring
* Maturity calculation
* Current vs target profile

### Frontend

* NIST function visualization
* Compliance gaps
* Control status
* Maturity visualization
* Target profile comparison

---

# Mid-Project Validation

GovernX must demonstrate dynamic behavior.

Example:

```text
MFA ENABLED
     ↓
PASS
     ↓
Good Compliance Score
```

Change:

```text
MFA DISABLED
     ↓
FAIL
     ↓
Compliance Gap
     ↓
Risk Increase
     ↓
Dashboard Update
```

---

# Week 3 — Governance & Financial Risk

### Governance

* Governance controls
* Risk ownership
* Policies
* Supply-chain relationships
* Organizational context

### Risk Engine

* Asset valuation
* Exposure factor
* Threat probability
* SLE
* ARO
* ALE
* Monte Carlo simulation
* Risk distribution
* VaR estimation
* Risk reduction

---

# Week 4 — Reporting & Finalization

### Reporting

* Executive report
* NIST posture report
* Maturity report
* Risk report
* Remediation report
* Business impact analysis

### Finalization

* Frontend/backend integration
* API validation
* Database validation
* Automated testing
* Error handling
* Security hardening
* UI polishing
* Documentation
* Final demonstration

---

# 🛠️ Technology Stack

## Backend

```text
Python
Flask / FastAPI
boto3
REST APIs
SQLite / PostgreSQL
Pandas
NumPy
Scikit-learn
Monte Carlo Simulation
```

## Frontend

```text
React.js
JavaScript / TypeScript
HTML5
CSS3
Chart.js / Recharts
```

## Cloud & Security

```text
AWS
IAM
S3
EBS
Security Groups
Cloud APIs
NIST CSF 2.0
```

## Testing

```text
pytest
Moto
API Integration Tests
Unit Tests
```

## Reporting

```text
Python PDF Generation
Automated Compliance Reports
Executive Risk Reports
```

---

# 📁 Project Structure

```text
GovernX/
│
├── backend/
│   ├── app.py
│   ├── config/
│   ├── integrations/
│   │   ├── aws/
│   │   └── azure/
│   │
│   ├── collectors/
│   ├── checks/
│   ├── mappings/
│   ├── compliance/
│   ├── risk_engine/
│   ├── models/
│   ├── api/
│   ├── reports/
│   ├── tests/
│   └── verify_day4.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── dashboards/
│   │   ├── charts/
│   │   ├── services/
│   │   └── hooks/
│   │
│   └── package.json
│
├── database/
│   ├── schema.sql
│   └── nist_mappings.sql
│
├── docs/
│   ├── architecture.md
│   ├── risk-model.md
│   ├── nist-mapping.md
│   └── api.md
│
├── reports/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 📊 Key Metrics

| Metric                 | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| Security Posture Score | Overall security control performance                      |
| NIST Function Score    | Score for each CSF function                               |
| Compliance Score       | Percentage of compliant assessed controls                 |
| Maturity Tier          | Current organizational maturity                           |
| Compliance Gap         | Difference between current and target state               |
| Critical Findings      | High-priority security issues                             |
| Control Coverage       | Percentage of controls assessed                           |
| ALE                    | Expected annualized loss                                  |
| VaR                    | Estimated financial exposure at selected confidence level |
| Risk Reduction         | Expected reduction after remediation                      |

---

# 🔥 Example End-to-End Scenario

## Initial State

```text
Financial AWS Environment

S3 Encryption       PASS
EBS Encryption      FAIL
MFA                  FAIL
Security Groups     PASS
Backup              FAIL
```

GovernX processes these findings:

```text
AWS Telemetry
      ↓
Security Checks
      ↓
5 Control Results
      ↓
NIST CSF Mapping
      ↓
Compliance Score
      ↓
Maturity Analysis
      ↓
Financial Risk
```

Dashboard:

```text
Compliance Score:        68%

Maturity:                Tier 2

Critical Findings:       3

Estimated Risk:          $1.2M

Highest Risk Area:
Identity & Data Protection
```

GovernX then generates:

```text
Priority 1
Enforce MFA

Priority 2
Enable EBS encryption

Priority 3
Implement recovery controls
```

After remediation:

```text
Compliance Score:
68% → 89%

Risk:
$1.2M → $430K

Maturity:
Tier 2 → Tier 3
```

The platform therefore demonstrates measurable security improvement.

---

# 🔄 Traditional Compliance vs GovernX

| Traditional Compliance        | GovernX                       |
| ----------------------------- | ----------------------------- |
| Periodic audits               | Continuous assessment         |
| Manual spreadsheets           | Automated evidence            |
| Static reports                | Dynamic dashboard             |
| Technical findings            | Business risk                 |
| Qualitative severity          | Quantified financial exposure |
| Manual framework mapping      | Automated NIST mapping        |
| Limited historical visibility | Persistent assessment history |
| Audit-focused                 | Risk-focused                  |
| Security-centric              | Business + security-centric   |

---

# 🎯 Expected Final Demonstration

The final GovernX demonstration should show the complete lifecycle:

```text
1. Launch Backend
        ↓
2. Launch Frontend
        ↓
3. Connect to Mock AWS
        ↓
4. Run Security Assessment
        ↓
5. Detect Configuration
        ↓
6. Generate Findings
        ↓
7. Map Findings to NIST CSF 2.0
        ↓
8. Calculate Compliance Score
        ↓
9. Calculate Maturity
        ↓
10. Quantify Financial Risk
        ↓
11. Display Results in React
        ↓
12. Change Cloud Configuration
        ↓
13. Re-run Assessment
        ↓
14. Observe Updated Risk & Compliance
        ↓
15. Generate Executive Report
```

This proves that GovernX is an integrated cybersecurity platform rather than a collection of independent modules.

---

# 🏆 What Makes GovernX Different?

GovernX is not intended to be another vulnerability scanner.

Its primary focus is the relationship between:

```text
Cybersecurity
      +
Governance
      +
Compliance
      +
Risk
      +
Business Impact
```

A conventional tool may say:

```text
MFA Disabled
Severity: Critical
```

GovernX aims to provide:

```text
MFA Disabled
      ↓
Identity Control Gap
      ↓
NIST CSF 2.0 Mapping
      ↓
Compliance Impact
      ↓
Maturity Impact
      ↓
Asset Exposure
      ↓
Financial Risk
      ↓
Remediation Recommendation
      ↓
Risk Reduction
      ↓
Executive Decision
```

---

# 🚀 Future Enhancements

Potential future versions include:

* Azure integration
* GCP integration
* Microsoft Entra ID
* Active Directory
* SIEM integrations
* CrowdStrike integration
* SentinelOne integration
* Automated remediation
* Policy-as-Code
* Terraform integration
* AI-assisted risk explanations
* AI-generated executive summaries
* ISO 27001 mapping
* SOC 2 mapping
* CIS Controls mapping
* GDPR mapping
* Multi-tenant enterprise architecture
* Role-based access control
* Security trend analytics
* Historical risk forecasting

---

# 🔐 Security Principles

GovernX follows the following design principles:

```text
Least Privilege
       +
Secure Secrets
       +
Input Validation
       +
Authentication
       +
Authorization
       +
Audit Logging
       +
Secure APIs
       +
Encrypted Data
       +
Separation of Duties
```

GovernX should remain **read-only wherever possible** when assessing monitored cloud environments.

---

# 📌 Current Implementation Status

### Week 1 Cloud Polling

The initial AWS cloud-polling implementation has been finalized and locally verified.

### Completed

* AWS boto3 integration
* Shared AWS check registry
* S3 encryption-at-rest check
* EBS encryption check
* Per-resource findings
* PASS/FAIL assessment
* AWS error handling
* Pagination support for EBS volume discovery
* NIST CSF 2.0 mapping
* Moto-backed mock AWS validation
* Automated test coverage

### Verified Checks

```text
s3_encryption_at_rest
        ↓
PR.DS-01

ebs_encryption
        ↓
PR.DS-01
```

### Verification

The checks were tested against compliant and non-compliant mock AWS resources.

```text
Compliant Resource
       ↓
PASS

Non-Compliant Resource
       ↓
FAIL
```

No real AWS credentials are required for local verification.

---

# 🧪 Backend Development Setup

From the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run automated tests:

```bash
pytest -v
```

Run AWS encryption verification:

```bash
python verify_day4.py
```

---

# 🌐 Running the Application

### Backend

Start the API server using the project's configured application entry point.

For an ASGI application:

```bash
uvicorn app:app --reload
```

For Flask:

```bash
python app.py
```

### Frontend

From the frontend directory:

```bash
npm install
npm run dev
```

The frontend communicates with the backend through REST APIs.

---

# 🎯 Final Project Outcome

GovernX demonstrates a complete transformation:

```text
                    GOVERNX

Technical Telemetry
        ↓
Security Assessment
        ↓
NIST CSF 2.0
        ↓
Compliance
        ↓
Maturity
        ↓
Risk Quantification
        ↓
Financial Impact
        ↓
Remediation
        ↓
Executive Decision
```

The platform demonstrates practical implementation of:

* Cybersecurity Governance
* NIST CSF 2.0
* Cloud Security
* AWS Security Assessment
* GRC
* Compliance Automation
* Risk Management
* Financial Risk Modeling
* Monte Carlo Simulation
* Python Automation
* REST APIs
* React
* Database Persistence
* Automated Testing
* Executive Security Reporting

---

# ⭐ GovernX

> **Automate Compliance. Quantify Risk. Empower Decisions.**

```text
┌─────────────────────────────────────────────┐
│                  G O V E R N X              │
│                                             │
│       SECURITY → COMPLIANCE → RISK          │
│                                             │
│       TECHNICAL DATA → BUSINESS             │
│             INTELLIGENCE                    │
└─────────────────────────────────────────────┘
```

### Built for the future of Cybersecurity Governance.

**Technical Data → Security Intelligence → Business Decisions**
