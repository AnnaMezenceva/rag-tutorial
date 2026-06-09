"""Проверка demo-ответа."""

from app.generator import ask

def show(label, question):
    print(f"\n--- {label}: «{question}» ---")
    result = ask(question)
    print(f"Ответ:\n{result['answer']}\n")
    print(f"Источников: {len(result['sources'])}")
    for i, src in enumerate(result["sources"], 1):
        print(f"  [{i}] doc_id={src['doc_id']}, score={src['score']:.4f}, name={src['name'][:60]}...")

if __name__ == "__main__":
    show("Тюрьма", "Какой фильм про побег из тюрьмы?")
    show("Космос", "Какие фильмы о космосе?")
    show("Мафия", "Посоветуй фильм про мафию")
    show("Война", "Какие есть фильмы про войну?")
    show("Negative", "Как приготовить борщ?")