"""KiTE Syllabus & Arrear Clearance AI Assistant.
Powered by Google Gemini API.
"""
import os
import sys

def get_answer(subject_code: str, question: str) -> str:
    print(f"Querying KiTE Syllabus Bot for [{subject_code}]: {question}...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Please set GEMINI_API_KEY environment variable. Get a free key at https://aistudio.google.com/"
    
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        prompt = (
            f"You are an expert autonomous engineering professor at KGiSL Institute of Technology (KiTE).\n"
            f"Subject Code: {subject_code}\n"
            f"Question: {question}\n\n"
            f"Provide a structured, high-scoring university answer (2-mark or 16-mark format with clear headings and bullet points)."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error querying Gemini: {e}"

if __name__ == "__main__":
    print("=== KiTE Syllabus AI Assistant ===")
    code = input("Enter Subject Code (e.g. 24UMA161, 24UCS511): ") or "24UMA161"
    q = input("Enter Exam Question / Topic: ") or "State Cayley-Hamilton Theorem and find inverse of matrix."
    print("\nAnswer:\n", get_answer(code, q))
