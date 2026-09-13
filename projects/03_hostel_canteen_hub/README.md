# 🍽️ Hostel Canteen Hub

A simple Python-based mess and feedback tracker for hostel students. This project helps students view the weekly menu and submit quick feedback about meals, with a lightweight foundation for future analytics and reporting.

## ✨ Features

- **📝 Feedback logging** — `record_feedback()` captures student ID, meal type, rating, comment, and timestamp.
- **📋 Weekly menu tracker** — `mess_menu.json` stores the breakfast, lunch, snacks, and dinner schedule for each weekday.
- **📊 Menu lookup helper** — `get_menu_for_day()` retrieves the menu for any selected day and meal type.
- **🌐 Streamlit UI** — a small web interface lets users browse the menu and submit feedback from the browser.
- **✅ Test coverage** — the project includes validation tests for menu lookup and feedback persistence.

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** for the UI
- **JSON** for menu and feedback storage
- **Pytest** for automated validation

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/nandhakumar-murugan/KGISL-CAMPUS-SOLVERS.git
cd KGISL-CAMPUS-SOLVERS/projects/03_hostel_canteen_hub
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the script
```bash
python canteen_feedback.py
```

### 5. Launch the Streamlit app
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `canteen_feedback.py` | Handles menu lookup and feedback recording |
| `mess_menu.json` | Weekly mess menu data for the hostel |
| `streamlit_app.py` | Minimal user interface for viewing the menu and submitting feedback |
| `feedback_log.json` | Stores submitted feedback entries |
| `tests/test_canteen.py` | Verifies menu and feedback behavior |

## 🤝 How to Contribute

This project is a great beginner-friendly open-source contribution opportunity. Some good next steps include:

- **Feedback analytics** — calculate average ratings, identify popular meals, and show trends over time.
- **Menu dashboard improvements** — enhance the Streamlit UI with filters, summary cards, and a cleaner layout.
- **Nutritional voting** — let students vote on healthier or more preferred menu items.
- **Input validation** — improve handling for invalid ratings, empty comments, and duplicate submissions.
- **CSV/Excel export** — allow admins to download feedback reports.
- **More tests** — add coverage for edge cases such as invalid meal names or invalid day values.
- **Documentation updates** — add screenshots and a short demo section for easier onboarding.

Contributions of all levels are welcome. If you find a bug or have an idea for improvement, open an issue or submit a pull request.
