"""KiTE Hostel & Canteen Feedback Hub."""
import json
from datetime import datetime

def record_feedback(student_id: str, meal_type: str, rating: int, comment: str):
    entry = {
        "student_id": student_id,
        "meal_type": meal_type,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.now().isoformat()
    }
    print(f"Recorded feedback for {meal_type}: Rating {rating}/5 - '{comment}'")
    return entry

if __name__ == "__main__":
    print("=== KiTE Canteen & Mess Feedback ===")
    record_feedback("24UCY129", "Breakfast", 5, "Idli and Sambar was fresh and hot!")
