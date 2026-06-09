# Техническое видение MVP

## Технологии
- Python 3.11+
- Streamlit (UI)
- scikit-learn (TF-IDF + cosine similarity)
- pytest (тесты)
- uv (менеджер пакетов)

## Как строится индекс
top10K-TMDB-movies.csv → datasets.json → documents.jsonl → chunks.jsonl → TF-IDF матрица

## Как работает поиск
Cosine similarity между TF-IDF вектором запроса и матрицей чанков.
Возвращается top-k результатов с doc_id и score.

## Что НЕ используется в MVP
- Embeddings / sentence-transformers
- Внешние LLM (OpenAI API и т.д.)
- Векторные базы данных (ChromaDB, FAISS)
- Reranking

## Как запускать
uv sync
uv run python scripts/prepare_datasets.py
uv run python scripts/build_index.py
uv run streamlit run app/main.py