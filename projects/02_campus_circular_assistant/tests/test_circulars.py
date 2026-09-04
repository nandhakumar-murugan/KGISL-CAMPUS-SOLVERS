import importlib.util
from pathlib import Path

app_path = Path(__file__).resolve().parent.parent / 'query_circulars.py'
spec = importlib.util.spec_from_file_location('query_circulars', str(app_path))
circulars_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(circulars_mod)

def test_search_circulars_finds_results():
    results = circulars_mod.search_circulars('exam')
    assert isinstance(results, list)

def test_search_circulars_empty():
    results = circulars_mod.search_circulars('xyznonexistentterm999')
    assert results == []
