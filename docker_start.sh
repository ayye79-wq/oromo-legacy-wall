#!/bin/sh
set -e

# Run migrations (synchronous, brief timeout via DB connect_timeout in settings)
python manage.py migrate --noinput 2>&1 | head -30

# Start gunicorn – PORT is injected by Railway (typically 8080)
exec gunicorn \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --timeout 60 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application
