#!/bin/sh
set -e

echo "🔁 Running collectstatic..."
python manage.py collectstatic --no-input

echo "🔁 Running migrations..."
python manage.py migrate

exec "$@"