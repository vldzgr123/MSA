#!/bin/bash

# Скрипт для инициализации проекта Blog Platform Backend

echo "🚀 Инициализация Blog Platform Backend..."

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Пожалуйста, установите Python 3.8+"
    exit 1
fi

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "⚙️ Создание файла конфигурации..."
    cp env.example .env
    echo "✅ Файл .env создан. Отредактируйте его с вашими настройками БД."
fi

# Инициализация Alembic
echo "🗄️ Инициализация Alembic..."
alembic init alembic

# Создание первой миграции
echo "📝 Создание первой миграции..."
alembic revision --autogenerate -m "Initial migration"

echo "✅ Инициализация завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Настройте PostgreSQL и создайте базу данных 'blog_platform'"
echo "2. Отредактируйте файл .env с правильными настройками БД"
echo "3. Запустите миграции: alembic upgrade head"
echo "4. Запустите сервер: uvicorn app.main:app --reload"
echo ""
echo "🌐 API будет доступен по адресу: http://localhost:8000"
echo "📚 Документация: http://localhost:8000/docs"
