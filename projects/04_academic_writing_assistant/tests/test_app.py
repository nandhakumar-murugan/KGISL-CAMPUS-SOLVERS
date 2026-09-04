import unittest

from app import analyze_text, tokenize


class WritingAssistantTests(unittest.TestCase):
    def test_tokenize_ignores_punctuation(self):
        self.assertEqual(tokenize("Hello, KiTE students!"), ["Hello", "KiTE", "students"])

    def test_analyzer_reports_basic_sentence_issues(self):
        result = analyze_text("this is a very long sentence")
        self.assertEqual(result["word_count"], 6)
        self.assertIn("Start the sentence with a capital letter.", result["issues"])
        self.assertIn("End the sentence with punctuation.", result["issues"])

    def test_analyzer_handles_empty_input(self):
        result = analyze_text("")
        self.assertEqual(result["word_count"], 0)
        self.assertTrue(result["issues"])


if __name__ == "__main__":
    unittest.main()
