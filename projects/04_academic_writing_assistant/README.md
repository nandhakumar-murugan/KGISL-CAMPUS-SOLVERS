# KiTE Academic Writing Assistant

A small, student-friendly writing analyzer for engineering assignments and exam preparation. It reports word counts, explainable part-of-speech guesses, and basic sentence issues. Gemini is optional and provides a plain-language tutoring explanation when `GEMINI_API_KEY` is configured.

## Run

```bash
python app.py
```

Set the optional Gemini key before running:

```bash
# Windows PowerShell
$env:GEMINI_API_KEY = "your-key"
```

No API key is needed for the offline analyzer.

## Test

```bash
python -m unittest discover -s tests
```

This project intentionally avoids bundling model files, API keys, virtual environments, or student data.
