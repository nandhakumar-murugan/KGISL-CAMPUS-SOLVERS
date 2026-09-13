# 🍽️ Hostel Canteen Hub

A simple but practical hostel mess dashboard built for students to quickly check the daily menu, view serving times, and submit meal feedback. The app is designed to make student dining information easier to access and more actionable for hostel administrators.

## ✨ Features

- **📋 Meal menu browser** — view the menu for any day and meal type
- **⏰ Meal timing display** — shows the service window for breakfast, lunch, snacks, and dinner
- **⭐ Rating summary cards** — quick insight into feedback for each meal category
- **📝 Student feedback form** — submit rating, comments, and student ID directly from the dashboard
- **📊 Data persistence** — stores feedback to JSON for lightweight tracking and analysis
- **✅ Automated validation** — tests ensure menu logic and feedback logging remain reliable

## 🧩 What the app does

This project helps hostel students:

- choose the day and meal they want to check
- read the menu items for that meal
- see serving time information
- submit a rating and comment
- review quick meal feedback summaries

It is built as a lightweight, beginner-friendly Streamlit app with future-ready analytics potential.

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** for the web interface
- **JSON** for menu and feedback storage
- **Pytest** for test validation

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

### 4. Run the application
```bash
streamlit run streamlit_app.py
```

### 5. Optional: run the Python helper module directly
```bash
python canteen_feedback.py
```

## 📁 Project Structure

| File | Purpose |
|------|---------|
| `canteen_feedback.py` | Core logic for menu lookup, meal timings, and feedback recording |
| `mess_menu.json` | Weekly hostel menu data |
| `streamlit_app.py` | Interactive UI for viewing menu and submitting feedback |
| `feedback_log.json` | Stores submitted feedback records |
| `requirements.txt` | Required Python dependencies |
| `tests/test_canteen.py` | Automated tests for menu and feedback behavior |

## 🧠 Example workflow

1. Select a day from the dropdown
2. Choose a meal such as breakfast or lunch
3. Review the served items and timing
4. Enter student ID, rating, and comment
5. Submit feedback to store the review

## 🤝 Future enhancements

This project is a great beginner-friendly contribution area. Some useful improvements include:

- **Feedback analytics dashboard** — average ratings by meal and trends over time
- **Admin report export** — CSV/Excel download for hostel staff
- **Meal popularity insights** — identify the most liked meal categories
- **Input validation improvements** — duplicate checks and cleaner validation logic
- **Health-focused meal filters** — highlight healthier or preferred menu items
- **Better visualization** — charts and summaries for daily feedback patterns

Contributions are welcome. If you want to improve the app or fix a bug, open an issue or submit a pull request.

