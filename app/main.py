"""Streamlit UI: вопрос -> фрагменты -> ответ -> источники."""

import streamlit as st

from app.config import INDEX_CHUNKS_JSONL, MATRIX_NPZ, TOP_K, VECTORIZER_PKL
from app.generator import ask
from app.prompts import MIN_SCORE
from app.retriever import Retriever

DEMO_QUESTIONS = [
    "Какой фильм про побег из тюрьмы?",
    "Какие фильмы о космосе?",
    "Посоветуй фильм про мафию",
    "Какие есть фильмы про войну?",
    "Как приготовить борщ?",
]

def index_exists() -> bool:
    return all(p.exists() for p in (VECTORIZER_PKL, MATRIX_NPZ, INDEX_CHUNKS_JSONL))

@st.cache_resource
def load_retriever() -> Retriever:
    return Retriever()

def render_chunk(i: int, src: dict, expanded: bool = True) -> None:
    label = f"[{i}] doc_id={src['doc_id']} · score={src['score']:.4f}"
    with st.expander(label, expanded=expanded):
        st.markdown(f"**{src['name']}**")
        st.text(src["text"])

def render_fragments(sources: list[dict], score_threshold: float) -> None:
    st.subheader("Найденные фрагменты (top-k)")
    filtered = [s for s in sources if s["score"] >= score_threshold]
    if not filtered:
        st.info("Фрагменты не найдены (или score ниже порога).")
        return
    for i, src in enumerate(filtered, 1):
        render_chunk(i, src, expanded=src["score"] >= MIN_SCORE)

def render_sources(sources: list[dict]) -> None:
    st.subheader("Источники")
    if not sources:
        st.info("Источники отсутствуют.")
        return
    for i, src in enumerate(sources, 1):
        render_chunk(i, src, expanded=False)

def main() -> None:
    st.set_page_config(page_title="RAG Tutorial — TMDB Movies", layout="wide")
    st.title("RAG Tutorial — TMDB Movies")
    st.caption("Учебный RAG: TF-IDF + demo-ответ с источниками (9979 фильмов)")

    if not index_exists():
        st.error(
            "Индекс не собран. Сначала выполните:\n\n"
            "`uv run python scripts/build_index.py`"
        )
        st.stop()

    # --- Sidebar ---
    st.sidebar.header("Demo-вопросы")
    for q in DEMO_QUESTIONS:
        if st.sidebar.button(q, use_container_width=True):
            st.session_state["question"] = q

    st.sidebar.markdown("---")
    st.sidebar.header("Настройки")
    score_threshold = st.sidebar.slider(
        "Порог score", min_value=0.0, max_value=1.0, value=0.0, step=0.05,
        help="Показывать только фрагменты с score выше порога"
    )
    top_k = st.sidebar.slider(
        "Top-K результатов", min_value=1, max_value=10, value=TOP_K,
        help="Сколько фрагментов искать"
    )

    # --- История запросов ---
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if st.session_state["history"]:
        st.sidebar.markdown("---")
        st.sidebar.header("История запросов")
        for past_q in st.session_state["history"][-10:]:
            if st.sidebar.button(f"↩ {past_q}", key=f"hist_{past_q}", use_container_width=True):
                st.session_state["question"] = past_q

    # --- Основная часть ---
    question = st.text_input("Ваш вопрос", key="question")

    if st.button("Спросить", type="primary"):
        if not question.strip():
            st.warning("Введите вопрос.")
            st.stop()

        if question.strip() not in st.session_state["history"]:
            st.session_state["history"].append(question.strip())

        with st.spinner("Поиск..."):
            result = ask(question.strip(), k=top_k, retriever=load_retriever())

        render_fragments(result["sources"], score_threshold)

        st.subheader("Ответ")
        st.text(result["answer"])

        render_sources(result["sources"])

if __name__ == "__main__":
    main()