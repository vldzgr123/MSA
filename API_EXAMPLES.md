# Примеры использования API (Python/FastAPI с аутентификацией)

## Регистрация пользователя

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

**Ответ:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "user@example.com",
      "username": "testuser",
      "bio": "Software developer",
      "image_url": "https://example.com/avatar.jpg",
      "is_active": true,
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    }
  }
}
```

## Аутентификация пользователя

```bash
curl -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

**Ответ:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "user@example.com",
      "username": "testuser",
      "bio": "Software developer",
      "image_url": "https://example.com/avatar.jpg",
      "is_active": true,
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

## Получение информации о текущем пользователе

```bash
curl -X GET "http://localhost:8000/api/user" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Обновление текущего пользователя

```bash
curl -X PUT "http://localhost:8000/api/user" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "bio": "Updated bio",
    "image_url": "https://example.com/new-avatar.jpg"
  }'
```

## Создание статьи (требует аутентификации)

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

**Ответ:**
```json
{
  "success": true,
  "message": "Article created successfully",
  "data": {
    "article": {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "title": "Моя первая статья",
      "description": "Краткое описание статьи",
      "body": "Полный текст статьи с подробным содержанием...",
      "tag_list": ["блог", "программирование", "API"],
      "slug": "moya-pervaya-statya",
      "author_id": "123e4567-e89b-12d3-a456-426614174000",
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
        "id": "456e7890-e89b-12d3-a456-426614174000",
        "title": "Моя первая статья",
        "description": "Краткое описание статьи",
        "body": "Полный текст статьи...",
        "tag_list": ["блог", "программирование", "API"],
        "slug": "moya-pervaya-statya",
        "author_id": "123e4567-e89b-12d3-a456-426614174000",
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

## Обновление статьи (только автор)

```bash
curl -X PUT "http://localhost:8000/api/articles/moya-pervaya-statya" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Обновленная статья",
    "description": "Новое описание"
  }'
```

## Удаление статьи (только автор)

```bash
curl -X DELETE "http://localhost:8000/api/articles/moya-pervaya-statya" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Ошибки валидации

При отправке некорректных данных:

```bash
curl -X POST "http://localhost:8000/api/users" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "invalid-email",
    "username": "ab",
    "password": "123"
  }'
```

**Ответ:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "input": "invalid-email"
    },
    {
      "type": "string_too_short",
      "loc": ["body", "username"],
      "msg": "String should have at least 3 characters",
      "input": "ab",
      "ctx": {"min_length": 3}
    },
    {
      "type": "string_too_short",
      "loc": ["body", "password"],
      "msg": "String should have at least 6 characters",
      "input": "123",
      "ctx": {"min_length": 6}
    }
  ]
}
```

## Python примеры с httpx

### Полный цикл: регистрация, логин, создание статьи

```python
import httpx
import asyncio

async def full_workflow():
    async with httpx.AsyncClient() as client:
        # 1. Регистрация пользователя
        register_response = await client.post(
            "http://localhost:8000/api/users",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "password123",
                "bio": "Python developer"
            }
        )
        print("Registration:", register_response.json())
        
        # 2. Логин
        login_response = await client.post(
            "http://localhost:8000/api/users/login",
            json={
                "email": "newuser@example.com",
                "password": "password123"
            }
        )
        token = login_response.json()["data"]["access_token"]
        print("Login successful, token:", token[:20] + "...")
        
        # 3. Получение информации о пользователе
        user_response = await client.get(
            "http://localhost:8000/api/user",
            headers={"Authorization": f"Bearer {token}"}
        )
        print("User info:", user_response.json())
        
        # 4. Создание статьи
        article_response = await client.post(
            "http://localhost:8000/api/articles",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Моя статья",
                "description": "Описание статьи",
                "body": "Содержание статьи...",
                "tag_list": ["python", "fastapi", "tutorial"]
            }
        )
        print("Article created:", article_response.json())
        
        # 5. Получение всех статей
        articles_response = await client.get("http://localhost:8000/api/articles")
        print("All articles:", articles_response.json())

# Использование
asyncio.run(full_workflow())
```

### Класс для работы с API

```python
import httpx
import asyncio
from typing import Optional, Dict, Any

class BlogAPI:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
    
    async def register(self, email: str, username: str, password: str, 
                      bio: str = "", image_url: str = "") -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/users",
                json={
                    "email": email,
                    "username": username,
                    "password": password,
                    "bio": bio,
                    "image_url": image_url
                }
            )
            return response.json()
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/users/login",
                json={"email": email, "password": password}
            )
            data = response.json()
            if data["success"]:
                self.token = data["data"]["access_token"]
            return data
    
    async def get_current_user(self) -> Dict[str, Any]:
        if not self.token:
            raise ValueError("Not authenticated")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/user",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.json()
    
    async def create_article(self, title: str, description: str, body: str, 
                           tag_list: list = None) -> Dict[str, Any]:
        if not self.token:
            raise ValueError("Not authenticated")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/articles",
                headers={"Authorization": f"Bearer {self.token}"},
                json={
                    "title": title,
                    "description": description,
                    "body": body,
                    "tag_list": tag_list or []
                }
            )
            return response.json()
    
    async def get_articles(self, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/articles?skip={skip}&limit={limit}"
            )
            return response.json()

# Использование
async def main():
    api = BlogAPI()
    
    # Регистрация и логин
    await api.register("test@example.com", "testuser", "password123")
    await api.login("test@example.com", "password123")
    
    # Создание статьи
    article = await api.create_article(
        "Тестовая статья",
        "Описание",
        "Содержание статьи...",
        ["test", "api"]
    )
    print("Article created:", article)
    
    # Получение статей
    articles = await api.get_articles()
    print("Articles:", articles)

asyncio.run(main())
```

## Синхронные примеры с requests

```python
import requests
import json

class BlogAPISync:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: str = None
    
    def register(self, email: str, username: str, password: str, 
                bio: str = "", image_url: str = ""):
        response = requests.post(
            f"{self.base_url}/api/users",
            json={
                "email": email,
                "username": username,
                "password": password,
                "bio": bio,
                "image_url": image_url
            }
        )
        return response.json()
    
    def login(self, email: str, password: str):
        response = requests.post(
            f"{self.base_url}/api/users/login",
            json={"email": email, "password": password}
        )
        data = response.json()
        if data["success"]:
            self.token = data["data"]["access_token"]
        return data
    
    def create_article(self, title: str, description: str, body: str, 
                      tag_list: list = None):
        if not self.token:
            raise ValueError("Not authenticated")
        
        response = requests.post(
            f"{self.base_url}/api/articles",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "title": title,
                "description": description,
                "body": body,
                "tag_list": tag_list or []
            }
        )
        return response.json()

# Использование
api = BlogAPISync()
api.register("sync@example.com", "syncuser", "password123")
api.login("sync@example.com", "password123")
article = api.create_article("Синхронная статья", "Описание", "Содержание...")
print("Article created:", article)
```

## Обработка ошибок

```python
import httpx

async def safe_api_call():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/api/users/login",
                json={
                    "email": "user@example.com",
                    "password": "wrongpassword"
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

asyncio.run(safe_api_call())
```

## Комментарии к статьям

### Добавление комментария к статье

```bash
curl -X POST "http://localhost:8000/api/articles/my-article-slug/comments" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "body": "Отличная статья! Очень полезная информация."
  }'
```

**Ответ:**
```json
{
  "success": true,
  "message": "Comment created successfully",
  "data": {
    "comment": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "body": "Отличная статья! Очень полезная информация.",
      "article_id": "456e7890-e89b-12d3-a456-426614174001",
      "author_id": "789e0123-e89b-12d3-a456-426614174002",
      "created_at": "2024-01-01T12:00:00.000Z",
      "updated_at": "2024-01-01T12:00:00.000Z"
    }
  }
}
```

### Получение комментариев к статье

```bash
curl -X GET "http://localhost:8000/api/articles/my-article-slug/comments?skip=0&limit=10"
```

**Ответ:**
```json
{
  "success": true,
  "message": "Comments retrieved successfully",
  "data": {
    "comments": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "body": "Отличная статья! Очень полезная информация.",
        "article_id": "456e7890-e89b-12d3-a456-426614174001",
        "author_id": "789e0123-e89b-12d3-a456-426614174002",
        "created_at": "2024-01-01T12:00:00.000Z",
        "updated_at": "2024-01-01T12:00:00.000Z"
      }
    ],
    "count": 1
  }
}
```

### Удаление комментария

```bash
curl -X DELETE "http://localhost:8000/api/articles/my-article-slug/comments/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Ответ:**
```json
{
  "success": true,
  "message": "Comment deleted successfully"
}
```

### Примеры с Python httpx для комментариев

```python
import httpx
import asyncio

async def test_comments():
    async with httpx.AsyncClient() as client:
        # 1. Логин для получения токена
        login_response = await client.post(
            "http://localhost:8000/api/users/login",
            json={
                "email": "user@example.com",
                "password": "password123"
            }
        )
        token = login_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Создание статьи
        article_response = await client.post(
            "http://localhost:8000/api/articles",
            json={
                "title": "Тестовая статья",
                "description": "Описание статьи",
                "body": "Содержание статьи",
                "tag_list": ["тест", "python"]
            },
            headers=headers
        )
        article_slug = article_response.json()["data"]["article"]["slug"]
        
        # 3. Добавление комментария
        comment_response = await client.post(
            f"http://localhost:8000/api/articles/{article_slug}/comments",
            json={
                "body": "Отличная статья!"
            },
            headers=headers
        )
        comment_id = comment_response.json()["data"]["comment"]["id"]
        
        # 4. Получение комментариев
        comments_response = await client.get(
            f"http://localhost:8000/api/articles/{article_slug}/comments"
        )
        print(f"Количество комментариев: {comments_response.json()['data']['count']}")
        
        # 5. Удаление комментария
        delete_response = await client.delete(
            f"http://localhost:8000/api/articles/{article_slug}/comments/{comment_id}",
            headers=headers
        )
        print("Комментарий удален")

asyncio.run(test_comments())
```
