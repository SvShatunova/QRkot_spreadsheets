# QRkot_spreadseets

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Инструкция по развёртыванию проекта

* клонировать проект на компьютер `git clone https://github.com`
* создание виртуального окружения `python3 -m venv venv`
* запуск виртуального окружения `. venv/bin/activate`, `source/venv/Scripts/activate`
* установить зависимости из файла requirements.txt `pip install -r requirements.txt`
* запуск сервера `uvicorn main:app`
* запуск сервера с автоматическим рестартом `uvicorn main:app --reload`
* инициализируем Alembic в проекте `alembic init --template async alembic`
* создание файла миграции `alembic revision --autogenerate -m "migration name"`
* применение миграций `alembic upgrade head`
* отмена миграций `alembic downgrade`
* запуск тестов `pytest`

### Автор

Светлана Шатунова
