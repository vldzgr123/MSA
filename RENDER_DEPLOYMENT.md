# Инструкции для деплоя на Render

## 🚀 Настройка Render

### 1. Создание Web Service

1. **Подключите GitHub репозиторий** к Render
2. **Выберите тип сервиса**: Web Service
3. **Настройте следующие параметры**:

#### Основные настройки:
- **Name**: `blog-platform-api`
- **Environment**: `Docker`
- **Region**: Выберите ближайший к вам
- **Branch**: `main`
- **Root Directory**: оставьте пустым
- **Dockerfile Path**: `Dockerfile`

#### Переменные окружения:
```env
DATABASE_URL=postgresql://username:password@hostname:port/database_name
SECRET_KEY=your-super-secret-key-for-production
DEBUG=false
```

### 2. Создание PostgreSQL Database

1. **Создайте новый PostgreSQL сервис** в Render
2. **Скопируйте DATABASE_URL** из настроек базы данных
3. **Добавьте DATABASE_URL** в переменные окружения Web Service

### 3. Настройка переменных окружения

#### Обязательные переменные:
- `DATABASE_URL` - URL базы данных PostgreSQL от Render
- `SECRET_KEY` - секретный ключ для JWT (используйте длинную случайную строку)

#### Опциональные переменные:
- `DEBUG=false` - отключить debug режим
- `ACCESS_TOKEN_EXPIRE_MINUTES=30` - время жизни JWT токена

### 4. Настройки деплоя

#### Build Command:
```bash
# Оставьте пустым - Dockerfile обработает всё
```

#### Start Command:
```bash
# Оставьте пустым - Dockerfile обработает всё
```

#### Health Check Path:
```
/health
```

### 5. Дополнительные настройки

#### Auto-Deploy:
- ✅ **Включено** - автоматический деплой при push в main

#### Pull Request Previews:
- ✅ **Включено** - для тестирования PR

## 🔧 Troubleshooting

### Проблема: "Connection refused"
**Решение**: Убедитесь, что DATABASE_URL правильно настроен и база данных создана.

### Проблема: "Migration failed"
**Решение**: Проверьте, что все миграции Alembic корректны и база данных доступна.

### Проблема: "Secret key not set"
**Решение**: Установите переменную окружения SECRET_KEY.

## 📊 Мониторинг

После успешного деплоя:

1. **Проверьте health check**: [https://msa-zfd1.onrender.com/health](https://msa-zfd1.onrender.com/health)
2. **Откройте API документацию**: [https://msa-zfd1.onrender.com/docs](https://msa-zfd1.onrender.com/docs)
3. **Проверьте логи** в панели Render

### ✅ Успешно развернуто!

Приложение успешно работает по адресу: [https://msa-zfd1.onrender.com](https://msa-zfd1.onrender.com)

## 🔐 Безопасность

### Для продакшн:
- ✅ Используйте сильный SECRET_KEY
- ✅ Установите DEBUG=false
- ✅ Настройте CORS для вашего домена
- ✅ Используйте HTTPS (Render предоставляет автоматически)

### Пример SECRET_KEY:
```bash
# Сгенерируйте случайный ключ
openssl rand -hex 32
```

## 📝 Примеры переменных окружения

```env
# База данных (замените на ваши данные)
DATABASE_URL=postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com/blog_platform

# Безопасность
SECRET_KEY=your-super-secret-key-here-change-in-production

# Настройки приложения
DEBUG=false
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (если нужно)
ALLOWED_ORIGINS=["https://your-frontend-domain.com"]
```
