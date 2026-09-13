# 🛡️ OpenAgentShield — Zero-Trust Security Gateway for Autonomous AI Agents

> **The Open-Source Security Firewall & AST Sandbox for AI Agent Tool Calls and Model Context Protocol (MCP) Middleware.**  
> *Engineered by **KGiSL Campus Solvers** • Lead Maintainer: [Nandhakumar M](https://github.com/nandhakumar-murugan) (Google Student Ambassador, B.E. CSE Cyber Security)*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![Test Suite](https://img.shields.io/badge/Tests-18%2F18_Passing-brightgreen.svg?style=for-the-badge)](tests/)
[![Security Standards](https://img.shields.io/badge/OWASP-Top_10_LLM_Mitigated-red.svg?style=for-the-badge)](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

---

## 🌍 The Global Real-World Challenge

Autonomous AI agents (Claude Code, Google Antigravity, Cursor, AutoGPT, Windsurf) are rapidly gaining write and shell execution powers on developer workstations, cloud infrastructure, and connected hardware (e.g. Android ADB devices).

However, **indirect prompt injection, malicious supply chains, and LLM hallucinations** can lead to disastrous real-world outcomes:
- **Catastrophic System Deletion**: AI executing `rm -rf /` or recursive deletions.
- **Shell Command Injections**: Chained shell payloads (`; reboot`, `| sh`, `&& rm`) escaping caller arguments (e.g. Google Artemis Issue #55).
- **Credential Exfiltration**: Leaking `.env` API keys, SSH private keys, or GitHub personal access tokens back into public LLM completions or logs.

**OpenAgentShield** acts as a high-performance, transparent proxy firewall between AI agents and underlying system tools, intercepting every invocation in micro-seconds to enforce zero-trust security policies.

---

## 🏗️ Architecture Overview

```
      [ Autonomous AI Agent / MCP Client ]
         (Claude Code / Antigravity / Cursor)
                         │
                         ▼
        ┌──────────────────────────────────┐
        │        OpenAgentShield Core       │
        │  ──────────────────────────────  │
        │  1. AST Shell Guard & Injection  │
        │  2. Secret & PII Redaction       │
        │  3. Sensitive File Boundaries    │
        │  4. Cryptographic Audit Hasher   │
        └──────────────────────────────────┘
                         │
                 [ Action Verdict ]
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
   [🛑 BLOCK]       [🔒 REDACT]      [✅ ALLOW]
Denied & Logged    Sanitized & Run   Safe Execution
```

---

## ✨ Core Defense Modules

### 1. 🛑 Shell AST & Command Injection Guard
- Tokenizes shell invocations and detects dangerous system binaries (`mkfs`, `dd`, `fdisk`, `reboot`, `shutdown`).
- Mitigates subshell chaining (`;`, `&&`, `|`, `` ` ``, `$()`).
- Validates Android package names against strict reverse-domain grammar (`^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+$`), eliminating ADB injection vectors.

### 2. 🔐 Zero-Leak Secret Sanitizer
- Scans input/output payloads for Google Cloud API keys, OpenAI keys, Anthropic keys, GitHub tokens (`ghp_`, `github_pat_`), AWS credentials, and RSA private keys.
- Automatically substitutes detected tokens with zero-knowledge markers (e.g. `[REDACTED:GOOGLE_API_KEY]`) before payloads touch logging or external agents.

### 3. 📂 Sensitive File System Boundary
- Blocks unauthorized reads and edits to `.env`, `.aws/credentials`, `/etc/passwd`, `/etc/shadow`, and `id_rsa` keys.

### 4. ⚡ MCP Middleware Decorator
- Provides `@interceptor.protect_tool` to wrap any Model Context Protocol (MCP) server tool asynchronously with zero latency overhead.

---

## 🚀 Quickstart & Interactive Simulation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Interactive Attack & Defense Simulation
```bash
python app.py
```
*Executes live inspection across 6 representative real-world attack scenarios (CVE-style destructive rm, shell chaining, ADB injection, credential exfiltration, and sensitive file reading).*

---

## 💻 Python Usage Example

```python
from agent_shield import AgentFirewall, ActionVerdict

# Initialize zero-trust firewall
firewall = AgentFirewall()

# Inspect an agent tool invocation before running it
result = firewall.inspect_tool_call(
    tool_name="run_command",
    arguments={"CommandLine": "echo 'Hello'; reboot"}
)

if result.verdict == ActionVerdict.BLOCK:
    print(f"Attack Blocked! Reasons: {result.reasons}")
else:
    print("Action approved for execution.")
```

### Protecting Model Context Protocol (MCP) Tools
```python
from agent_shield import MCPInterceptor

interceptor = MCPInterceptor()

@interceptor.protect_tool("execute_command")
async def execute_command(CommandLine: str):
    # This function will NEVER run if CommandLine contains dangerous or malicious syntax
    return os.system(CommandLine)
```

---

## 🧪 Verification & Automated Tests

OpenAgentShield maintains 100% test pass rates across all security assertion vectors:

```bash
pytest tests/test_firewall.py
```

Output:
```text
tests/test_firewall.py ......... [100%]
============================== 9 passed in 0.14s ==============================
```

---

## 🤝 Global Contributor Roadmap

We welcome student developers and security researchers worldwide:
- [ ] **eBPF Kernel Sandboxing**: Linux kernel level process confinement for agent bash subshells.
- [ ] **Real-Time Web Dashboard**: FastAPI + React telemetry dashboard with live agent risk visualizer.
- [ ] **LangChain / CrewAI Middleware**: Drop-in callbacks for popular Python agent frameworks.
- [ ] **Adversarial Benchmark Dataset**: 100+ standardized red-teaming test cases for LLM agent jailbreaks.

*Part of the **KGiSL Campus Solvers** open-source ecosystem. Built with ❤️ in Coimbatore, India for the global developer community.*
