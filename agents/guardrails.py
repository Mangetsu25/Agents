import re


class Guardrails:
    """Simple guardrails for PII/PHI and basic content safety."""

    EMAIL_RE = re.compile(r"[\w.-]+@[\w.-]+")
    PHONE_RE = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")

    def is_safe(self, text: str) -> bool:
        if self.EMAIL_RE.search(text) or self.PHONE_RE.search(text):
            return False
        lower = text.lower()
        if any(term in lower for term in ["suicide", "self-harm"]):
            return False
        return True


__all__ = ["Guardrails"]
