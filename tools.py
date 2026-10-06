import json
from pathlib import Path


BASE = Path(__file__).parent


def load_requirements():
    path = BASE / "knowledge" / "requirements.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_signals(text):
    text = text.lower()

    sensitive_terms = [
        "customer",
        "account information",
        "employee",
        "performance",
        "hr information",
        "security logs",
        "personal data",
        "confidential",
        "sensitive"
    ]

    decision_terms = [
        "promotion",
        "primary input",
        "automatically recommend",
        "automated decision",
        "approve",
        "reject"
    ]

    external_terms = [
        "third-party",
        "third party",
        "hosted llm",
        "external api",
        "vendor",
        "hosted model"
    ]

    review_terms = [
        "human review",
        "human support agent",
        "support agent will review",
        "security analysts will review",
        "analyst will review",
        "will review",
        "human oversight"
    ]

    return {
        "sensitive_data": any(x in text for x in sensitive_terms),
        "high_impact_decision": any(x in text for x in decision_terms),
        "third_party_ai": any(x in text for x in external_terms),
        "human_review": any(x in text for x in review_terms)
    }


def calculate_risk(signals):
    score = 20
    reasons = []

    if signals["sensitive_data"]:
        score += 20
        reasons.append("Sensitive information is involved.")

    if signals["high_impact_decision"]:
        score += 30
        reasons.append(
            "AI influences a high-impact business decision."
        )

    if signals["third_party_ai"]:
        score += 15
        reasons.append(
            "A third-party AI provider is involved."
        )

    if signals["human_review"]:
        score -= 10
        reasons.append(
            "Human review is explicitly present."
        )

    score = max(0, min(100, score))

    if score >= 80:
        level = "Critical"
    elif score >= 60:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return {
        "score": score,
        "level": level,
        "reasons": reasons
    }


def format_requirements(requirements):
    lines = []

    for item in requirements:
        lines.append(
            f"{item['id']} - {item['title']}: {item['text']}"
        )

    return "\n".join(lines)
