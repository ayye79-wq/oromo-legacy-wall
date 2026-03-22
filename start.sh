#!/bin/bash
set -e

echo "==> Building React frontend..."
cd frontend && npm install && npm run build
cd ..

echo "==> Collecting static files..."
python manage.py collectstatic --noinput

echo "==> Starting Gunicorn..."
exec gunicorn --bind=0.0.0.0:5000 --reuse-port --workers=2 oromolegacy.wsgi:application
