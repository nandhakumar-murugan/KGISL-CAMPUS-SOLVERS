"""
Shell Guard and Command Injection Analyzer.
Safeguards operating system execution boundaries, adb bridges, and terminal tool invocations.
"""

import re
import shlex
from typing import Tuple, List, Optional
from .policy import SecurityPolicy, ActionVerdict


class ShellGuard:
    """Performs static syntax and AST-style safety inspection on commands before execution."""

    ANDROID_PACKAGE_REGEX = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+$")

    DANGEROUS_BINARIES = {
        "mkfs", "fdisk", "parted", "dd", "shutdown", "reboot", "poweroff", "init",
        "format", "del /f /s /q c:\\", "chkdsk"
    }

    def __init__(self, policy: Optional[SecurityPolicy] = None):
        self.policy = policy or SecurityPolicy.default_strict_policy()

    def inspect_command(self, cmd_string: str) -> Tuple[ActionVerdict, str, List[str]]:
        """Analyzes a terminal command string for injection risks or destructive payloads.

        Returns:
            Tuple of (ActionVerdict, reason_message, list_of_detected_violations)
        """
        if not cmd_string or not cmd_string.strip():
            return ActionVerdict.ALLOW, "Empty command allowed", []

        violations: List[str] = []
        normalized_cmd = cmd_string.strip()

        # 1. Exact or substring match on blocked destructive commands
        for blocked in self.policy.blocked_commands:
            if blocked.lower() in normalized_cmd.lower():
                violations.append(f"Blocked explicit dangerous command pattern: '{blocked}'")

        # 2. Regex-based command injection detection (chained execution, subshells, piping to interpreters)
        for pattern in self.policy.blocked_patterns:
            if re.search(pattern, normalized_cmd, re.IGNORECASE):
                violations.append(f"Command injection risk detected matching pattern: '{pattern}'")

        # 3. Tokenize command to check base binary
        try:
            tokens = shlex.split(normalized_cmd, posix=True)
            if tokens:
                base_binary = tokens[0].lower().split("/")[-1].split("\\")[-1]
                if base_binary in self.DANGEROUS_BINARIES:
                    violations.append(f"Execution of dangerous system binary '{base_binary}' is restricted")

                # Check for recursive root rm
                if base_binary == "rm" and ("-rf" in tokens or "-fr" in tokens):
                    for t in tokens[1:]:
                        if t in ("/", "/*", "*", "~", "$HOME"):
                            violations.append(f"High-risk filesystem deletion targeting root/home: '{t}'")
        except ValueError:
            # Unbalanced quotation marks often signify injection tricks
            violations.append("Malformed command syntax or unbalanced quotation marks detected")

        if violations:
            return ActionVerdict.BLOCK, "Command execution denied by security policy", violations

        return ActionVerdict.ALLOW, "Command cleared security policy checks", []

    def validate_android_package(self, package_name: str) -> bool:
        """Validates package name against Android's standard reverse-domain naming grammar.
        Mitigates ADB command injection vulnerabilities (e.g. Google Artemis Issue #55).
        """
        if not package_name or not isinstance(package_name, str):
            return False
        return bool(self.ANDROID_PACKAGE_REGEX.match(package_name.strip()))

    def sanitize_url_argument(self, url: str) -> str:
        """Safely quotes a URL parameter to prevent shell breakout characters."""
        return shlex.quote(url.strip())
