import csv
import os
import time
from datetime import datetime

import requests

from app import API_KEY, OPENROUTER_URL, load_persona

MODELS = [
    "qwen/qwen3.8-flash",
    "deepseek/deepseek-v4.1-flash",
    "anthropic/claude-haiku-5.5",
]

QUESTIONS = [
    "Prompt injection nedir? Kısaca anlat.",
    "Python'da bir listedeki tekrar eden elemanları nasıl silerim?",
    "Overfitting ile underfitting arasındaki fark nedir?",
    "Bir web uygulamasını SQL injection saldırısına karşı nasıl korurum?",
    "Yapay zekâ ve siber güvenlik alanında staj için nasıl bir yol haritası önerirsin?",
]


def run_one(model, question):
    messages = [
        {"role": "system", "content": load_persona()},
        {"role": "user", "content": question},
    ]

    start = time.time()
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": model, "messages": messages},
        timeout=120,
    )
    elapsed = time.time() - start
    response.raise_for_status()

    data = response.json()
    usage = data.get("usage", {})

    return {
        "model": model,
        "question": question,
        "seconds": round(elapsed, 2),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "cost_usd": usage.get("cost"),
        "answer": data["choices"][0]["message"]["content"],
        "error": "",
    }


def main():
    os.makedirs("results", exist_ok=True)
    filename = f"results/eval_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    rows = []

    total = len(MODELS) * len(QUESTIONS)
    count = 0

    for question in QUESTIONS:
        for model in MODELS:
            count += 1
            print(f"[{count}/{total}] {model} -> {question[:40]}...")
            try:
                row = run_one(model, question)
                print(f"    ✓ {row['seconds']} sn, {row['completion_tokens']} token")
            except Exception as e:
                row = {"model": model, "question": question, "error": str(e)}
                print(f"    ✗ Hata: {e}")
            rows.append(row)

    fields = ["model", "question", "seconds", "prompt_tokens",
              "completion_tokens", "cost_usd", "answer", "error"]
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nBitti! Sonuçlar: {filename}")


if __name__ == "__main__":
    main()