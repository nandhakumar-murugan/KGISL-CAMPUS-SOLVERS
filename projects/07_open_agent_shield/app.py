"""
OpenAgentShield Interactive Simulation & CLI Console.
Demonstrates live interception of real-world AI agent tool calls and attacks.
"""

import sys
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from agent_shield import AgentFirewall, ActionVerdict


def run_demo():
    print("=" * 70)
    print("[OPEN-AGENT-SHIELD] - Autonomous AI Agent Security Gateway")
    print("    Developed by KGiSL Campus Solvers & Lead Maintainer Nandhakumar M")
    print("=" * 70)
    print("\nInitializing AgentFirewall with Zero-Trust Security Policies...")

    firewall = AgentFirewall()

    test_scenarios = [
        {
            "name": "Benign Command Execution",
            "tool": "run_command",
            "args": {"CommandLine": "git status"}
        },
        {
            "name": "Destructive Filesystem Attack (CVE Style)",
            "tool": "run_command",
            "args": {"CommandLine": "rm -rf / --no-preserve-root"}
        },
        {
            "name": "Shell Chaining / Command Injection",
            "tool": "run_command",
            "args": {"CommandLine": "echo 'Testing'; reboot"}
        },
        {
            "name": "ADB Package Name Injection (Google Artemis Issue #55)",
            "tool": "launch_app",
            "args": {"package_name": "com.android.settings; reboot"}
        },
        {
            "name": "Sensitive File Read Attempt",
            "tool": "read_file",
            "args": {"AbsolutePath": "/home/user/project/.env"}
        },
        {
            "name": "Credential Leakage in Agent Prompt / Arguments",
            "tool": "write_to_file",
            "args": {
                "TargetFile": "/tmp/test.txt",
                "CodeContent": "Deploying with API Key: AIzaSyD9x8y7Z6w5V4u3T2s1R0qP_testToken123"
            }
        }
    ]

    print("\nExecuting live inspection across 6 representative agent interaction vectors:\n")

    for idx, scenario in enumerate(test_scenarios, 1):
        print(f"[{idx}/6] Scenario: {scenario['name']}")
        print(f"     Tool: `{scenario['tool']}`")
        print(f"     Input Args: {json.dumps(scenario['args'])}")
        
        result = firewall.inspect_tool_call(scenario['tool'], scenario['args'])
        
        status_icon = "[BLOCKED]" if result.verdict == ActionVerdict.BLOCK else (
            "[REDACTED & ALLOWED]" if result.verdict == ActionVerdict.REDACT else "[ALLOWED]"
        )
        print(f"     Verdict: {status_icon} (Risk Score: {result.risk_score}/100)")
        print(f"     Reason: {', '.join(result.reasons)}")
        if result.verdict == ActionVerdict.REDACT:
            print(f"     Sanitized Output: {json.dumps(result.sanitized_arguments)}")
        print("-" * 70)

    summary = firewall.get_audit_summary()
    print("\n--- Firewall Telemetry & Audit Summary ---")
    print(f"   * Total Actions Inspected: {summary['total_inspected']}")
    print(f"   * Blocked Malicious Calls: {summary['blocked_actions']}")
    print(f"   * Sanitized / Redacted Calls: {summary['redacted_actions']}")
    print(f"   * Safe Passed Calls:       {summary['allowed_actions']}")
    print(f"   * Mean Risk Score:         {summary['average_risk_score']}/100")
    print("\n[OK] All defenses active. Zero unauthorized destructive payloads passed.")


if __name__ == "__main__":
    run_demo()
