from telegram import Update
from telegram.ext import CallbackContext


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


async def movie_search(update: Update, context: CallbackContext):
    args = context.args
    name = ' '.join(args) if args else None
    if not name:
        await update.message.reply_text("Пожалуйста, укажите название фильма после команды.")
        return

    history_data.append(f"Поиск по названию: {name}")

    await update.message.reply_text(f"Поиск фильма: {name}")


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

    await update.message.reply_text(f"Поиск фильмов с рейтингом выше {rating_threshold} (пример).")


async def low_budget_movie(update: Update, context: CallbackContext):
    history_data.append("Поиск фильмов с низким бюджетом")

    await update.message.reply_text("Поиск фильмов с низким бюджетом (пример).")


async def high_budget_movie(update: Update, context: CallbackContext):
    history_data.append("Поиск фильмов с высоким бюджетом")

    await update.message.reply_text("Поиск фильмов с высоким бюджетом (пример).")


async def show_history(update: Update, context: CallbackContext):
    if not history_data:
        await update.message.reply_text("История пустая.")
    else:

        history_text = "\n".join(history_data[-20:])
        await update.message.reply_text(f"История запросов:\n{history_text}")


async def record_query(update: Update, context: CallbackContext):
    user_query = update.message.text
    history_data.append(user_query)
