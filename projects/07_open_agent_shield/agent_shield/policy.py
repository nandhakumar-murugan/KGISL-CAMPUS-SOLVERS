"""
Security Policy definitions and verdict enumerations for OpenAgentShield.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ActionVerdict(str, Enum):
    ALLOW = "ALLOW"
    BLOCK = "BLOCK"
    REDACT = "REDACT"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class RuleSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PolicyRule(BaseModel):
    rule_id: str
    name: str
    description: str
    severity: RuleSeverity
    verdict: ActionVerdict
    pattern: Optional[str] = None
    target_tools: List[str] = Field(default_factory=list)


class SecurityPolicy(BaseModel):
    policy_name: str = "Enterprise-Agent-Zero-Trust"
    version: str = "1.0.0"
    allow_unlisted_tools: bool = True
    enforce_secret_redaction: bool = True
    enforce_shell_sandboxing: bool = True
    blocked_commands: List[str] = Field(default_factory=lambda: [
        "rm -rf /",
        "rm -rf *",
        ":(){ :|:& };:",
        "mkfs",
        "dd if=",
        "shutdown",
        "reboot",
        "> /dev/sda",
        "chmod -R 777 /",
        "curl | sh",
        "curl | bash",
        "wget | sh",
        "wget | bash",
        "nc -e /bin/sh",
        "nc -e /bin/bash"
    ])
    blocked_patterns: List[str] = Field(default_factory=lambda: [
        r";\s*reboot",
        r";\s*shutdown",
        r"&&\s*rm\s+-rf",
        r"\|\s*bash",
        r"\|\s*sh",
        r"`.*`",
        r"\$\(.*\)"
    ])
    sensitive_file_patterns: List[str] = Field(default_factory=lambda: [
        r".*\.env$",
        r".*id_rsa.*",
        r".*\.ssh/.*",
        r".*/etc/shadow",
        r".*/etc/passwd",
        r".*\.aws/credentials.*"
    ])
    rules: List[PolicyRule] = Field(default_factory=list)

    @classmethod
    def default_strict_policy(cls) -> "SecurityPolicy":
        """Generates a hardened zero-trust policy ready for production AI agents."""
        return cls(
            policy_name="Strict-Production-Guard",
            allow_unlisted_tools=True,
            enforce_secret_redaction=True,
            enforce_shell_sandboxing=True,
            rules=[
                PolicyRule(
                    rule_id="RULE-001",
                    name="Block Destructive Root Commands",
                    description="Prevents AI agents from executing system wipe or kernel denial-of-service commands.",
                    severity=RuleSeverity.CRITICAL,
                    verdict=ActionVerdict.BLOCK,
                    target_tools=["run_command", "bash", "terminal", "execute_command", "adb_shell"]
                ),
                PolicyRule(
                    rule_id="RULE-002",
                    name="Prevent Credential File Read",
                    description="Blocks access to sensitive environment or private key files.",
                    severity=RuleSeverity.HIGH,
                    verdict=ActionVerdict.BLOCK,
                    target_tools=["read_file", "view_file", "cat", "fetch_file"]
                ),
                PolicyRule(
                    rule_id="RULE-003",
                    name="Require Confirmation for Mass Modifications",
                    description="Flags bulk deletion or destructive Git operations for human confirmation.",
                    severity=RuleSeverity.MEDIUM,
                    verdict=ActionVerdict.REQUIRE_APPROVAL,
                    target_tools=["git_push_force", "drop_database", "delete_all"]
                )
            ]
        )
