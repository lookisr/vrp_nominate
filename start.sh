#!/usr/bin/env bash
set -euo pipefail

APP_HOME="/app"
POSTGRES_DATA="/var/lib/postgresql/data"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"
POSTGRES_DB="${POSTGRES_DB:-vrp}"
POSTGRES_USER="${POSTGRES_USER:-vrp_user}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-vrp_password}"
APP_PORT="${APP_PORT:-8000}"

echo "Инициализация PostgreSQL..."

# Используем pg_createcluster для PostgreSQL 17
if [ ! -d "${POSTGRES_DATA}/base" ]; then
  echo "Создаём новый кластер базы данных..."
  mkdir -p "${POSTGRES_DATA}"
  chown -R postgres:postgres "${POSTGRES_DATA}"
  
  # Инициализируем кластер
  su postgres -c "/usr/lib/postgresql/17/bin/initdb -D ${POSTGRES_DATA} --locale=C.UTF-8"
  
  # Настраиваем pg_hba.conf для подключений
  echo "host all all 0.0.0.0/0 scram-sha-256" >> "${POSTGRES_DATA}/pg_hba.conf"
  echo "local all all trust" >> "${POSTGRES_DATA}/pg_hba.conf"
  
  # Запускаем PostgreSQL
  su postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D ${POSTGRES_DATA} -o \"-c listen_addresses='*' -c port=${POSTGRES_PORT}\" -w start"
  
  # Создаём пользователя и базу данных
  sleep 2
  su postgres -c "psql -c \"CREATE USER ${POSTGRES_USER} WITH PASSWORD '${POSTGRES_PASSWORD}';\""
  su postgres -c "psql -c \"CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};\""
  su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${POSTGRES_DB} TO ${POSTGRES_USER};\""
  
  su postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D ${POSTGRES_DATA} -m fast -w stop"
fi

echo "Запускаем PostgreSQL..."
su postgres -c "/usr/lib/postgresql/17/bin/pg_ctl -D ${POSTGRES_DATA} -o \"-c listen_addresses='*' -c port=${POSTGRES_PORT}\" -w start"

cd "${APP_HOME}/backend"

echo "Применяем миграции..."
alembic upgrade head || echo "Предупреждение: миграции не выполнены (пока нет конфигурации)."

echo "Запускаем FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port "${APP_PORT}"

