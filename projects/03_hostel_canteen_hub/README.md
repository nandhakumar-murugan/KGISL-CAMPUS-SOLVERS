# 🍽️ Hostel Canteen Hub

A simple Python starter for collecting and logging student feedback on hostel mess meals, paired with a structured weekly mess menu — built as a foundation for a fuller canteen feedback and menu system.

## ✨ Current Features

- **📝 Feedback Recording Engine** — `record_feedback()` in `canteen_feedback.py` records student feedback with automatic ISO timestamps:
  - `student_id` (str): Student registration / roll number
  - `meal_type` (str): `Breakfast` | `Lunch` | `Snacks` | `Dinner`
  - `rating` (int): Scale of 1 to 5 stars
  - `comment` (str): Detailed feedback on quality, hygiene, or quantity
- **📋 Weekly Mess Menu & Timing Structure** — `mess_menu.json` stores the weekly meal schedule for the KGiSL IIM Men's Hostel Mess:
  - **Breakfast**: 07:30 AM – 09:00 AM
  - **Lunch**: 12:30 PM – 02:00 PM
  - **Snacks**: 04:30 PM – 05:30 PM
  - **Dinner**: 07:30 PM – 09:00 PM
  - Includes special Sunday feast menus.

> This is an early-stage tool. The menu file and feedback script are separate pieces right now — see **How to Contribute** below for what's missing (menu tracker UI, feedback analytics, voting).

## 🛠️ Tech Stack

- **Python 3** (standard library only — `json`, `datetime`)
- **JSON** for menu data storage

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/nandhakumar-murugan/KGISL-CAMPUS-SOLVERS.git
   cd KGISL-CAMPUS-SOLVERS/projects/03_hostel_canteen_hub
   ```

2. **Make sure Python 3 is installed**
   ```bash
   python --version
   ```

3. **Run the script**
   ```bash
   python canteen_feedback.py
   ```
   This runs a demo call to `record_feedback()` and prints the recorded feedback to the console.

4. **Explore the menu data**
   Open `mess_menu.json` to see the weekly mess schedule — it's not yet wired into the script, but it's ready to be read and displayed.

## 📂 Project Files

| File | Purpose |
|------|---------|
| `canteen_feedback.py` | Defines `record_feedback(student_id, meal_type, rating, comment)` — builds a feedback entry with a timestamp and prints it |
| `mess_menu.json` | Weekly mess menu (breakfast/lunch/snacks/dinner) with meal timings for the KGiSL IIM Men's Hostel |

## 🤝 How to Contribute

This is a great beginner-friendly project to build on. Ideas:

- **Menu Tracker** — write a function that reads `mess_menu.json` and prints/shows "what's for lunch today" based on the current day
- **Persist feedback** — currently feedback prints and is discarded; save entries to a file or small database (e.g. append to a JSON/CSV log)
- **Feedback analytics** — once feedback is saved, add a summary function (average rating per meal, most-commented dish, etc.)
- **Nutritional voting** — add a simple voting mechanism so students can flag preferred/healthier menu items
- **Input validation** — handle bad ratings (e.g. outside 1–5) or empty comments gracefully
- **CLI menu** — turn the script into an interactive loop instead of one hardcoded demo call
- **Tests** — add unit tests for `record_feedback()`
- **Screenshot** — add one here once you've run it, so future contributors know what to expect

Found a bug or have an idea beyond this list? Open an issue or submit a PR — no prior experience needed to get started!