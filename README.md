# Blog Platform Backend (Python/FastAPI)

Современный бэкенд для блог-платформы с управлением пользователями и статьями, построенный на Python с использованием FastAPI, SQLAlchemy и PostgreSQL.

## 🚀 Технологический стек

- **FastAPI** - современный веб-фреймворк для Python
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - система миграций базы данных
- **PostgreSQL** - реляционная база данных
- **Pydantic** - валидация данных и сериализация
- **python-jose** - JWT токены для аутентификации
- **passlib** - хеширование паролей
- **python-slugify** - генерация slug из заголовков
- **Uvicorn** - ASGI сервер

## 📦 Установка

### Локальная разработка (только база данных)

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd blog-platform-backend
```

2. **Запустите только PostgreSQL:**
```bash
docker-compose --profile dev up -d
```

3. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

4. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

5. **Настройте переменные окружения:**
```bash
cp env.example .env
```

6. **Запустите миграции:**
```bash
alembic upgrade head
```

7. **Запустите сервер:**
```bash
uvicorn src.main:app --reload
```

### Полное развертывание с Docker

1. **Запустите полное приложение:**
```bash
docker-compose --profile prod up -d
```

Приложение будет доступно по адресу: `http://localhost:8000`

### Профили Docker Compose

- **`dev`** - Только база данных для локальной разработки
- **`prod`** - Полное приложение с health checks

Подробнее см. [DOCKER_PROFILES.md](DOCKER_PROFILES.md)

## 📚 API Документация

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Развернутое приложение

- **Live Demo**: [https://msa-zfd1.onrender.com](https://msa-zfd1.onrender.com)
- **API Docs**: [https://msa-zfd1.onrender.com/docs](https://msa-zfd1.onrender.com/docs)

## 🔗 API Endpoints

### Пользователи

- `POST /api/users` - Регистрация пользователя
- `POST /api/users/login` - Аутентификация пользователя

### Текущий пользователь

- `GET /api/user` - Получение текущего пользователя
- `PUT /api/user` - Обновление текущего пользователя

### Статьи

- `POST /api/articles` - Создание статьи (требует аутентификации)
- `GET /api/articles` - Список статей (с пагинацией)
- `GET /api/articles/{slug}` - Получение статьи по slug
- `PUT /api/articles/{slug}` - Обновление статьи (только автор)
- `DELETE /api/articles/{slug}` - Удаление статьи (только автор)

### Комментарии

- `POST /api/articles/{slug}/comments` - Добавление комментария к статье (требует аутентификации)
- `GET /api/articles/{slug}/comments` - Получение комментариев к статье (с пагинацией)
- `DELETE /api/articles/{slug}/comments/{id}` - Удаление комментария (только автор комментария)

### Формат пользователя

```json
{
  "email": "string (email)",
  "username": "string (3-50 символов, только буквы и цифры)",
  "password": "string (6-100 символов)",
  "bio": "string (опционально, до 500 символов)",
  "image_url": "string (опционально, до 500 символов)"
}
```

### Формат статьи

```json
{
  "title": "string (1-200 символов)",
  "description": "string (1-500 символов)", 
  "body": "string (обязательное поле)",
  "tag_list": ["string"] // опциональное поле
}
```

### Формат комментария

```json
{
  "body": "string (обязательное поле)"
}
```

## ✨ Особенности

- **Аутентификация JWT** - безопасная аутентификация с токенами
- **Система комментариев** - пользователи могут комментировать статьи
- **Автоматическая генерация slug** из заголовка статьи
- **Полная валидация данных** с помощью Pydantic
- **Пагинация** для списка статей и комментариев
- **Автоматическая документация API** (Swagger/OpenAPI)
- **Система миграций** с Alembic
- **Логирование запросов** и ошибок
- **CORS поддержка**
- **Docker контейнеризация**
- **Типизация** с помощью Python type hints
- **GitHub Actions** для CI/CD

## 🗂️ Структура проекта (Монолитная архитектура)

```
├── src/                  # Исходный код
│   ├── models/          # Слои работы с данными
│   │   ├── database.py  # SQLAlchemy модели
│   │   └── schemas.py   # Pydantic схемы
│   ├── routes/          # Объявление HTTP роутов
│   │   ├── users.py     # Маршруты пользователей
│   │   ├── user.py      # Маршруты текущего пользователя
│   │   ├── articles.py  # Маршруты статей
│   │   └── comments.py  # Маршруты комментариев
│   ├── controllers/     # Основная бизнес логика
│   │   └── crud.py      # CRUD операции
│   ├── middleware/      # Промежуточное ПО
│   │   └── auth.py      # Аутентификация
│   ├── utils/           # Утилиты
│   │   ├── auth.py      # JWT и хеширование
│   │   └── slug.py      # Генерация slug
│   ├── config.py        # Конфигурация
│   └── main.py          # Основной файл приложения
├── alembic/             # Миграции БД
│   ├── versions/        # Файлы миграций
│   └── env.py
├── .github/
│   └── workflows/       # GitHub Actions конфигурация
│       └── docker-publish.yaml
├── Dockerfile           # Dockerfile приложения
├── docker-compose.yml   # Файл compose
├── .env.example         # Пример переменных окружения
└── README.md           # Документация проекта
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

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123",
    "bio": "Software developer",
    "image_url": "https://example.com/avatar.jpg"
  }'
```

### Аутентификация

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

### Создание статьи (с токеном)

```bash
curl -X POST "http://localhost:8000/api/articles" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Моя первая статья",
    "description": "Краткое описание статьи",
    "body": "Полный текст статьи с подробным содержанием...",
    "tag_list": ["блог", "программирование", "API"]
  }'
```

### Python пример с аутентификацией

```python
import httpx
import asyncio

async def create_article_with_auth():
    # Сначала аутентифицируемся
    async with httpx.AsyncClient() as client:
        # Логин
        login_response = await client.post(
            "http://localhost:8000/api/users/login",
            json={
                "email": "user@example.com",
                "password": "password123"
            }
        )
        token = login_response.json()["data"]["access_token"]
        
        # Создаем статью с токеном
        article_response = await client.post(
            "http://localhost:8000/api/articles",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Новая статья",
                "description": "Описание",
                "body": "Содержание...",
                "tag_list": ["python", "fastapi"]
            }
        )
        return article_response.json()

# Использование
result = asyncio.run(create_article_with_auth())
print("Article created:", result)
```

## 🔧 Конфигурация

Основные настройки находятся в `src/config.py`:

- `DATABASE_URL` - URL подключения к PostgreSQL
- `SECRET_KEY` - секретный ключ для JWT
- `API_TITLE` - название API
- `ALLOWED_ORIGINS` - разрешенные CORS источники
- `ACCESS_TOKEN_EXPIRE_MINUTES` - время жизни токена

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

## 🔐 Безопасность

- **JWT токены** для аутентификации
- **Хеширование паролей** с bcrypt
- **Валидация данных** на всех уровнях
- **CORS настройки** для безопасности
- **Rate limiting** (можно добавить)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request