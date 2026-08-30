# 🛡️ GovernX

### Automated NIST CSF 2.0 Compliance & Cyber Risk Quantification Engine

**Company:** AXLERO Innovating Solutions

**Team:**
- Harshal Ghatbandhe
- Ansh Gautam
- Mounika Dunna
- Sujal Waghmode
- Amrita
- Yannam Chittikumari



> **GovernX transforms technical cybersecurity telemetry into executive-level compliance insights and measurable financial risk.**

GovernX is an automated **Governance, Risk, and Compliance (GRC)** platform designed around the **NIST Cybersecurity Framework (CSF) 2.0**.

Instead of relying on static spreadsheets and manual compliance assessments, GovernX continuously analyzes security configurations, maps technical findings to NIST CSF 2.0 outcomes, evaluates organizational maturity, and translates critical security gaps into **quantified financial risk**.

The goal is simple:

**Turn cybersecurity data into business decisions.**

---

## 🚀 Why GovernX?

Modern organizations generate enormous amounts of security data across:

* ☁️ AWS / Azure
* 👤 Active Directory / IAM
* 💻 Endpoint Security
* 🔐 Identity & Access Management
* 🛡️ Security Controls
* 📋 Organizational Policies
* 🔎 Vulnerability Management Platforms

The problem is that this technical information rarely reaches business leadership in a meaningful form.

A security engineer may report:

> `MFA is disabled on a critical financial database.`

A CISO needs to communicate:

> **"This control gap exposes approximately $1.2M in potential annualized financial risk."**

GovernX acts as the bridge between these two worlds.

```text
Technical Telemetry
       ↓
Security Findings
       ↓
NIST CSF 2.0 Mapping
       ↓
Maturity Assessment
       ↓
Risk Quantification
       ↓
Financial Impact
       ↓
Executive Decision
```

---

# 🎯 Project Objectives

GovernX is designed to:

* Automate cybersecurity compliance monitoring
* Continuously collect cloud security configuration data
* Map technical controls to NIST CSF 2.0 outcomes
* Evaluate organizational cybersecurity maturity
* Identify compliance and security gaps
* Quantify cybersecurity risks financially
* Prioritize remediation based on business impact
* Generate board-ready compliance reports
* Provide executives with a simple cybersecurity risk posture

---

# 🧩 NIST CSF 2.0 Coverage

GovernX is built around the six core functions introduced by **NIST CSF 2.0**:

| Function        | Purpose                                                                |
| --------------- | ---------------------------------------------------------------------- |
| 🏛️ **GOVERN**  | Establish cybersecurity strategy, policies, roles, and risk management |
| 🔎 **IDENTIFY** | Understand assets, risks, dependencies, and organizational context     |
| 🛡️ **PROTECT** | Implement safeguards to reduce cybersecurity risk                      |
| 👁️ **DETECT**  | Discover and analyze cybersecurity events                              |
| 🚨 **RESPOND**  | Take action against detected cybersecurity incidents                   |
| ♻️ **RECOVER**  | Restore affected assets and operations                                 |

GovernX converts raw technical evidence into an organized representation of the organization's cybersecurity posture across these functions.

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │   Cloud Providers   │
                         │   AWS / Azure       │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Continuous          │
                         │ Integration Engine  │
                         │      Python         │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Security Findings   │
                         │ & Configuration     │
                         │ Evidence            │
                         └──────────┬──────────┘
                                    │
                  ┌─────────────────▼─────────────────┐
                  │       Framework Mapping Engine    │
                  │                                   │
                  │ Technical Control → NIST CSF 2.0 │
                  └─────────────────┬─────────────────┘
                                    │
                    ┌───────────────▼──────────────┐
                    │   Compliance & Maturity      │
                    │       Assessment Engine      │
                    └───────────────┬──────────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │         Financial Risk Engine           │
               │                                         │
               │ Monte Carlo Simulation                  │
               │ ALE / Loss Estimation                   │
               │ Value at Risk                           │
               └────────────────────┬────────────────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Executive Dashboard │
                         │       React         │
                         └──────────┬──────────┘
                                    │
               ┌────────────────────▼────────────────────┐
               │        CISO / Security Team / Board     │
               └─────────────────────────────────────────┘
