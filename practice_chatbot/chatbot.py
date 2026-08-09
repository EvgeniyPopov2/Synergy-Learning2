"""Простой чат-бот по вопросам производственной практики."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DATA_FILE = Path(__file__).with_name("intents.json")


def normalize(text: str) -> str:
    """Приводит строку к виду, удобному для поиска ключевых слов."""
    text = text.lower().replace("ё", "е")
    return " ".join(re.findall(r"[a-zа-я0-9]+", text))


class PracticeChatBot:
    """Выбирает намерение пользователя по фразам и корням ключевых слов."""

    def __init__(self, data_file: Path | str = DATA_FILE) -> None:
        with Path(data_file).open("r", encoding="utf-8") as source:
            data: dict[str, Any] = json.load(source)
        self.intents: list[dict[str, Any]] = data["intents"]
        self.fallback: dict[str, str] = data["fallback"]

    def detect_intent(self, message: str) -> str:
        normalized = normalize(message)
        tokens = normalized.split()

        best_name = self.fallback["name"]
        best_score = 0

        for intent in self.intents:
            score = 0

            for phrase in intent.get("phrases", []):
                normalized_phrase = normalize(phrase)
                if normalized_phrase and normalized_phrase in normalized:
                    score += 4 + len(normalized_phrase.split())

            for keyword in intent.get("keywords", []):
                root = normalize(keyword)
                if root and any(token.startswith(root) for token in tokens):
                    score += 1

            if score > best_score:
                best_name = intent["name"]
                best_score = score

        return best_name

    def answer(self, message: str) -> str:
        intent_name = self.detect_intent(message)
        for intent in self.intents:
            if intent["name"] == intent_name:
                return intent["response"]
        return self.fallback["response"]


def main() -> None:
    bot = PracticeChatBot()
    print("Бот: Здравствуйте! Напишите 'помощь', чтобы увидеть мои возможности.")

    while True:
        try:
            message = input("Вы: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nБот: До свидания!")
            break

        if not message:
            continue

        intent = bot.detect_intent(message)
        print(f"Бот: {bot.answer(message)}")
        if intent == "farewell":
            break


if __name__ == "__main__":
    main()

