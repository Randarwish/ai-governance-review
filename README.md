# AI Governance Review

AI Governance Review is a small application for assessing AI use cases against a defined set of security and governance requirements.

The app combines deterministic risk scoring with Gemini-based contextual analysis.

## Workflow

```text
User scenario
      |
      v
Input validation
      |
      v
Basic PII redaction
      |
      v
Risk signal detection
      |
      v
Deterministic risk score
      |
      +---- Local governance requirements
      |
      v
Gemini assessment
      |
      v
Pydantic validation
      |
      v
Structured assessment
