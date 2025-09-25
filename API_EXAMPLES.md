# Примеры использования API (Python/FastAPI)

## Создание статьи

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

**Ответ:**
```json
{
  "success": true,
  "message": "Article created successfully",
  "data": {
    "article": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Моя первая статья",
      "description": "Краткое описание статьи",
      "body": "Полный текст статьи с подробным содержанием...",
      "tag_list": ["блог", "программирование", "API"],
      "slug": "moya-pervaya-statya",
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    },
    "slug": "moya-pervaya-statya"
  }
}
```

## Получение списка статей

```bash
curl -X GET "http://localhost:8000/api/articles?skip=0&limit=10"
```

**Ответ:**
```json
{
  "success": true,
  "message": "Articles retrieved successfully",
  "data": {
    "articles": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "Моя первая статья",
        "description": "Краткое описание статьи",
        "body": "Полный текст статьи...",
        "tag_list": ["блог", "программирование", "API"],
        "slug": "moya-pervaya-statya",
        "created_at": "2024-01-01T12:00:00.000Z",
        "updated_at": "2024-01-01T12:00:00.000Z"
      }
    ],
    "count": 1
  }
}
```

## Получение статьи по slug

```bash
curl -X GET "http://localhost:8000/api/articles/moya-pervaya-statya"
```

## Обновление статьи

```bash
curl -X PUT "http://localhost:8000/api/articles/moya-pervaya-statya" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Обновленная статья",
    "description": "Новое описание"
  }'
```

## Удаление статьи

```bash
curl -X DELETE "http://localhost:8000/api/articles/moya-pervaya-statya"
```

## Ошибки валидации

При отправке некорректных данных:

```bash
curl -X POST "http://localhost:8000/api/articles" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "description": "Описание",
    "body": ""
  }'
```

**Ответ:**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    },
    {
      "type": "string_too_short",
      "loc": ["body", "body"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": {"min_length": 1}
    }
  ]
}
```

## Python примеры с httpx

### Создание статьи

```python
import httpx
import asyncio

async def create_article():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/articles",
            json={
                "title": "Новая статья",
                "description": "Описание новой статьи",
                "body": "Содержание статьи...",
                "tag_list": ["python", "fastapi"]
            }
        )
        return response.json()

# Использование
result = asyncio.run(create_article())
print("Article created:", result)
```

### Получение всех статей

```python
async def get_articles(skip=0, limit=10):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"http://localhost:8000/api/articles?skip={skip}&limit={limit}"
        )
        return response.json()

# Использование
articles = asyncio.run(get_articles())
print("Articles:", articles)
```

### Обновление статьи

```python
async def update_article(slug, data):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://localhost:8000/api/articles/{slug}",
            json=data
        )
        return response.json()

# Использование
updated = asyncio.run(update_article(
    "moya-pervaya-statya",
    {"title": "Новый заголовок", "description": "Новое описание"}
))
print("Updated:", updated)
```

### Удаление статьи

```python
async def delete_article(slug):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"http://localhost:8000/api/articles/{slug}"
        )
        return response.json()

# Использование
deleted = asyncio.run(delete_article("moya-pervaya-statya"))
print("Deleted:", deleted)
```

## Синхронные примеры с requests

### Создание статьи

```python
import requests

def create_article():
    response = requests.post(
        "http://localhost:8000/api/articles",
        json={
            "title": "Синхронная статья",
            "description": "Описание",
            "body": "Содержание...",
            "tag_list": ["requests", "python"]
        }
    )
    return response.json()

# Использование
result = create_article()
print("Article created:", result)
```

### Получение статей

```python
def get_articles():
    response = requests.get("http://localhost:8000/api/articles")
    return response.json()

# Использование
articles = get_articles()
print("Articles:", articles)
```

## Использование с FastAPI клиентом

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Создание статьи
response = client.post(
    "/api/articles",
    json={
        "title": "Тестовая статья",
        "description": "Описание",
        "body": "Содержание...",
        "tag_list": ["test", "fastapi"]
    }
)
print("Status:", response.status_code)
print("Response:", response.json())

# Получение статей
response = client.get("/api/articles")
print("Articles:", response.json())
```

## Обработка ошибок

```python
import httpx

async def safe_create_article():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/articles",
                json={
                    "title": "Статья",
                    "description": "Описание",
                    "body": "Содержание"
                }
            )
            response.raise_for_status()  # Вызовет исключение для HTTP ошибок
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
        print(f"Error details: {e.response.json()}")
    except httpx.RequestError as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Использование
asyncio.run(safe_create_article())
```
