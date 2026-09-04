"""
KiTE Smart Academic & Examination AI Assistant - Streamlit Web Interface.
Powered by Google Gemini API.
"""
import os
import streamlit as st
from app import get_answer

st.set_page_config(
    page_title="KiTE Academic AI Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 KiTE Smart Academic & Examination AI Assistant")
st.caption("Autonomous Engineering Exam Preparation & Syllabus Revision • Powered by Google Gemini")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input(
        "Gemini API Key (Optional if set in ENV)",
        type="password",
        help="Get your free API key at https://aistudio.google.com/"
    )
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.markdown("---")
    st.markdown("### 🏛️ KiTE Departments")
    st.markdown("- CS & Cybersecurity")
    st.markdown("- AI & Data Science")
    st.markdown("- Computer Science (CSE)")
    st.markdown("- Information Technology")
    st.markdown("- CSBS / ECE / Mech")

# Subject Selection
subject_options = [
    "CS3451 - Operating Systems",
    "AI3401 - Machine Learning Techniques",
    "IT3301 - Data Structures & Algorithms",
    "CS3491 - Cryptography & Network Security",
    "24UMA161 - Calculus and Matrix Algebra",
    "24UPY171 - Physics for Engineering",
    "Custom Subject Code"
]

selected_subject = st.selectbox("Select Course / Subject:", subject_options)

if selected_subject == "Custom Subject Code":
    subject_code = st.text_input("Enter Subject Code:", value="CS3451")
else:
    subject_code = selected_subject.split(" - ")[0]

# Answer format selection
col1, col2 = st.columns(2)
with col1:
    answer_format = st.radio(
        "Select Answer Type:",
        options=["2-mark", "16-mark"],
        format_func=lambda x: "🎯 2-Mark Short Answer" if x == "2-mark" else "📝 16-Mark Detailed Answer"
    )

with col2:
    st.info("**2-Mark:** Concise definition + key points.\n\n**16-Mark:** In-depth explanation + architecture/diagram + code/derivation.")

# Question input
default_question = "Explain Dijkstra's Algorithm with time complexity analysis and an example graph."
question = st.text_area("Enter University Examination Question / Topic:", value=default_question, height=100)

if st.button("🚀 Generate University Exam Answer", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question or topic.")
    else:
        with st.spinner(f"Generating structured {answer_format} response with Gemini..."):
            result = get_answer(subject_code, question, answer_format)
            
            if "Please set GEMINI_API_KEY" in result:
                st.error(result)
            elif result.startswith("Error querying Gemini:"):
                st.error(result)
            else:
                st.success("✅ Solution Generated Successfully!")
                st.markdown(f"### 📋 {subject_code} - {answer_format.upper()} Model Answer")
                st.markdown(result)
