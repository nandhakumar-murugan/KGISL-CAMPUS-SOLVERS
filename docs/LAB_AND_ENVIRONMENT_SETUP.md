# Lab and Environment Setup Guide

This guide helps first-year and second-year students set up Python, virtual environments, and Git on college lab PCs or personal laptops — especially machines where these tools haven't been configured before.

## 1. Check Your Python Version

Before anything else, confirm Python is installed and check its version.

**Windows / Linux / macOS:**
```bash
python --version
```

If that doesn't work, try:
```bash
python3 --version
```

You should see output like `Python 3.11.4`. If you get a "command not found" error, you'll need to install Python first from [python.org](https://www.python.org/downloads/).

## 2. Create a Virtual Environment

A virtual environment keeps your project's dependencies separate from other projects and the system Python.

From your project folder, run:
```bash
python -m venv venv
```

This creates a folder named `venv` containing an isolated Python environment.

## 3. Activate the Virtual Environment

Activation differs by OS and shell — use the one that matches your setup.

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```
> If you get a security/execution policy error, run PowerShell as Administrator and execute:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Windows Command Prompt (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux / macOS Bash:**
```bash
source venv/bin/activate
```

Once activated, you'll see `(venv)` at the start of your terminal prompt — that confirms it's active.

To deactivate at any time:
```bash
deactivate
```

## 4. Install Project Requirements

With your virtual environment active, install all required packages:
```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet and are installing packages manually, save your current setup for others with:
```bash
pip freeze > requirements.txt
```

## 5. Configure Git Username and Email

Git needs to know who you are before you can commit changes. Set this globally (once per machine):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

Verify it worked:
```bash
git config --global --list
```

## Troubleshooting

- **`python` not recognized on Windows** → Try `py` instead, or reinstall Python and check "Add Python to PATH" during setup.
- **`pip` not recognized** → Make sure your virtual environment is activated first.
- **PowerShell blocks script execution** → See the execution policy fix under Step 3.

---

*Once set up, head back to [`STUDENT_ONBOARDING_GUIDE.md`](../STUDENT_ONBOARDING_GUIDE.md) to continue with the rest of the onboarding steps.*