```

---

# 🔥 Core Modules

## 1. ☁️ Continuous Integration Engine

The integration engine is responsible for collecting security configuration data from connected infrastructure.

### Initial capabilities

* AWS configuration auditing
* IAM policy analysis
* S3 security configuration
* Encryption checks
* Public exposure detection
* Open port detection
* Security group analysis
* Identity configuration analysis

### Technology

```text
Python
├── boto3
├── REST APIs
├── JSON
└── Scheduled Polling
```

The architecture is designed to support additional integrations such as:

```text
AWS
Azure
Active Directory
Endpoint Security
SIEM
IAM
Vulnerability Management
```

---

# 2. 🗺️ NIST CSF 2.0 Framework Mapping Engine

The mapping engine forms the core compliance intelligence layer.

It establishes relationships between:

```text
Technical Configuration
        ↓
Security Control
        ↓
NIST CSF 2.0 Outcome
        ↓
Compliance Status
        ↓
Risk
```

### Example

```text
AWS S3 Public Access
        ↓
Public Access Block
        ↓
Protect / Data Security
        ↓
Control Failed
        ↓
Compliance Gap
        ↓
Risk Calculation
```

A centralized mapping database allows GovernX to maintain relationships between technical controls and NIST CSF 2.0 outcomes.

Example structure:

| Technical Check      | Security Control      | NIST Function | Status |
| -------------------- | --------------------- | ------------- | ------ |
| S3 Public Access     | Public Access Block   | Protect       | ✅      |
| MFA Configuration    | Strong Authentication | Protect       | ❌      |
| Encryption at Rest   | Data Protection       | Protect       | ✅      |
| IAM Privileges       | Access Control        | Protect       | ⚠️     |
| Backup Configuration | Recovery Planning     | Recover       | ❌      |

---

# 3. 📊 Cybersecurity Maturity Scoring

GovernX evaluates the organization's cybersecurity maturity using the NIST CSF Tier model.

### Tier 1 — Partial

Limited awareness and inconsistent cybersecurity practices.

### Tier 2 — Risk Informed

Risk management practices exist but may not be organization-wide.

### Tier 3 — Repeatable

Formal, repeatable, and consistently implemented cybersecurity processes.

### Tier 4 — Adaptive

Highly mature, continuously improving, and adaptive cybersecurity practices.

GovernX calculates maturity scores using automated control assessment results.

```text
Control Results
      ↓
Function Scores
      ↓
Category Scores
      ↓
Overall Maturity
      ↓
Current Profile vs Target Profile
```

---

# 4. 💰 Financial Risk Quantifier

One of the key differentiators of GovernX is the ability to translate cybersecurity weaknesses into financial impact.

Instead of displaying only:

```text
CRITICAL VULNERABILITY
```

GovernX attempts to answer:

```text
What could this vulnerability cost the organization?
```

### Risk Model

The engine can incorporate:

* Asset value
* Threat probability
* Exposure
* Control effectiveness
* Potential loss magnitude
* Incident frequency
* Recovery cost
* Business impact

A simplified Annualized Loss Expectancy model can be represented as:

```text
ALE = SLE × ARO

SLE = Asset Value × Exposure Factor

ARO = Annual Rate of Occurrence
```

For more advanced analysis, GovernX uses **Monte Carlo simulation** to model uncertainty and generate a distribution of potential losses.

Example:

```text
Estimated Annual Loss
        ↓
$420K ─────────────── $1.2M ─────────────── $3.4M
        Low            Expected              High
```

This allows security teams to communicate risk using a language executives understand:

> **Cybersecurity Risk → Financial Exposure → Business Decision**

---

# 5. 📈 Executive Board Dashboard

The React-based dashboard provides a simplified view of organizational cybersecurity posture.

### Dashboard Components

```text
┌──────────────────────────────────────────────┐
│              GOVERNX EXECUTIVE               │
├──────────────────────────────────────────────┤
│                                              │
│  Security Score       Maturity Tier          │
│      78%                  Tier 3              │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│ GOVERN      ████████████████░░  82%          │
│ IDENTIFY    ███████████████░░░  76%          │
│ PROTECT     █████████████░░░░░  68%          │
│ DETECT      ████████████████░░  81%          │
│ RESPOND     ███████████████░░░  74%          │
│ RECOVER     ██████████████░░░░  71%          │
│                                              │
├──────────────────────────────────────────────┤
│                                              │
│ Critical Risk Exposure:     $1.2M            │
│ Open Critical Gaps:         07               │
│ Compliance Score:           76%              │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 🏛️ The Govern Function

NIST CSF 2.0 significantly expands the governance perspective of cybersecurity.

GovernX incorporates governance-oriented concepts such as:

* Cybersecurity strategy
* Organizational policies
* Roles and responsibilities
* Risk management strategy
* Supply-chain cybersecurity
* Organizational context
* Risk appetite
* Cybersecurity oversight

