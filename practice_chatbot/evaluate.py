"""Оценка точности распознавания и скорости ответа чат-бота."""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter

from chatbot import PracticeChatBot


CASES_FILE = Path(__file__).with_name("evaluation_cases.json")


def evaluate() -> dict[str, object]:
    bot = PracticeChatBot()
    with CASES_FILE.open("r", encoding="utf-8") as source:
        cases = json.load(source)

    correct = 0
    errors: list[dict[str, str]] = []
    elapsed_ms = 0.0

    for case in cases:
        started = perf_counter()
        predicted = bot.detect_intent(case["text"])
        bot.answer(case["text"])
        elapsed_ms += (perf_counter() - started) * 1000

        if predicted == case["expected"]:
            correct += 1
        else:
            errors.append(
                {
                    "text": case["text"],
                    "expected": case["expected"],
                    "predicted": predicted,
                }
            )

    total = len(cases)
    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total,
        "average_ms": elapsed_ms / total,
        "errors": errors,
    }


def main() -> None:
    result = evaluate()
    print(f"Всего фраз: {result['total']}")
    print(f"Распознано верно: {result['correct']}")
    print(f"Точность: {result['accuracy']:.1%}")
    print(f"Среднее время обработки: {result['average_ms']:.3f} мс")

    errors = result["errors"]
    if errors:
        print("Ошибки распознавания:")
        for error in errors:
            print(
                f"- {error['text']} -> {error['predicted']} "
                f"(ожидалось: {error['expected']})"
            )


if __name__ == "__main__":
    main()

