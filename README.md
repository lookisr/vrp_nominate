# Премия года VRP - Telegram Mini App

Telegram Mini App для проведения голосования "Премия года VRP".

## Быстрый старт

### 1. Настройка

```bash
# Скопируйте файл с переменными окружения
cp env.example .env

# Отредактируйте .env и укажите:
# - TELEGRAM_BOT_TOKEN (получить у @BotFather)
# - ADMIN_IDS (ваш Telegram ID, узнать у @userinfobot)
```

### 2. Запуск через Docker

```bash
# Сборка образа
docker build -t vrp-app .

# Запуск контейнера
docker run -d --name vrp-app -p 8000:8000 --env-file .env vrp-app
```

### 3. Создание первой миграции

```bash
# Войдите в контейнер
docker exec -it vrp-app bash

# Создайте и примените миграции
cd /app/backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 4. Тестирование

- API: http://localhost:8000/docs
- Фронтенд: http://localhost:8000
- Telegram-бот: найдите вашего бота и отправьте `/admin`

## Структура проекта

```
vrp/
├── backend/          # FastAPI бэкенд
│   ├── app/
│   │   ├── api/      # API роутеры
│   │   ├── db/       # Модели БД и миграции
│   │   ├── services/ # Бизнес-логика
│   │   └── telegram_bot/ # Telegram-бот
│   └── alembic/      # Миграции БД
├── frontend/         # React Mini App
│   └── src/
│       ├── pages/    # Страницы приложения
│       ├── components/ # Компоненты
│       └── api/      # API клиент
└── docs/            # Документация
```

## Функционал

### Пользовательская часть (Mini App):
- Главный экран
- Просмотр номинаций
- Голосование за номинантов
- Просмотр результатов

### Административная часть (Telegram-бот):
- Управление номинациями (создание, редактирование, удаление)
- Управление номинантами (добавление, редактирование, удаление)
- Управление голосованием (старт/стоп)
- Просмотр статистики
- Экспорт результатов в CSV

## Подробная документация

См. [docs/setup.md](docs/setup.md) для подробных инструкций по установке и тестированию.

## Технологии

- **Backend**: FastAPI, SQLAlchemy, Alembic, aiogram
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Database**: PostgreSQL
- **Deployment**: Docker

