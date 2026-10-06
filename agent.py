import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai

from guardrails import validate, redact_pii
from models import Assessment
from tools import (
    load_requirements,
    get_signals,
    calculate_risk,
    format_requirements
)


load_dotenv()


def get_client():
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    return genai.Client(api_key=key)


def clean_json(text):
    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def call_gemini(prompt):
    client = get_client()

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    last_error = None

    for attempt in range(3):
        try:
            result = client.interactions.create(
                model=model,
                input=prompt
            )

            if result.output_text:
                return result.output_text

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(3 * (attempt + 1))

    raise RuntimeError(
        f"Gemini request failed: {last_error}"
    )


def analyze(scenario):
    validate(scenario)

    safe_text = redact_pii(scenario)

    signals = get_signals(safe_text)
    risk = calculate_risk(signals)

    requirements = load_requirements()

    prompt = f"""
You are reviewing an AI use case for security and governance.

Scenario:
{safe_text}

Detected signals:
{json.dumps(signals)}

Application risk score:
{risk["score"]}/100

Application risk level:
{risk["level"]}

Governance requirements:
{format_requirements(requirements)}

Assess all eight requirements.

Rules:
- Base evidence only on the scenario.
- Do not assume controls exist when they are not mentioned.
- Missing information should normally be Review Required.
- Use Gap when the scenario clearly conflicts with a requirement.
- Use Compliant only when there is supporting evidence.
- Use Not Applicable only when the requirement clearly does not apply.
- Do not change the supplied risk score or level.
- Recommendations should be short and practical.
- Do not expose private chain-of-thought.
- Return JSON only.

Return exactly this structure:

{{
  "use_case_type": "short classification",
  "risk_level": "{risk['level']}",
  "risk_score": {risk['score']},
  "confidence": 0.90,
  "summary": "short executive summary",
  "requirements": [
    {{
      "requirement_id": "AI-001",
      "title": "Business Ownership",
      "status": "Review Required",
      "evidence": "short evidence",
      "recommendation": "short recommendation"
    }}
  ],
  "risks": ["risk"],
  "actions": ["action"]
}}

Return all AI-001 through AI-008.
"""

    output = call_gemini(prompt)

    try:
        data = json.loads(
            clean_json(output)
        )
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned an invalid JSON response."
        )

    data["risk_score"] = risk["score"]
    data["risk_level"] = risk["level"]

    result = Assessment(**data)

    trace = [
        "Validated user input",
        "Redacted basic PII",
        f"Detected scenario signals: {signals}",
        "Loaded AI-001 through AI-008",
        f"Calculated risk: {risk['score']}/100 ({risk['level']})",
        "Sent sanitized evidence to Gemini",
        "Validated Gemini response with Pydantic"
    ]

    return result, trace
