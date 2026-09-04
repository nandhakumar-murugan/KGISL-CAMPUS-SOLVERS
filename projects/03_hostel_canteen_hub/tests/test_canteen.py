import importlib.util
from pathlib import Path

app_path = Path(__file__).resolve().parent.parent / 'canteen_feedback.py'
spec = importlib.util.spec_from_file_location('canteen_feedback', str(app_path))
canteen_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(canteen_mod)

def test_record_feedback():
    res = canteen_mod.record_feedback('TEST_01', 'Lunch', 5, 'Great food')
    assert res['student_id'] == 'TEST_01'
    assert res['rating'] == 5
    assert res['meal_type'] == 'Lunch'
    assert 'timestamp' in res
