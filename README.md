# cat_fund

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Технологии

![Python](https://img.shields.io/badge/python-3.9-blue?logo=python)
![Framework-FastAPI](https://img.shields.io/badge/Framework-FastAPI-brightgreen?logo=pydantic&labelColor=grey&color=blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-brightgreen?logo=pydantic&labelColor=grey&color=blue)
![Pydantic](https://img.shields.io/badge/Pydantic-brightgreen?logo=pydantic&labelColor=grey&color=blue)
![Google-Cloud](https://img.shields.io/badge/Google-Cloud-brightgreen?logo=googlecloud&labelColor=grey&color=blue)
![Google-Sheets](https://img.shields.io/badge/Google-Sheets-brightgreen?logo=googlesheets&labelColor=grey&color=blue)
![Google-Drive](https://img.shields.io/badge/Google-Drive-brightgreen?logo=googledrive&labelColor=grey&color=blue)

### Запуск проекта

- Клонируйте репозитоий

git@github.com:SvShatunova/cat_fund.git

- Перейти в нужную папку

cd cat_fund

- Установите и активируйте виртуальное окружение

python3 -m venv venv
source venv/Scripts/activate

python3 -m pip install --upgrade pip

- Установите зависимости из файла requirements.txt

pip install -r requirements.txt

- в корневой папке проекта создайте файл .env со следующим содержимым:

APP_TITLE=<Ваш вариант названия проекта>
PROJECT_DESCRIPTION=<Ваш вариант описания проекта>
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=<Ваш вариант серкретного ключа>
FIRST_SUPERUSER_EMAIL=<e-mail для автоматического создания суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль для автоматического создания суперюзера>

Данные, получаемые после настройки Google Cloud:
EMAIL=<ваш e-mail гугл-аккаунта>
TYPE=service_account
PROJECT_ID=<идентификатор>
PRIVATE_KEY_ID=<id приватного ключа>
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----<приватный ключ>-----END PRIVATE KEY-----\n
CLIENT_EMAIL=<email сервисного аккаунта>
CLIENT_ID=<id сервисного аккаунта>
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https:<ваша ссылка на местоположение общедоступных сертификатов (X.509) публичных ключей для сервисных аккаунтов Google в формате JSON Web Key (JWK), которые используются для аутентификации>
UNIVERSE_DOMAIN=googleapis.com

- создайте базу данных, применив миграции (из корневой папки проекта)

alembic upgrade head

- запустите проект локально (из корневой папки проекта)

uvicorn app.main:app --reload

- описание эндпоинтов и возможностей доступно по этим ссылкам

[Swagger](http://127.0.0.1:8000/doc)

или

[Redoc](http://127.0.0.1:8000/redoc)

### Автор

[Светлана Шатунова](https://github.com/SvShatunova)
