import unittest

from app.utils.fallback_content import build_fallback_questions, build_fallback_evaluation


class FallbackContentTests(unittest.TestCase):
    def test_build_fallback_questions_returns_five_tailored_questions(self):
        candidate = {
            "name": "Ava",
            "role": "Python Developer",
            "experience": "3 years",
            "skills": "FastAPI, SQLAlchemy",
            "difficulty": "Intermediate",
        }

        questions = build_fallback_questions(candidate)

        self.assertEqual(len(questions), 5)
        self.assertTrue(all("question" in item for item in questions))
        self.assertTrue(any("FastAPI" in item["question"] for item in questions))

    def test_build_fallback_evaluation_returns_expected_structure(self):
        candidate = {
            "name": "Ava",
            "role": "Python Developer",
            "experience": "3 years",
            "skills": "FastAPI, SQLAlchemy",
            "difficulty": "Intermediate",
        }
        questions = [{"id": 1, "question": "Explain FastAPI"}]
        answers = [{"questionId": 1, "answer": "I used FastAPI"}]

        evaluation = build_fallback_evaluation(candidate, questions, answers)

        self.assertIn("overallScore", evaluation)
        self.assertIn("recommendation", evaluation)
        self.assertIn("questionEvaluation", evaluation)
        self.assertEqual(len(evaluation["questionEvaluation"]), 1)


if __name__ == "__main__":
    unittest.main()
