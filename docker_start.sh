#!/bin/sh

# Run migrations in background so gunicorn can start immediately.
# Healthcheck hits /ping/ which needs no DB — passes as soon as gunicorn is up.
(
  MAX=10
  I=0
  while [ $I -lt $MAX ]; do
    if python manage.py migrate --noinput 2>&1; then
      echo "Migrations complete."
      break
    fi
    I=$((I+1))
    echo "Migration attempt $I/$MAX failed. Retrying in 3s..."
    sleep 3
  done
  [ $I -eq $MAX ] && echo "WARNING: migrations never completed after $MAX attempts."
) &

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 oromolegacy.wsgi:application
