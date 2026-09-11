# 🍽️ KiTE Hostel & Canteen Feedback Hub

A simple Python-based project for managing hostel mess menu information and recording student feedback about meals.

The project is designed as a beginner-friendly starting point for students who want to learn Python, JSON data handling, testing, and contribute new features to a campus utility project.

---

## 🎯 Project Overview

The Hostel & Canteen Feedback Hub currently provides:

- 🍛 Weekly hostel mess menu information
- 🕒 Meal timings
- ⭐ Student meal feedback recording
- 💬 Feedback comments
- 🕐 Automatic timestamp generation
- 🧪 Basic automated testing

The project can be extended in the future with feedback analytics, menu search, nutritional information, and other useful campus features.

---

## ✨ Current Features

### 1. 🍴 Mess Menu

The `mess_menu.json` file contains:

- Hostel name
- Breakfast timing
- Lunch timing
- Snacks timing
- Dinner timing
- Weekly meal schedule

The menu is organized by day and meal type.

### 2. ⭐ Feedback Recording

The `canteen_feedback.py` file provides the `record_feedback()` function.

It accepts:

```text
Student ID
Meal type
Rating
Comment