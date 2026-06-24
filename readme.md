# YaCut

YaCut - сервис для укорачивания ссылок. Приложение создано для того,
чтобы пользователь мог преобразовать длинный URL в короткую ссылку,
предложить собственный вариант короткого идентификатора или получить его
автоматически.

Дополнительно сервис позволяет загружать несколько файлов на Яндекс Диск.
После загрузки приложение создает короткие ссылки для скачивания этих
файлов.

## Технологии

Проект разработан на Python с использованием Flask.

В проекте используются:

- Flask - основа веб-приложения;
- Flask-SQLAlchemy - работа с базой данных;
- Flask-WTF - обработка веб-форм;
- Flask-Migrate - управление миграциями;
- aiohttp - асинхронные запросы к API Яндекс Диска;
- SQLite - база данных на этапе разработки;
- python-dotenv - загрузка переменных окружения из `.env`.

## Запуск проекта

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone <адрес_репозитория>
cd async-yacut
```

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
```

Для Windows:

```bash
source venv/Scripts/activate
```

Для Linux/macOS:

```bash
source venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте файл `.env` по примеру `.env.example` и укажите переменные
окружения:

```env
FLASK_APP=yacut
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=sqlite:///db.sqlite3
DISK_TOKEN=your_yandex_disk_oauth_token
```

Создайте базу данных:

```bash
flask shell
```

В интерактивной оболочке выполните:

```python
from yacut import db
db.create_all()
exit()
```

Запустите приложение:

```bash
flask run
```

После запуска проект будет доступен по адресу:

```text
http://127.0.0.1:5000/
```

## Автор

Бочков Артем - [https://github.com/userartemru](https://github.com/userartemru)
