import re


MAX_LENGTH = 5000


def validate(text):
    if not text or not text.strip():
        raise ValueError("Please enter a scenario.")

    if len(text) > MAX_LENGTH:
        raise ValueError("Scenario is too long.")

    blocked = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "reveal system prompt",
        "show hidden instructions",
        "bypass the rules",
        "jailbreak"
    ]

    value = text.lower()

    for phrase in blocked:
        if phrase in value:
            raise ValueError("Possible prompt injection detected.")


def redact_pii(text):
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    )

    phone_pattern = (
        r"(?<!\w)"
        r"(?:\+?\d{1,3}[\s-]?)?"
        r"(?:\(?\d{2,4}\)?[\s-]?)?"
        r"\d{3,4}[\s-]?\d{3,4}"
        r"(?!\w)"
    )

    text = re.sub(
        email_pattern,
        "[REDACTED_EMAIL]",
        text
    )

    text = re.sub(
        phone_pattern,
        "[REDACTED_PHONE]",
        text
    )

    return text
