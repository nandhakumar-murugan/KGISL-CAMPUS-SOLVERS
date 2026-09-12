"""
OpenAgentShield - The Open-Source Firewall and Safety Sandbox for Autonomous AI Agents.
Developed by KGiSL Campus Solvers & Lead Maintainer Nandhakumar Murugan.
"""

from .policy import SecurityPolicy, ActionVerdict, RuleSeverity, PolicyRule
from .sanitizer import SecretSanitizer
from .shell_guard import ShellGuard
from .firewall import AgentFirewall
from .mcp_interceptor import MCPInterceptor

__version__ = "1.0.0"
__all__ = [
    "AgentFirewall",
    "SecurityPolicy",
    "ActionVerdict",
    "RuleSeverity",
    "PolicyRule",
    "SecretSanitizer",
    "ShellGuard",
    "MCPInterceptor",
]
