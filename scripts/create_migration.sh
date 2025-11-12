#!/bin/bash

# Скрипт для создания первой миграции

echo "Создание первой миграции..."

cd backend

# Проверяем, существует ли виртуальное окружение
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Устанавливаем зависимости (если нужно)
if [ ! -f "venv/.installed" ]; then
    echo "Установка зависимостей..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Создаём миграцию
echo "Создание миграции..."
alembic revision --autogenerate -m "Initial migration"

echo "Миграция создана! Теперь примените её командой:"
echo "  alembic upgrade head"

