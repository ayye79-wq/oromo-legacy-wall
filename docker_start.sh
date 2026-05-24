#!/bin/sh
set -e

# Run migrations
python manage.py migrate --noinput 2>&1 | head -30

# Create/reset superuser if DJANGO_SUPERUSER_PASSWORD is set
python manage.py ensure_superuser

# Start gunicorn – PORT is injected by Railway (typically 8080)
exec gunicorn \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application
