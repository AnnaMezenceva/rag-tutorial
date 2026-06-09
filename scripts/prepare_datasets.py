"""Конвертация TMDB CSV → datasets.json для RAG-pipeline."""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "raw" / "top10K-TMDB-movies.csv"
OUT_JSON = ROOT / "data" / "raw" / "datasets.json"

GENRE_MAP = {
    "Drama": "драма драмы драму",
    "Crime": "криминал криминальный мафия мафию мафии преступность преступление",
    "Comedy": "комедия комедии смешной юмор",
    "Action": "боевик боевики экшен",
    "Horror": "ужасы ужасов хоррор страшный",
    "Romance": "романтика романтический любовь любви",
    "Thriller": "триллер триллеры напряжение",
    "Adventure": "приключения приключение путешествие",
    "Science Fiction": "фантастика фантастику фантастики космос космосе космический",
    "Fantasy": "фэнтези магия магии волшебство",
    "Animation": "мультфильм мультфильмы анимация",
    "War": "война войну войны военный военные солдат солдаты",
    "Documentary": "документальный документальное",
    "Mystery": "детектив детективы тайна тайну загадка расследование",
    "Family": "семейный семейное детский",
    "History": "исторический исторические история историю",
    "Music": "музыка музыку музыкальный",
    "Western": "вестерн ковбой ковбои",
}

KEYWORD_MAP = {
    "prison": "тюрьма тюрьмы тюрьму заключённый заключённые",
    "escape": "побег побега побегу сбежать",
    "murder": "убийство убийства убийцу",
    "love": "любовь любви любовную",
    "robot": "робот роботы роботов",
    "alien": "инопланетянин инопланетяне пришелец пришельцы",
    "zombie": "зомби",
    "vampire": "вампир вампиры",
    "ghost": "призрак призраки",
    "dragon": "дракон драконы",
    "king": "король короля королевство",
    "queen": "королева королевы",
    "detective": "детектив расследование расследования",
    "spy": "шпион шпионы агент",
    "superhero": "супергерой супергерои",
    "school": "школа школы школьный",
    "family": "семья семьи семейный",
    "revenge": "месть мести",
    "survival": "выживание выживания",
    "island": "остров острова острове",
    "ocean": "океан океане море",
    "space": "космос космосе космический",
    "planet": "планета планеты планете",
    "ship": "корабль корабля",
    "pirate": "пират пираты пиратов",
    "death": "смерть смерти",
    "dream": "сон сновидение мечта",
    "monster": "монстр монстры чудовище",
    "army": "армия армии",
    "police": "полиция полицейский",
    "bank": "банк ограбление ограбления",
    "money": "деньги денег",
    "child": "ребёнок дети детей",
    "horse": "лошадь лошади",
    "car": "машина машины гонка гонки",
    "race": "гонка гонки",
    "fight": "бой сражение сражения битва",
    "wedding": "свадьба свадьбы",
    "christmas": "рождество",
    "witch": "ведьма ведьмы",
    "magic": "магия магии волшебство",
    "wizard": "волшебник волшебники",
    "dinosaur": "динозавр динозавры",
}


def translate_genres(genre_str: str) -> str:
    return " ".join(
        GENRE_MAP.get(g.strip(), "") for g in genre_str.split(",")
    ).strip()


def extract_keywords(overview: str) -> str:
    overview_lower = overview.lower()
    tags = []
    for eng, rus in KEYWORD_MAP.items():
        if eng in overview_lower:
            tags.append(rus)
    return " ".join(tags)


def main():
    datasets = []
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            overview = (row.get("overview") or "").strip()
            if len(overview) < 50:
                continue

            title = row.get("title", "").strip()
            genre = row.get("genre", "").strip()
            year = row.get("release_date", "")[:4]
            rating = row.get("vote_average", "")
            lang = row.get("original_language", "")
            genres_ru = translate_genres(genre)
            keywords_ru = extract_keywords(overview)

            text = (
                f"Фильм: {title}. Жанр: {genre} ({genres_ru}). "
                f"Год выпуска: {year}. Рейтинг: {rating}. "
                f"Язык оригинала: {lang}.\n\n"
                f"Описание:\n{overview}\n\n"
                f"Ключевые слова: {genres_ru} {keywords_ru}"
            )

            datasets.append({
                "id": len(datasets),
                "name": f"{title} ({year})",
                "text": text,
            })

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps({"datasets": datasets}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Записано {len(datasets)} фильмов в {OUT_JSON}")


if __name__ == "__main__":
    main()
