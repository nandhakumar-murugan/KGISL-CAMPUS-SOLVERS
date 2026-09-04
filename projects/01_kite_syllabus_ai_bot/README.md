# 🎓 KiTE Smart Academic & Examination AI Assistant

An autonomous engineering examination preparation assistant powered by the Google Gemini API.

---

## 🌟 Features
- **University Syllabus Grounding:** Tailored for KiTE Autonomous Regulations (CS, AI & DS, Cyber Security, IT, ECE).
- **Dual Examination Formats (PR #8 by Harini Sri):**
  - 🎯 **2-Mark Short Answer:** Concise definitions, formula statements, and key points.
  - 📝 **16-Mark Detailed Answer:** Comprehensive explanations, architectural breakdown, derivations, and step-by-step algorithms.
- **Web UI & CLI Interfaces:** Launch via Streamlit web portal or lightweight Python CLI.

## 🚀 Quick Start

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/):
```bash
export GEMINI_API_KEY="your_api_key_here"  # On Windows: set GEMINI_API_KEY="your_api_key_here"
```

### 3. Run Web Interface
```bash
streamlit run streamlit_app.py
```

### 4. Run CLI Interface
```bash
python app.py
```
