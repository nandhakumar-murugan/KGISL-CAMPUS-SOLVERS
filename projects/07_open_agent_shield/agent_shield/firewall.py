"""
AgentFirewall - The core runtime security gateway for autonomous AI agents.
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

from .policy import SecurityPolicy, ActionVerdict, RuleSeverity
from .sanitizer import SecretSanitizer
from .shell_guard import ShellGuard


class EvaluationResult(BaseModel):
    verdict: ActionVerdict
    tool_name: str
    risk_score: float = Field(ge=0.0, le=100.0, description="Risk score from 0.0 (safe) to 100.0 (critical)")
    reasons: List[str] = Field(default_factory=list)
    sanitized_arguments: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    event_hash: str = ""

    def is_safe(self) -> bool:
        return self.verdict in (ActionVerdict.ALLOW, ActionVerdict.REDACT)


class AgentFirewall:
    """Enterprise-grade firewall that intercepts and validates agent tool calls."""

    def __init__(self, policy: Optional[SecurityPolicy] = None):
        self.policy = policy or SecurityPolicy.default_strict_policy()
        self.shell_guard = ShellGuard(self.policy)
        self.audit_log: List[EvaluationResult] = []

    def inspect_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        caller_id: Optional[str] = "agent-primary"
    ) -> EvaluationResult:
        """Inspects an incoming tool invocation before execution.

        Args:
            tool_name: Name of the tool (e.g. 'run_command', 'write_file', 'launch_app').
            arguments: Dictionary of arguments provided by the AI agent.
            caller_id: Identifier of the calling agent session.

        Returns:
            EvaluationResult detailing whether the action is ALLOWED, BLOCKED, or REDACTED.
        """
        reasons: List[str] = []
        verdict = ActionVerdict.ALLOW
        risk_score = 0.0
        sanitized_args = dict(arguments)

        # 1. Shell / Command line validation
        if tool_name in ("run_command", "bash", "execute_command", "terminal", "adb_shell"):
            cmd = arguments.get("CommandLine") or arguments.get("command") or arguments.get("cmd") or ""
            if isinstance(cmd, str):
                v, reason, violations = self.shell_guard.inspect_command(cmd)
                if v == ActionVerdict.BLOCK:
                    verdict = ActionVerdict.BLOCK
                    risk_score = max(risk_score, 95.0)
                    reasons.extend(violations)
                elif violations:
                    risk_score = max(risk_score, 50.0)
                    reasons.extend(violations)

        # 2. Android ADB package sanitization (Artemis tool guard)
        if tool_name in ("launch_app", "stop_app", "terminate_app"):
            pkg = arguments.get("package_name") or arguments.get("package") or ""
            if isinstance(pkg, str):
                if not self.shell_guard.validate_android_package(pkg):
                    verdict = ActionVerdict.BLOCK
                    risk_score = 100.0
                    reasons.append(f"Invalid Android package name '{pkg}'. Possible command injection attempt.")

        # 3. Sensitive file access guard
        if tool_name in ("read_file", "view_file", "write_to_file", "replace_file_content"):
            target = (
                arguments.get("AbsolutePath")
                or arguments.get("TargetFile")
                or arguments.get("file_path")
                or arguments.get("path")
                or ""
            )
            if isinstance(target, str):
                for sensitive_pattern in self.policy.sensitive_file_patterns:
                    import re
                    if re.match(sensitive_pattern, target, re.IGNORECASE):
                        verdict = ActionVerdict.BLOCK
                        risk_score = 85.0
                        reasons.append(f"Access to sensitive file matching '{sensitive_pattern}' is prohibited")

        # 4. Secret & Credential Redaction
        if self.policy.enforce_secret_redaction:
            for key, val in arguments.items():
                if isinstance(val, str) and SecretSanitizer.contains_secrets(val):
                    redacted, detected_types = SecretSanitizer.scan_and_redact(val)
                    sanitized_args[key] = redacted
                    if verdict != ActionVerdict.BLOCK:
                        verdict = ActionVerdict.REDACT
                    reasons.append(f"Redacted sensitive credentials ({', '.join(detected_types)}) in argument '{key}'")
                    risk_score = max(risk_score, 30.0)

        # Build tamper-evident cryptographic hash of the evaluation event
        raw_hash_content = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}:{verdict.value}:{time.time()}"
        event_hash = hashlib.sha256(raw_hash_content.encode("utf-8")).hexdigest()

        result = EvaluationResult(
            verdict=verdict,
            tool_name=tool_name,
            risk_score=risk_score,
            reasons=reasons or ["Action complies with security policy"],
            sanitized_arguments=sanitized_args,
            event_hash=event_hash
        )

        self.audit_log.append(result)
        return result

    def get_audit_summary(self) -> Dict[str, Any]:
        """Returns statistics on intercepted agent tool executions."""
        total = len(self.audit_log)
        blocked = sum(1 for e in self.audit_log if e.verdict == ActionVerdict.BLOCK)
        redacted = sum(1 for e in self.audit_log if e.verdict == ActionVerdict.REDACT)
        allowed = sum(1 for e in self.audit_log if e.verdict == ActionVerdict.ALLOW)
        avg_risk = sum(e.risk_score for e in self.audit_log) / total if total > 0 else 0.0

        return {
            "total_inspected": total,
            "blocked_actions": blocked,
            "redacted_actions": redacted,
            "allowed_actions": allowed,
            "average_risk_score": round(avg_risk, 2)
        }
