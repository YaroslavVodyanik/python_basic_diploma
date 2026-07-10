from telegram import Update
from telegram.ext import CallbackContext
from requests import RequestException
from api import (
    format_movies,
    get_high_budget_movies,
    get_low_budget_movies,
    get_movies_by_rating,
    search_movie_by_name,
)


history_data = []


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Здравствуйте! Используйте /help для списка команд.")


async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "/movie_search <название> — поиск фильма/сериала по названию\n"
        "/movie_by_rating <рейтинг> — поиск фильмов с рейтингом выше указанного\n"
        "/low_budget_movie — фильмы с низким бюджетом\n"
        "/high_budget_movie — фильмы с высоким бюджетом\n"
        "/history — история запросов"
    )
    await update.message.reply_text(help_text)


async def _reply_with_movies(update: Update, movies):
    text = format_movies(movies)
    if len(text) <= 4000:
        await update.message.reply_text(text)
        return

    for part_start in range(0, len(text), 4000):
        await update.message.reply_text(text[part_start:part_start + 4000])


async def _reply_with_error(update: Update, error):
    if isinstance(error, RuntimeError):
        await update.message.reply_text(str(error))
        return

    await update.message.reply_text(
        "Не получилось получить данные о фильмах. Проверьте API-ключ и попробуйте позже."
    )


async def movie_search(update: Update, context: CallbackContext):
    args = context.args
    name = ' '.join(args) if args else None
    if not name:
        await update.message.reply_text("Пожалуйста, укажите название фильма после команды.")
        return

    history_data.append(f"Поиск по названию: {name}")

    try:
        movies = search_movie_by_name(name)
    except (RuntimeError, RequestException) as error:
        await _reply_with_error(update, error)
        return

    await _reply_with_movies(update, movies)


async def movie_by_rating(update: Update, context: CallbackContext):
    args = context.args
    if not args:
        await update.message.reply_text("Пожалуйста, укажите минимальный рейтинг (например, /movie_by_rating 7.5).")
        return
    try:
        rating_threshold = float(args[0])
    except ValueError:
        await update.message.reply_text("Пожалуйста, укажите валидное число для рейтинга.")
        return

    history_data.append(f"Поиск фильмов с рейтингом выше {rating_threshold}")

    try:
        movies = get_movies_by_rating(rating_threshold)
    except (RuntimeError, RequestException) as error:
        await _reply_with_error(update, error)
        return

    await _reply_with_movies(update, movies)


async def low_budget_movie(update: Update, context: CallbackContext):
    history_data.append("Поиск фильмов с низким бюджетом")

    try:
        movies = get_low_budget_movies()
    except (RuntimeError, RequestException) as error:
        await _reply_with_error(update, error)
        return

    await _reply_with_movies(update, movies)


async def high_budget_movie(update: Update, context: CallbackContext):
    history_data.append("Поиск фильмов с высоким бюджетом")

    try:
        movies = get_high_budget_movies()
    except (RuntimeError, RequestException) as error:
        await _reply_with_error(update, error)
        return

    await _reply_with_movies(update, movies)


async def show_history(update: Update, context: CallbackContext):
    if not history_data:
        await update.message.reply_text("История пустая.")
    else:

        history_text = "\n".join(history_data[-20:])
        await update.message.reply_text(f"История запросов:\n{history_text}")


async def record_query(update: Update, context: CallbackContext):
    user_query = update.message.text
    history_data.append(user_query)
