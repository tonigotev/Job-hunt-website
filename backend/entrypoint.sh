#!/bin/sh

set -e

# Wait for the database to be ready
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 