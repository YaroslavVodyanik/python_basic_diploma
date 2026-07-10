import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("KINOPOISK_API_KEY")
BASE_URL = "https://api.kinopoisk.dev/v1.4/movie"
MAX_FREE_LIMIT = 5


def _request(path="", params=None):
    if not API_KEY or API_KEY == "your_kinopoisk_api_key":
        raise RuntimeError("Добавьте настоящий KINOPOISK_API_KEY в файл .env.")

    response = requests.get(
        f"{BASE_URL}{path}",
        headers={"X-API-KEY": API_KEY},
        params=params or {},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def _get_docs(data):
    return data.get("docs", [])


def _rating_value(movie):
    rating = movie.get("rating") or {}
    return rating.get("kp") or rating.get("imdb") or "нет"


def _movie_title(movie):
    return (
        movie.get("name")
        or movie.get("alternativeName")
        or movie.get("enName")
        or "Без названия"
    )


def _movie_description(movie):
    description = movie.get("shortDescription") or movie.get("description")
    if not description:
        return "Описание не найдено."
    return description[:350] + "..." if len(description) > 350 else description


def format_movie(movie, index):
    title = _movie_title(movie)
    year = movie.get("year") or "год не указан"
    rating = _rating_value(movie)
    description = _movie_description(movie)
    budget = movie.get("budget") or {}
    budget_text = ""

    if budget.get("value"):
        currency = budget.get("currency") or ""
        budget_text = f"\nБюджет: {budget['value']:,} {currency}".replace(",", " ")

    return (
        f"{index}. {title} ({year})\n"
        f"Рейтинг: {rating}"
        f"{budget_text}\n"
        f"{description}"
    )


def format_movies(movies):
    if not movies:
        return "Ничего не найдено."

    return "\n\n".join(format_movie(movie, index) for index, movie in enumerate(movies, 1))


def search_movie_by_name(name, genre=None, max_results=5):
    params = {
        "query": name,
        "page": 1,
        "limit": min(max_results, MAX_FREE_LIMIT),
    }
    data = _request("/search", params=params)
    return _get_docs(data)


def get_movies_by_rating(min_rating=0, max_rating=10, max_results=5):
    params = {
        "rating.kp": f"{min_rating}-{max_rating}",
        "notNullFields": ["name", "rating.kp", "description"],
        "sortField": "rating.kp",
        "sortType": "-1",
        "page": 1,
        "limit": min(max_results, MAX_FREE_LIMIT),
    }
    data = _request(params=params)
    return _get_docs(data)


def get_low_budget_movies(max_budget=10000000, max_results=5):
    params = {
        "budget.value": f"1-{max_budget}",
        "notNullFields": ["name", "budget.value", "rating.kp"],
        "sortField": "budget.value",
        "sortType": "1",
        "page": 1,
        "limit": min(max_results, MAX_FREE_LIMIT),
    }
    data = _request(params=params)
    return _get_docs(data)


def get_high_budget_movies(min_budget=50000000, max_results=5):
    params = {
        "budget.value": f"{min_budget}-1000000000",
        "notNullFields": ["name", "budget.value", "rating.kp"],
        "sortField": "budget.value",
        "sortType": "-1",
        "page": 1,
        "limit": min(max_results, MAX_FREE_LIMIT),
    }
    data = _request(params=params)
    return _get_docs(data)