The objective is to connect:

```text
Business Strategy
       ↓
Cybersecurity Governance
       ↓
Policies
       ↓
Technical Controls
       ↓
Security Evidence
       ↓
Measured Risk
```

This creates a continuous connection between **board-level governance and technical security operations**.

---

# 🔄 Continuous Compliance Model

Traditional compliance:

```text
Audit
 ↓
Spreadsheet
 ↓
Manual Evidence
 ↓
Report
 ↓
Repeat Next Year
```

GovernX:

```text
Continuous Telemetry
        ↓
Automated Assessment
        ↓
Framework Mapping
        ↓
Risk Calculation
        ↓
Dashboard
        ↓
Remediation
        ↓
Continuous Reassessment
```

This transforms compliance from a periodic activity into a **continuous security process**.

---

# 🧪 Example Use Case

### Scenario

A critical financial database is accessible through an identity configuration where MFA is not enforced.

GovernX detects:

```text
Finding:
MFA Not Enabled

Asset:
Critical Financial Database

Severity:
CRITICAL

NIST Function:
PROTECT

Control:
Identity & Access Management
```

The financial risk engine then evaluates:

```text
Asset Value
       +
Threat Probability
       +
Exposure
       +
Potential Impact
       ↓
Monte Carlo Simulation
       ↓
Financial Risk Distribution
```

Example executive output:

```text
Estimated Value at Risk

$1.2M
```

The dashboard can then recommend:

```text
Priority: CRITICAL

Recommended Action:
Deploy centralized identity management
and enforce MFA across privileged and
critical-resource accounts.

Business Justification:
Reducing this control gap can materially
reduce the organization's estimated
financial exposure.
```

---

# 🗓️ Development Roadmap

## Week 1 — Data Ingestion & Dashboard Foundation

### Backend

* Build Python AWS integration
* Implement boto3 configuration checks
* Audit encryption settings
* Detect exposed resources
* Analyze IAM policies
* Store security findings

### Frontend

* Initialize React application
* Build dashboard structure
* Create six NIST CSF function cards
* Implement basic security posture visualization

---

## Week 2 — NIST Mapping & Maturity

### Backend

* Build NIST CSF 2.0 ontology
* Create framework mapping database
* Map AWS findings to CSF outcomes
* Implement control scoring
* Implement Tier 1–4 maturity logic

### Frontend

* Function-level maturity scores
* Current vs Target Profile
* Compliance gap visualization
* Control status indicators

---

## 🔎 Mid-Project Review

GovernX must demonstrate dynamic compliance detection.

### Test

Modify a mock AWS configuration:

```text
Before:
MFA = ENABLED
```

Change:

```text
MFA = DISABLED
```

GovernX should automatically:

```text
Detect Change
     ↓
Update Finding
     ↓
Fail Control
     ↓
Recalculate Score
     ↓
Downgrade NIST Category
     ↓
Update Dashboard
```

---

# Week 3 — Governance & Financial Risk

### Governance

Implement:

* Governance requirements
* Organizational policies
* Supply-chain risk relationships
* Risk ownership
* Technical-to-business control relationships

### Risk Engine

Implement:

* Asset valuation
* Exposure factor
* Threat probability
* SLE
* ARO
* ALE
* Monte Carlo simulation
* Value-at-Risk estimation

---

# Week 4 — Reporting & Finalization

### Reporting Engine

Generate automated reports containing:

* Executive summary
* NIST CSF 2.0 posture
* Maturity tier
* Critical security gaps
* Financial risk exposure
* Remediation priorities
* Risk reduction opportunities
* ROI-oriented recommendations

### Final UI

Focus on creating a common language between:

```text
Security Engineers
        ↕
       GovernX
        ↕
CISO / Risk Managers
        ↕
      Board
```

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

## Security & Infrastructure

```text
AWS
IAM
S3
Security Groups
Cloud APIs
NIST CSF 2.0
```

## Reporting

```text
Python PDF Generation
Automated Compliance Reports
Executive Risk Reports
```

---

# 📁 Proposed Project Structure

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
│   ├── mappings/
│   ├── compliance/
│   ├── risk_engine/
│   ├── models/
│   ├── reports/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── dashboards/
│   │   ├── charts/
│   │   └── services/
│   └── package.json
│
├── database/
│   ├── schema.sql
│   └── nist_mappings.sql
│
├── docs/
│   ├── architecture.md
│   ├── risk-model.md
│   └── nist-mapping.md
│
├── reports/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🔐 Security Considerations

GovernX is designed with security as a core requirement.

Key considerations include:

