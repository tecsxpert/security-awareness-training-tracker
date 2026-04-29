import re
import bleach

# Simple prompt injection patterns
INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"act as",
    r"bypass",
    r"override",
    r"jailbreak",
]

def sanitize_input(text: str) -> str:
    """Strip HTML and clean input"""
    return bleach.clean(text, tags=[], strip=True).strip()


def detect_prompt_injection(text: str) -> bool:
    """Detect basic prompt injection attempts"""
    text = text.lower()

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text):
            return True

    return False