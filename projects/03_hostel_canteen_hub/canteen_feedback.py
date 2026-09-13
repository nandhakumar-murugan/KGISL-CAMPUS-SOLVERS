"""KiTE Hostel & Canteen Feedback Hub."""
import json
from datetime import datetime
from pathlib import Path


def load_menu_data():
    """Load the weekly hostel mess menu from the JSON file."""
    menu_path = Path(__file__).with_name("mess_menu.json")
    with menu_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_menu_for_day(day: str, meal_type: str) -> str:
    """Return the menu for a specific day and meal type."""
    weekly_schedule = load_menu_data().get("weekly_schedule", {})
    normalized_day = day.strip().title()
    normalized_meal = meal_type.strip().lower()

    if normalized_day not in weekly_schedule:
        valid_days = ", ".join(weekly_schedule.keys())
        raise ValueError(f"Invalid day: '{day}'. Choose from: {valid_days}")

    valid_meals = {"breakfast", "lunch", "snacks", "dinner"}
    if normalized_meal not in valid_meals:
        raise ValueError(
            f"Invalid meal type: '{meal_type}'. Choose from: {', '.join(sorted(valid_meals))}"
        )

    return weekly_schedule[normalized_day][normalized_meal]


def get_meal_timing(meal_type: str) -> str:
    """Return the serving window for a meal."""
    meal_timings = load_menu_data().get("meal_timings", {})
    normalized_meal = meal_type.strip().lower()
    valid_meals = {"breakfast", "lunch", "snacks", "dinner"}

    if normalized_meal not in valid_meals:
        raise ValueError(
            f"Invalid meal type: '{meal_type}'. Choose from: {', '.join(sorted(valid_meals))}"
        )

    return meal_timings.get(normalized_meal, "Timing not available")


def load_feedback_log(log_path: str | Path | None = None) -> list[dict]:
    """Load feedback entries from the JSON log file."""
    if log_path is None:
        log_path = Path(__file__).with_name("feedback_log.json")
    log_path = Path(log_path)

    if not log_path.exists():
        return []

    try:
        with log_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    return data if isinstance(data, list) else []


def get_feedback_summary(entries: list[dict]) -> dict:
    """Summarize average ratings by meal type."""
    ordered_meals = ["Breakfast", "Lunch", "Snacks", "Dinner"]
    summary = {meal: {"count": 0, "total_rating": 0, "average_rating": 0.0} for meal in ordered_meals}

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        meal_type = str(entry.get("meal_type", "")).strip().title()
        rating = entry.get("rating")

        if meal_type not in summary:
            summary[meal_type] = {"count": 0, "total_rating": 0, "average_rating": 0.0}

        try:
            rating_value = int(rating)
        except (TypeError, ValueError):
            continue

        summary.setdefault(meal_type, {"count": 0, "total_rating": 0, "average_rating": 0.0})
        summary[meal_type]["count"] += 1
        summary[meal_type]["total_rating"] += rating_value

    for meal, values in summary.items():
        count = values["count"]
        values["average_rating"] = round(values["total_rating"] / count, 1) if count else 0.0

    return {meal: summary[meal] for meal in ordered_meals if meal in summary}


def save_feedback_log(entry: dict, log_path: str | Path | None = None):
    """Persist feedback entries to a JSON list file."""
    if log_path is None:
        log_path = Path(__file__).with_name("feedback_log.json")
    log_path = Path(log_path)

    if log_path.exists():
        with log_path.open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(entry)
    with log_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def record_feedback(
    student_id: str,
    meal_type: str,
    rating: int,
    comment: str,
    log_path: str | Path | None = None,
):
    entry = {
        "student_id": student_id,
        "meal_type": meal_type,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
    }
    save_feedback_log(entry, log_path)
    print(f"Recorded feedback for {meal_type}: Rating {rating}/5 - '{comment}'")
    return entry


if __name__ == "__main__":
    print("=== KiTE Canteen & Mess Feedback ===")
    record_feedback("KITE_STUDENT_01", "Breakfast", 5, "Idli and Sambar was fresh and hot!")

    today = datetime.now().strftime("%A")
    print(f"\nToday's menu for {today}:")
    for meal in ["breakfast", "lunch", "snacks", "dinner"]:
        try:
            menu_value = get_menu_for_day(today, meal)
            print(f"- {meal.title()}: {menu_value}")
        except ValueError as exc:
            print(f"- {meal.title()}: {exc}")
