# Conventions

## Границы изменений
- Минимальный diff, принцип KISS
- Одна итерация = одна задача

## Архитектура модулей
- scripts/prepare_datasets.py — конвертация CSV в datasets.json
- scripts/ingest.py — загрузка данных в documents.jsonl
- app/chunker.py — нарезка на чанки
- scripts/build_index.py — построение TF-IDF индекса
- app/retriever.py — поиск top-k по cosine similarity
- app/generator.py — формирование ответа
- app/main.py — Streamlit UI

## Правила ответа
- Отвечать ТОЛЬКО по найденному контексту
- Если данных нет — явный отказ
- Не выдумывать факты

## Тесты
- pytest, минимум 5 тестов
- Тесты chunking + retrieval