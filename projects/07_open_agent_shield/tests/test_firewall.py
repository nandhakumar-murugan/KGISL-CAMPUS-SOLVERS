"""
Comprehensive Unit Tests for OpenAgentShield.
Validates zero-trust evaluation, command injection mitigation, secret redaction, and MCP protection.
"""

import pytest
import os
import sys

# Ensure agent_shield can be imported regardless of execution working directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent_shield import (
    AgentFirewall,
    ActionVerdict,
    SecretSanitizer,
    ShellGuard,
    MCPInterceptor
)
from agent_shield.mcp_interceptor import SecurityInterceptionError


@pytest.fixture
def firewall():
    return AgentFirewall()


def test_benign_command_allowed(firewall):
    result = firewall.inspect_tool_call("run_command", {"CommandLine": "python --version"})
    assert result.verdict == ActionVerdict.ALLOW
    assert result.is_safe()
    assert result.risk_score == 0.0


def test_destructive_rm_blocked(firewall):
    result = firewall.inspect_tool_call("run_command", {"CommandLine": "rm -rf / --no-preserve-root"})
    assert result.verdict == ActionVerdict.BLOCK
    assert not result.is_safe()
    assert result.risk_score >= 90.0
    assert any("dangerous" in r.lower() or "deletion" in r.lower() for r in result.reasons)


def test_command_injection_chained_blocked(firewall):
    result = firewall.inspect_tool_call("run_command", {"CommandLine": "echo hello; reboot"})
    assert result.verdict == ActionVerdict.BLOCK
    assert any("injection" in r.lower() or "reboot" in r.lower() for r in result.reasons)


def test_adb_package_injection_blocked(firewall):
    # Tests vulnerability pattern from Google Artemis Issue #55
    malicious_pkg = "com.android.settings; reboot"
    result = firewall.inspect_tool_call("launch_app", {"package_name": malicious_pkg})
    assert result.verdict == ActionVerdict.BLOCK
    assert "Invalid Android package name" in result.reasons[0]

    valid_pkg = "com.android.settings"
    valid_res = firewall.inspect_tool_call("launch_app", {"package_name": valid_pkg})
    assert valid_res.verdict == ActionVerdict.ALLOW


def test_sensitive_env_file_blocked(firewall):
    result = firewall.inspect_tool_call("read_file", {"AbsolutePath": "/root/app/.env"})
    assert result.verdict == ActionVerdict.BLOCK
    assert any(".env" in r for r in result.reasons)


def test_secret_redaction(firewall):
    sample_text = "Logging in with token ghp_1234567890abcdefghijklmnopqrstuvwx and key AIzaSyD9x8y7Z6w5V4u3T2s1R0qP_fakeKey123"
    result = firewall.inspect_tool_call("write_to_file", {
        "TargetFile": "/tmp/notes.txt",
        "CodeContent": sample_text
    })
    assert result.verdict == ActionVerdict.REDACT
    sanitized = result.sanitized_arguments["CodeContent"]
    assert "ghp_" not in sanitized
    assert "AIzaSy" not in sanitized
    assert "[REDACTED:GITHUB_TOKEN]" in sanitized
    assert "[REDACTED:GOOGLE_API_KEY]" in sanitized


def test_mcp_interceptor_sync_decorator(firewall):
    interceptor = MCPInterceptor(firewall)

    @interceptor.protect_tool("run_command")
    def execute_terminal(CommandLine: str) -> str:
        return f"Executed: {CommandLine}"

    # Safe call should succeed
    res = execute_terminal(CommandLine="ls -la")
    assert "Executed: ls -la" in res

    # Blocked call should raise SecurityInterceptionError
    with pytest.raises(SecurityInterceptionError):
        execute_terminal(CommandLine="rm -rf /")


def test_mcp_interceptor_async_decorator(firewall):
    import asyncio
    interceptor = MCPInterceptor(firewall)

    @interceptor.protect_tool("read_file")
    async def fetch_code(AbsolutePath: str) -> str:
        return f"Content of {AbsolutePath}"

    safe_res = asyncio.run(fetch_code(AbsolutePath="/app/main.py"))
    assert "main.py" in safe_res

    with pytest.raises(SecurityInterceptionError):
        asyncio.run(fetch_code(AbsolutePath="/app/.env"))


def test_audit_summary_metrics(firewall):
    firewall.inspect_tool_call("run_command", {"CommandLine": "ls"})
    firewall.inspect_tool_call("run_command", {"CommandLine": "rm -rf *"})
    
    summary = firewall.get_audit_summary()
    assert summary["total_inspected"] >= 2
    assert summary["blocked_actions"] >= 1
    assert summary["allowed_actions"] >= 1
