"""KiTE Smart Academic & Examination AI Assistant.
Powered by Google Gemini API.
"""
import os
import sys

def get_answer(subject_code: str, question: str) -> str:
    print(f"Querying KiTE Academic AI Assistant for [{subject_code}]: {question}...")
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
            f"Provide a structured, high-scoring university examination answer (2-mark or 16-mark format with clear definitions, bullet points, and key concepts)."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Error querying Gemini: {e}"

if __name__ == "__main__":
    print("=== KiTE Smart Academic & Examination AI Assistant ===")
    code = input("Enter Subject Code (e.g. CS3451, AI3401, IT3301): ") or "CS3451"
    q = input("Enter Exam Question / Topic: ") or "Explain Dijkstra's Algorithm with a neat diagram and time complexity analysis."
    print("\nAnswer:\n", get_answer(code, q))
