"""KiTE Academic Writing Assistant."""

from __future__ import annotations

import os
import re
from collections import Counter


WORD_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
COMMON_VERBS = {
    "am", "are", "be", "been", "being", "can", "could", "did", "do", "does",
    "had", "has", "have", "is", "may", "might", "must", "shall", "should",
    "was", "were", "will", "would",
}
COMMON_DETERMINERS = {"a", "an", "the", "this", "that", "these", "those"}
COMMON_PRONOUNS = {
    "he", "her", "hers", "him", "his", "i", "it", "its", "me", "my", "our",
    "she", "their", "theirs", "them", "they", "us", "we", "you", "your",
}


def tokenize(text: str) -> list[str]:
    """Return words from a sentence while ignoring punctuation."""
    return WORD_PATTERN.findall(text)


def guess_part_of_speech(word: str) -> str:
    """Provide a lightweight POS guess without requiring a model download."""
    normalized = word.lower()
    if normalized in COMMON_PRONOUNS:
        return "PRON"
    if normalized in COMMON_DETERMINERS:
        return "DET"
    if normalized in COMMON_VERBS or normalized.endswith(("ed", "ing")):
        return "VERB"
    if normalized.endswith(("ly",)):
        return "ADV"
    if normalized.endswith(("ous", "ful", "ive", "al")):
        return "ADJ"
    return "NOUN"


def analyze_text(text: str) -> dict:
    """Analyze words and return simple, explainable writing signals."""
    words = tokenize(text)
    tags = [{"word": word, "pos": guess_part_of_speech(word)} for word in words]
    counts = Counter(item["pos"] for item in tags)
    issues: list[str] = []

    if not words:
        issues.append("Enter a sentence or paragraph to analyze.")
    if words and text[:1].islower():
        issues.append("Start the sentence with a capital letter.")
    if words and text.rstrip()[-1:] not in ".!?":
        issues.append("End the sentence with punctuation.")
    if len(words) > 35:
        issues.append("Consider splitting this long sentence into smaller sentences.")
    if re.search(r"\s{2,}", text):
        issues.append("Remove repeated spaces.")

    return {
        "word_count": len(words),
        "pos_counts": dict(counts),
        "tokens": tags,
        "issues": issues,
    }


def explain_with_gemini(text: str, analysis: dict) -> str:
    """Ask Gemini for a student-friendly explanation when an API key is available."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Set GEMINI_API_KEY to receive a Gemini explanation."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        prompt = (
            "You are a supportive English tutor for engineering students. "
            "Explain the writing issues below in plain language and give one improved example.\n\n"
            f"Text: {text}\n"
            f"Analysis: {analysis}"
        )
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        return response.text or "Gemini returned no explanation."
    except Exception as error:
        return f"Gemini explanation unavailable: {error}"


if __name__ == "__main__":
    sentence = input("Enter a sentence to analyze: ").strip()
    result = analyze_text(sentence)
    print(f"\nWords: {result['word_count']}")
    print(f"POS counts: {result['pos_counts']}")
    print(f"Issues: {result['issues'] or 'No basic issues found.'}")
    print(f"\nGemini tutor: {explain_with_gemini(sentence, result)}")
