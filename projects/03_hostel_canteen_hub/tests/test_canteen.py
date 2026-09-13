import importlib.util
import json
from pathlib import Path

import pytest

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


def test_get_menu_for_day_returns_expected_meal():
    menu = canteen_mod.get_menu_for_day('Monday', 'breakfast')
    assert 'Pongal' in menu
    assert 'Tea' in menu


def test_get_menu_for_day_rejects_invalid_day():
    with pytest.raises(ValueError):
        canteen_mod.get_menu_for_day('Funday', 'breakfast')


def test_get_meal_timing_returns_expected_schedule():
    timing = canteen_mod.get_meal_timing('lunch')
    assert '12:15 PM' in timing
    assert '01:45 PM' in timing


def test_get_feedback_summary_returns_average_rating():
    entries = [
        {'meal_type': 'Lunch', 'rating': 5},
        {'meal_type': 'Lunch', 'rating': 3},
        {'meal_type': 'Dinner', 'rating': 4},
    ]
    summary = canteen_mod.get_feedback_summary(entries)
    assert summary['Lunch']['count'] == 2
    assert summary['Lunch']['average_rating'] == 4.0
    assert summary['Dinner']['average_rating'] == 4.0


def test_record_feedback_logs_to_json_file(tmp_path):
    log_path = tmp_path / 'feedback_log.json'
    res = canteen_mod.record_feedback('TEST_02', 'Dinner', 4, 'Nice taste', log_path=log_path)

    assert log_path.exists()
    saved_data = json.loads(log_path.read_text(encoding='utf-8'))
    assert any(item['student_id'] == 'TEST_02' and item['meal_type'] == 'Dinner' for item in saved_data)
    assert res['student_id'] == 'TEST_02'