* Least-privilege AWS permissions
* Secure API credential management
* Environment-variable based secrets
* Input validation
* API authentication
* Audit logging
* Encryption of sensitive data
* Role-based dashboard access
* Secure database access
* Separation of collection and analysis layers

GovernX should never require unnecessary write permissions to monitored environments.

---

# 📊 Key Metrics

GovernX can provide organizations with measurable security indicators such as:

| Metric                 | Description                                 |
| ---------------------- | ------------------------------------------- |
| Security Posture Score | Overall security control score              |
| NIST Function Score    | Score for each CSF function                 |
| Maturity Tier          | Current organizational maturity             |
| Compliance Gap         | Difference between current and target state |
| Critical Findings      | High-priority security issues               |
| ALE                    | Annualized expected loss                    |
| Value at Risk          | Estimated financial exposure                |
| Risk Reduction         | Expected impact of remediation              |
| Control Coverage       | Percentage of mapped controls assessed      |

---

# 🎯 Expected Outcome

By the end of the project, GovernX should be capable of demonstrating:

```text
AWS Configuration
        ↓
Automated Security Check
        ↓
NIST CSF 2.0 Mapping
        ↓
Compliance Assessment
        ↓
Maturity Score
        ↓
Financial Risk Calculation
        ↓
Executive Dashboard
        ↓
Board-Ready Report
```

The final system demonstrates how modern organizations can move from:

**Manual Compliance → Automated Continuous Compliance**

and from:

**Technical Vulnerability → Quantified Business Risk**

---

# 💡 What Makes GovernX Different?

GovernX is not designed to be just another vulnerability scanner.

Its primary focus is the **relationship between cybersecurity, governance, compliance, and business risk**.

### Traditional Security Tool

```text
Finding:
MFA Disabled

Severity:
Critical
```

### GovernX

```text
Finding:
MFA Disabled

        ↓

NIST CSF Mapping:
PROTECT

        ↓

Maturity Impact:
-8%

        ↓

Business Impact:
Critical Identity Risk

        ↓

Financial Exposure:
$1.2M Estimated VaR

        ↓

Recommendation:
Implement centralized MFA

        ↓

Executive Decision:
Approve Identity Security Investment
```

That is the core vision of GovernX:

> **Make cybersecurity measurable in the language of business.**

---

# 🚀 Future Enhancements

Potential future versions can include:

* 🔹 Azure & GCP integrations
* 🔹 Microsoft Entra ID integration
* 🔹 Active Directory integration
* 🔹 SIEM integrations
* 🔹 CrowdStrike / SentinelOne integrations
* 🔹 Automated remediation
* 🔹 Policy-as-Code
* 🔹 Terraform integration
* 🔹 AI-assisted risk explanations
* 🔹 AI-generated executive summaries
* 🔹 Regulatory framework mapping
* 🔹 ISO 27001 mapping
* 🔹 SOC 2 mapping
* 🔹 CIS Controls mapping
* 🔹 GDPR compliance mapping
* 🔹 Multi-tenant enterprise architecture

---

# 🏆 Project Impact

GovernX demonstrates practical understanding of:

* Cybersecurity Governance
* NIST CSF 2.0
* Cloud Security
* Security Operations
* GRC
* Risk Management
* Compliance Automation
* Financial Risk Modeling
* Monte Carlo Simulation
* Python Automation
* REST APIs
* React Development
* Executive Security Reporting

---

# 👨‍💻 Project Vision

GovernX aims to build a bridge between **technical cybersecurity operations and executive decision-making**.

The platform answers three critical questions:

### 1. Where are we vulnerable?

**Automated security telemetry**

### 2. How does it affect our cybersecurity posture?

**NIST CSF 2.0 + maturity analysis**

### 3. Why should the business care?

**Quantified financial risk**

---

## ⭐ GovernX

**Automate Compliance. Quantify Risk. Empower Decisions.**

```text
┌─────────────────────────────────────────┐
│              G O V E R N X              │
│                                         │
│     Security → Compliance → Risk        │
│                                         │
│        Technical Data → Business        │
│             Intelligence               │
└─────────────────────────────────────────┘
```

### Built for the future of Cybersecurity Governance.

---
## Backend Local Development Setup

### Python Virtual Environment

From the `backend` directory, create and activate the virtual environment:

```bash
> python -m venv venv

EBS Encryption Check
Implemented the ebs_encryption AWS check using boto3.
Verifies whether EBS volumes have encryption enabled.
Added NIST CSF 2.0 mapping to PR.DS-01.
Added tests for encrypted and unencrypted EBS volumes.