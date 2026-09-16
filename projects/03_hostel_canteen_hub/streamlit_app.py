from datetime import datetime
from pathlib import Path

import streamlit as st

from canteen_feedback import (
    get_feedback_summary,
    get_meal_timing,
    get_menu_for_day,
    load_feedback_log,
    record_feedback,
)


LOG_PATH = Path(__file__).with_name("feedback_log.json")
MEAL_BADGES = {
    "breakfast": {"color": "#E8F7E8", "text": "#1F7A1F", "emoji": "☀️"},
    "lunch": {"color": "#EAF3FF", "text": "#1D4ED8", "emoji": "🍱"},
    "snacks": {"color": "#FFF3E6", "text": "#B45309", "emoji": "🥨"},
    "dinner": {"color": "#F3E8FF", "text": "#7C3AED", "emoji": "🌙"},
}

st.set_page_config(page_title="Hostel Canteen Hub", page_icon="🍽️")

st.markdown(
    """
    <style>
        .main { background: linear-gradient(135deg, #f7f9fc 0%, #eef4ff 100%); }
        .block-container {
            max-width: 1200px;
            margin: 0 auto;
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }
        div[data-testid="stMetricValue"] { font-size: 1.4rem; }
        .section-header {
            font-size: 1.25rem;
            font-weight: 700;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .info-card {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #dfe7f5;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 4px 12px rgba(31, 41, 55, 0.08);
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        .meal-badge {
            display: inline-block;
            padding: 0.35rem 0.8rem;
            border-radius: 999px;
            font-weight: 600;
            margin: 0.15rem 0.3rem 0.15rem 0;
        }
        div[data-testid="stForm"] {
            background: rgba(255,255,255,0.7);
            border: 1px solid #dfe7f5;
            border-radius: 16px;
            padding: 1rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        div[data-testid="stSegmentedControl"] {
            max-width: 520px;
        }
        div[data-testid="stSelectbox"] {
            max-width: 520px;
        }
        .stAlert, .stSuccess, .stWarning, .stInfo {
            border-radius: 12px;
        }
        .top-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.5rem;
        }
        .panel-stack {
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
            height: 100%;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🍽️ Hostel Canteen Hub")
st.caption("Pick a day and meal to quickly check what’s being served and share your feedback.")

st.markdown('<div class="top-controls"></div>', unsafe_allow_html=True)

weekdays = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

selected_day = st.selectbox("Choose a day", weekdays, index=datetime.now().weekday(), help="Select the day you want to view the mess menu for.")
selected_meal = st.segmented_control(
    "Choose a meal",
    options=["breakfast", "lunch", "snacks", "dinner"],
    selection_mode="single",
    default="lunch" if datetime.now().hour < 18 else "dinner",
    label_visibility="visible",
)

meal_summary = get_feedback_summary(load_feedback_log(LOG_PATH))
meal_badges_html = "".join(
    f"<span class='meal-badge' style='background:{MEAL_BADGES[meal]['color']}; color:{MEAL_BADGES[meal]['text']};'>"
    f"{MEAL_BADGES[meal]['emoji']} {meal.title()}</span>"
    for meal in ["breakfast", "lunch", "snacks", "dinner"]
)
st.markdown(f"<div style='margin-bottom: 1rem;'>{meal_badges_html}</div>", unsafe_allow_html=True)

menu_col, feedback_col = st.columns([1.45, 1.05], vertical_alignment="center")

with menu_col:
    with st.container():
        try:
            menu = get_menu_for_day(selected_day, selected_meal)
            meal_timing = get_meal_timing(selected_meal)
            menu_items = [item.strip() for item in menu.split(",") if item.strip()]

            st.markdown('<div class="section-header">📋 Today’s menu</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class='info-card'>
                    <strong>{selected_day}</strong><br>
                    <span style='font-size: 1.1rem; font-weight: 600; color: #0d6efd;'>{selected_meal.title()}</span>
                    <br><br>
                    {menu}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(f"Serving time: {meal_timing}")

            with st.expander("View all menu items", expanded=False):
                for item in menu_items:
                    st.markdown(f"- {item}")

            st.info(f"{selected_meal.title()} is served from {meal_timing}.")

            st.markdown('<div class="section-header">⭐ Quick rating summary</div>', unsafe_allow_html=True)
            summary_cols = st.columns(4)
            for idx, meal in enumerate(["breakfast", "lunch", "snacks", "dinner"]):
                stats = meal_summary.get(meal.title(), {"count": 0, "average_rating": 0.0})
                badge = MEAL_BADGES[meal]
                with summary_cols[idx]:
                    rating_text = "No ratings yet" if stats["count"] == 0 else f"{stats['average_rating']:.1f} / 5"
                    review_text = "0 reviews" if stats["count"] == 0 else f"{stats['count']} reviews"
                    st.markdown(
                        f"""
                        <div class='info-card' style='background:{badge['color']}; border-color: transparent; min-height: 118px; display:flex; flex-direction:column; justify-content:center;'>
                            <div style='font-weight: 700; color:{badge['text']};'>{badge['emoji']} {meal.title()}</div>
                            <div style='font-size: 1.8rem; color:{badge['text']}; margin-top: 0.5rem;'>{rating_text}</div>
                            <div style='color:{badge['text']};'>{review_text}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except ValueError as exc:
            st.error(str(exc))

with feedback_col:
    with st.container():
        st.markdown('<div class="section-header">📝 Share feedback</div>', unsafe_allow_html=True)
        with st.form("feedback_form"):
            student_id = st.text_input("Student ID", placeholder="KITE_STUDENT_01")
            rating = st.slider("Rating", 1, 5, 3, help="Rate your meal from 1 to 5")
            comment = st.text_area(
                "Comment",
                placeholder="Tell us what was good or needs improvement...",
            )
            submitted = st.form_submit_button("Submit Feedback", type="primary")

        if submitted:
            if not student_id.strip() or not comment.strip():
                st.warning("Please enter both a student ID and a comment before submitting.")
            else:
                entry = record_feedback(student_id.strip(), selected_meal, rating, comment.strip(), log_path=LOG_PATH)
                st.success("Feedback recorded successfully!")
                st.json(entry)
                st.caption(f"Saved to: {LOG_PATH.name}")
