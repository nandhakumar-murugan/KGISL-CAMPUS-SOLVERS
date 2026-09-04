"""KiTE Campus Circular Assistant."""
import json
import os

def search_circulars(query: str):
    db_path = os.path.join(os.path.dirname(__file__), "circulars_db.json")
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    results = [c for c in data if query.lower() in c["title"].lower() or query.lower() in c["summary"].lower()]
    return results

if __name__ == "__main__":
    print("=== KiTE Campus Circular Helper ===")
    q = input("Search circular (e.g. mobile, exam): ") or "mobile"
    matches = search_circulars(q)
    for m in matches:
        print(f"\n[{m['circular_id']}] {m['title']} ({m['date']})")
        print(f"Summary: {m['summary']}")
