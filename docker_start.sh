#!/bin/sh
set -e

MAX=10
I=0
echo "Running migrations (will retry up to $MAX times)..."
while [ $I -lt $MAX ]; do
    if python manage.py migrate --noinput 2>&1; then
        echo "Migrations done."
        break
    fi
    I=$((I+1))
    echo "Attempt $I/$MAX failed. Retrying in 3s..."
    sleep 3
done

if [ $I -eq $MAX ]; then
    echo "ERROR: Migrations never completed. Aborting."
    exit 1
fi

echo "Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 oromolegacy.wsgi:application
