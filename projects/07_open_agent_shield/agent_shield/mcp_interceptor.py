"""
Model Context Protocol (MCP) Interceptor.
Provides transparent middleware wrapping for MCP server tools in modern AI IDEs
(Google Antigravity, Claude Code, Cursor, Windsurf).
"""

import functools
from typing import Callable, Any, Dict, Optional
from .firewall import AgentFirewall, EvaluationResult, ActionVerdict


class SecurityInterceptionError(Exception):
    """Raised when an agent tool invocation is intercepted and denied by policy."""
    def __init__(self, result: EvaluationResult):
        self.result = result
        super().__init__(f"Security Exception [{result.tool_name}]: {', '.join(result.reasons)}")


class MCPInterceptor:
    """Middleware for securing MCP server endpoints against malicious or runaway tool calls."""

    def __init__(self, firewall: Optional[AgentFirewall] = None):
        self.firewall = firewall or AgentFirewall()

    def protect_tool(self, tool_name: Optional[str] = None):
        """Decorator for MCP tools to enforce automatic inspection and sanitization."""
        def decorator(func: Callable) -> Callable:
            actual_tool_name = tool_name or func.__name__

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> Any:
                evaluation = self.firewall.inspect_tool_call(actual_tool_name, kwargs)
                if evaluation.verdict == ActionVerdict.BLOCK:
                    raise SecurityInterceptionError(evaluation)
                # Use sanitized arguments (e.g. redacted credentials)
                return await func(*args, **evaluation.sanitized_arguments)

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> Any:
                evaluation = self.firewall.inspect_tool_call(actual_tool_name, kwargs)
                if evaluation.verdict == ActionVerdict.BLOCK:
                    raise SecurityInterceptionError(evaluation)
                return func(*args, **evaluation.sanitized_arguments)

            import inspect
            return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

        return decorator
