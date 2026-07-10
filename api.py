import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("KINOPOISK_API_KEY")
BASE_URL = 'https://kinopoisk.dev/documentation'

def search_movie_by_name(name, genre=None, max_results=5):
    if not API_KEY:
        raise RuntimeError("Set KINOPOISK_API_KEY in .env before using Kinopoisk API.")

    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': API_KEY,
        'query': name,
        'language': 'ru-RU'
    }
    response = requests.get(url, params=params)
    data = response.json()
    results = data.get('results', [])[:max_results]

    return results

def get_movies_by_rating(min_rating=0, max_rating=10, max_results=5):

    pass

def get_low_budget_movies(max_budget=10000000, max_results=5):

    pass

def get_high_budget_movies(min_budget=50000000, max_results=5):

    pass
