"""
Secret sanitizer and PII redactor for Agent interactions.
Protects sensitive developer and infrastructure credentials from leaking into LLM logs or tool returns.
"""

import re
from typing import Tuple, List, Dict


class SecretSanitizer:
    """Detects and redacts secrets, API keys, tokens, and sensitive infrastructure patterns."""

    PATTERNS: Dict[str, re.Pattern] = {
        "Google API Key": re.compile(r"AIza[0-9A-Za-z-_]{35}"),
        "OpenAI API Key": re.compile(r"sk-[a-zA-Z0-9T3BlbkFJ]{20,}"),
        "Anthropic API Key": re.compile(r"sk-ant-[a-zA-Z0-9-_]{32,}"),
        "GitHub Token": re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,255}"),
        "GitHub Fine-Grained Token": re.compile(r"github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}"),
        "AWS Access Key": re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
        "Generic Bearer Token": re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}", re.IGNORECASE),
        "RSA Private Key": re.compile(r"-----BEGIN (?:RSA )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA )?PRIVATE KEY-----"),
        "Password in URI": re.compile(r"://([^:\s]+):([^@\s]+)@")
    }

    @classmethod
    def scan_and_redact(cls, text: str) -> Tuple[str, List[str]]:
        """Scans input text and replaces any detected sensitive token with [REDACTED:<TYPE>].

        Returns:
            Tuple of (redacted_text, list_of_detected_types)
        """
        if not text or not isinstance(text, str):
            return text, []

        detected: List[str] = []
        sanitized_text = text

        for name, pattern in cls.PATTERNS.items():
            matches = list(pattern.finditer(sanitized_text))
            if matches:
                detected.append(name)
                # Redact from end to start to maintain string slice indexes
                for m in reversed(matches):
                    replacement = f"[REDACTED:{name.upper().replace(' ', '_')}]"
                    sanitized_text = sanitized_text[:m.start()] + replacement + sanitized_text[m.end():]

        return sanitized_text, detected

    @classmethod
    def contains_secrets(cls, text: str) -> bool:
        """Quick boolean test if text contains known sensitive credential formats."""
        if not text or not isinstance(text, str):
            return False
        return any(pattern.search(text) is not None for pattern in cls.PATTERNS.values())
