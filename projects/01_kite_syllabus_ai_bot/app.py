"""KiTE Smart Academic & Examination AI Assistant.
Powered by Google Gemini API.
"""
import os

def get_answer(subject_code: str, question: str, answer_type: str = "16-mark") -> str:
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
            f"Provide a structured, high-scoring university examination answer in strict {answer_type} format "
            f"with clear definitions, bullet points, and key concepts."
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

    print("\nSelect Answer Type:")
    print("1. 2-Mark Answer")
    print("2. 16-Mark Answer")
    choice = input("Choose (1 or 2): ")

    if choice == "1":
        answer_type = "2-mark"
    elif choice == "2":
        answer_type = "16-mark"
    else:
        print("Invalid choice. Defaulting to 16-mark answer.")
        answer_type = "16-mark"

    q = input("\nEnter Exam Question / Topic: ") or "Explain Dijkstra's Algorithm with a neat diagram and time complexity analysis."
    print("\nAnswer:\n", get_answer(code, q, answer_type))
