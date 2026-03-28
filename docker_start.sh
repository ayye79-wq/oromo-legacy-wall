#!/bin/sh
echo "=== STARTUP ==="
echo "PORT=${PORT}"
echo "PWD=$(pwd)"
echo "PYTHON=$(python --version 2>&1)"

echo "=== IMPORT CHECK ==="
python -c "import django; print('django OK', django.__version__)" || echo "DJANGO IMPORT FAILED"
python -c "import gunicorn; print('gunicorn OK', gunicorn.__version__)" || echo "GUNICORN IMPORT FAILED"
python -c "import oromolegacy.wsgi; print('wsgi OK')" || echo "WSGI IMPORT FAILED"

echo "=== STARTING GUNICORN ==="
exec gunicorn \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers 1 \
  --log-level debug \
  --access-logfile - \
  --error-logfile - \
  oromolegacy.wsgi:application
