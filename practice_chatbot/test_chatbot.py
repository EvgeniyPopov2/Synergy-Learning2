"""Автоматические тесты чат-бота."""

import unittest

from chatbot import PracticeChatBot, normalize
from evaluate import evaluate


class PracticeChatBotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bot = PracticeChatBot()

    def test_normalize(self) -> None:
        self.assertEqual(normalize("  ВСЁ, хорошо! "), "все хорошо")

    def test_greeting(self) -> None:
        self.assertEqual(self.bot.detect_intent("Здравствуйте!"), "greeting")

    def test_dates(self) -> None:
        self.assertEqual(
            self.bot.detect_intent("Когда заканчивается практика?"),
            "practice_dates",
        )

    def test_hours(self) -> None:
        self.assertEqual(
            self.bot.detect_intent("Сколько недель длится практика?"),
            "practice_hours",
        )

    def test_place(self) -> None:
        self.assertEqual(
            self.bot.detect_intent("Где проходит практика?"),
            "practice_place",
        )

    def test_documents(self) -> None:
        self.assertEqual(
            self.bot.detect_intent("Какие документы прикрепить?"),
            "documents",
        )

    def test_unknown_question(self) -> None:
        self.assertEqual(self.bot.detect_intent("Расскажи анекдот"), "fallback")

    def test_evaluation_dataset(self) -> None:
        result = evaluate()
        self.assertEqual(result["total"], 30)
        self.assertEqual(result["correct"], 28)
        self.assertAlmostEqual(result["accuracy"], 28 / 30)


if __name__ == "__main__":
    unittest.main()

