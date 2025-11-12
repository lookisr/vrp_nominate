FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive \
    APP_HOME=/app

WORKDIR ${APP_HOME}

# Устанавливаем системные зависимости: PostgreSQL, Node.js, build tools.
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg build-essential ca-certificates postgresql && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    npm install -g npm@11.6.2 && \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости Python.
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Копируем весь проект.
COPY backend backend
COPY frontend frontend
COPY docs docs
COPY env.example .env

# Устанавливаем зависимости и собираем фронтенд.
WORKDIR ${APP_HOME}/frontend
RUN npm install && npm run build

# Переносим сборку фронтенда в бэкенд для отдачи статических файлов.
WORKDIR ${APP_HOME}
RUN mkdir -p backend/app/static && cp -r frontend/dist/* backend/app/static/

# Готовим директорию для данных PostgreSQL.
RUN mkdir -p /var/lib/postgresql/data && chown -R postgres:postgres /var/lib/postgresql

# Копируем стартовый скрипт.
COPY start.sh start.sh
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]

