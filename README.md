# Python Basic Diploma: Telegram Movie Bot

Telegram-бот для поиска информации о фильмах и сериалах. Проект сделан в рамках дипломной работы по базовому курсу Python.

## Возможности

- поиск фильма или сериала по названию;
- поиск фильмов по минимальному рейтингу;
- подборки фильмов с низким или высоким бюджетом;
- история пользовательских запросов;
- команда помощи со списком доступных действий.

## Команды бота

```text
/start
/help
/movie_search <название>
/movie_by_rating <рейтинг>
/low_budget_movie
/high_budget_movie
/history
```

## Технологии

- Python
- python-telegram-bot
- requests
- python-dotenv
- Kinopoisk API

## Установка и запуск

1. Клонировать репозиторий:

```bash
git clone https://github.com/YaroslavVodyanik/python_basic_diploma.git
cd python_basic_diploma
```

2. Создать и активировать виртуальное окружение:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Установить зависимости:

```bash
pip install -r requirements.txt
```

4. Создать файл `.env` по примеру `.env.example`:

```text
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
KINOPOISK_API_KEY=your_kinopoisk_api_key
```

5. Запустить бота:

```bash
python main.py
```

## Скриншоты

Скриншоты работы бота находятся в папке `screenshots`.

## Важно

Токены и API-ключи не должны храниться в коде и публиковаться на GitHub. Для запуска проекта используйте локальный файл `.env`.
