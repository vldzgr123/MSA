# Docker Compose Profiles

Этот проект использует Docker Compose профили для разных сценариев развертывания.

## Профили

### `dev` - Локальная разработка
Запускает только базу данных PostgreSQL для локальной разработки.

```bash
# Запуск только базы данных
docker-compose --profile dev up -d

# Остановка
docker-compose --profile dev down
```

### `prod` - Продакшн
Запускает полное приложение с базой данных и health checks.

```bash
# Запуск полного приложения
docker-compose --profile prod up -d

# Остановка
docker-compose --profile prod down
```

## Переменные окружения

### Для локальной разработки
Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/blog_platform
SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

### Для продакшн
Используйте переменные окружения или файл `.env.prod`:

```env
DATABASE_URL=postgresql://user:password@db:5432/blog_platform
SECRET_KEY=your-production-secret-key
DEBUG=false
```

## Health Checks

### База данных
- **Тест**: `pg_isready -U user -d blog_platform`
- **Интервал**: 10 секунд
- **Таймаут**: 5 секунд
- **Повторы**: 5

### Приложение
- **Тест**: `curl -f http://localhost:8000/health`
- **Интервал**: 30 секунд
- **Таймаут**: 10 секунд
- **Повторы**: 3
- **Период запуска**: 40 секунд

## Полезные команды

```bash
# Просмотр логов
docker-compose logs -f

# Просмотр логов конкретного сервиса
docker-compose logs -f app
docker-compose logs -f db

# Перезапуск сервиса
docker-compose restart app

# Просмотр статуса
docker-compose ps

# Выполнение команд в контейнере
docker-compose exec app bash
docker-compose exec db psql -U user -d blog_platform
```

