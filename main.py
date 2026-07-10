from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
from handlers import (
    start, help_command, movie_search, show_history, record_query,
    movie_by_rating, low_budget_movie, high_budget_movie
)

def main():
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in .env before starting the bot.")

    application = Application.builder().token(token).build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("movie_search", movie_search))
    application.add_handler(CommandHandler("movie_by_rating", movie_by_rating))
    application.add_handler(CommandHandler("low_budget_movie", low_budget_movie))
    application.add_handler(CommandHandler("high_budget_movie", high_budget_movie))
    application.add_handler(CommandHandler("history", show_history))


    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, record_query))


    application.run_polling()

if __name__ == '__main__':
    main()
