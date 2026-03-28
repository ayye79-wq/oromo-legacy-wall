#!/bin/sh
echo "=== STARTUP ==="
echo "PORT=${PORT}"
echo "PWD=$(pwd)"

echo "=== IMPORT CHECK ==="
python -c "import django; print('django OK', django.__version__)" || echo "DJANGO IMPORT FAILED"
python -c "import gunicorn; print('gunicorn OK', gunicorn.__version__)" || echo "GUNICORN IMPORT FAILED"
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oromolegacy.settings')
import django
django.setup()
print('django setup OK')
" || echo "DJANGO SETUP FAILED"

# Run migrations in the background
(python manage.py migrate --noinput 2>&1 && echo "Migrations OK") &

# Gunicorn must listen on the PORT Railway assigns
BIND_PORT=${PORT:-8000}
echo "Binding gunicorn to 0.0.0.0:${BIND_PORT}"
exec gunicorn \
  --bind 0.0.0.0:${BIND_PORT} \
  --workers 1 \
  --log-level info \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application
