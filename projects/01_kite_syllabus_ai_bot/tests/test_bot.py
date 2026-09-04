import os
import importlib.util
from pathlib import Path
import pytest

app_path = Path(__file__).resolve().parent.parent / "app.py"
spec = importlib.util.spec_from_file_location("syllabus_app", str(app_path))
syllabus_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(syllabus_app)

def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    resp = syllabus_app.get_answer("CS3451", "What is an AVL Tree?", "2-mark")
    assert "Please set GEMINI_API_KEY" in resp
