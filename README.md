# Blog Platform Backend (Python/FastAPI)

Современный бэкенд для блог-платформы, построенный на Python с использованием FastAPI, SQLAlchemy и PostgreSQL.

## 🚀 Технологический стек

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - система миграций базы данных
- **PostgreSQL** - реляционная база данных
- **Pydantic** - валидация данных и сериализация
- **python-slugify** - генерация slug из заголовков
- **Uvicorn** - ASGI сервер

## 📦 Установка

### Локальная установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd blog-platform-backend
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте базу данных PostgreSQL:**
```bash
# Создайте базу данных
createdb blog_platform

# Скопируйте файл конфигурации
cp env.example .env

# Отредактируйте .env файл с вашими настройками БД
```

5. **Запустите миграции:**
```bash
alembic upgrade head
```

6. **Запустите сервер:**
```bash
uvicorn app.main:app --reload
```

### Docker установка

1. **Запустите с Docker Compose:**
```bash
docker-compose up --build
```

Сервер будет доступен по адресу: `http://localhost:8000`

## 📚 API Документация

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 API Endpoints

### Статьи

- `POST /api/articles` - Создание статьи
- `GET /api/articles` - Список статей (с пагинацией)
- `GET /api/articles/{slug}` - Получение статьи по slug
- `PUT /api/articles/{slug}` - Обновление статьи
- `DELETE /api/articles/{slug}` - Удаление статьи

### Формат статьи

```json
{
  "title": "string (1-200 символов)",
  "description": "string (1-500 символов)", 
  "body": "string (обязательное поле)",
  "tag_list": ["string"] // опциональное поле
}
```

## ✨ Особенности

- **Автоматическая генерация slug** из заголовка статьи
- **Полная валидация данных** с помощью Pydantic
- **Пагинация** для списка статей
- **Автоматическая документация API** (Swagger/OpenAPI)
- **Система миграций** с Alembic
- **Логирование запросов** и ошибок
- **CORS поддержка**
- **Docker контейнеризация**
- **Типизация** с помощью Python type hints

## 🗂️ Структура проекта

```
app/
├── __init__.py
├── main.py              # Основной файл приложения
├── config.py            # Конфигурация приложения
├── database.py          # Настройка базы данных и модели
├── schemas.py           # Pydantic схемы для валидации
├── crud.py              # CRUD операции
└── routers/
    ├── __init__.py
    └── articles.py      # Маршруты для статей

alembic/                 # Миграции базы данных
├── versions/
└── env.py

docker-compose.yml       # Docker конфигурация
Dockerfile              # Docker образ
requirements.txt        # Python зависимости
alembic.ini            # Конфигурация Alembic
```

## 🛠️ Разработка

### Создание миграций

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description of changes"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Запуск тестов

```bash
# Установите тестовые зависимости
pip install pytest pytest-asyncio httpx

# Запустите тесты
pytest
```

## 📝 Примеры использования

### Создание статьи

```bash
curl -X POST "http://localhost:8000/api/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Моя первая статья",
    "description": "Краткое описание статьи",
    "body": "Полный текст статьи с подробным содержанием...",
    "tag_list": ["блог", "программирование", "API"]
  }'
```

### Получение списка статей

```bash
curl -X GET "http://localhost:8000/api/articles?skip=0&limit=10"
```

### Python пример

```python
import httpx

async def create_article():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/articles",
            json={
                "title": "Новая статья",
                "description": "Описание",
                "body": "Содержание...",
                "tag_list": ["python", "fastapi"]
            }
        )
        return response.json()

# Использование
import asyncio
result = asyncio.run(create_article())
print(result)
```

## 🔧 Конфигурация

Основные настройки находятся в `app/config.py`:

- `DATABASE_URL` - URL подключения к PostgreSQL
- `SECRET_KEY` - секретный ключ для JWT (если используется)
- `API_TITLE` - название API
- `ALLOWED_ORIGINS` - разрешенные CORS источники

## 🐳 Docker

### Сборка образа

```bash
docker build -t blog-platform-backend .
```

### Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f app

# Остановка
docker-compose down
```

## 📊 Мониторинг

- **Health Check**: `GET /health`
- **API Info**: `GET /`
- **Логи**: автоматическое логирование всех запросов

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request
