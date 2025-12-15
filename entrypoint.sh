#!/bin/bash
set -e

# Ожидаем доступности базы
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Waiting for database at $DB_HOST:$DB_PORT..."
  sleep 0.1
done

# миграции:
alembic upgrade head

# Запускаем
exec "$@"
